from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from app.database import get_db_connection, load_db
from app.auth import get_current_user
from app.engine import find
from app.services.transcript_service import search_transcripts
from app.models.content_schemas import (
    CuratedPlaylistDTO,
    CuratedLessonDTO,
    TranscriptChunkDTO,
    LessonDetailResponse,
    TranscriptSearchResponse,
    TranscriptSearchResultItem,
    LessonProgressRequest
)

router = APIRouter(prefix="/api/content", tags=["Content & Transcripts"])

@router.get("/playlists", response_model=List[CuratedPlaylistDTO])
def list_playlists(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Returns all curated YouTube playlists mapped to official competencies."""
    con = get_db_connection()
    try:
        D = load_db(con)
        cursor = con.execute("SELECT * FROM curated_playlists WHERE status = 'ACTIVE'")
        rows = cursor.fetchall()
        
        results = []
        for r in rows:
            comp = find(D, "competencies", "competency_id", r["competency_id"])
            label = comp["label"] if comp else r["competency_id"]
            results.append(CuratedPlaylistDTO(
                playlist_id=r["playlist_id"],
                title=r["title"],
                youtube_url=r["youtube_url"],
                channel_name=r["channel_name"],
                competency_id=r["competency_id"],
                competency_label=label,
                description=r["description"],
                category=r["category"],
                total_lessons=r["total_lessons"],
                status=r["status"],
                provider_badge="Curated YouTube Resource"
            ))
        return results
    finally:
        con.close()

@router.get("/playlists/{playlist_id}", response_model=CuratedPlaylistDTO)
def get_playlist_detail(playlist_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Returns a playlist with its ordered lesson series."""
    con = get_db_connection()
    try:
        D = load_db(con)
        cursor = con.execute("SELECT * FROM curated_playlists WHERE playlist_id = ?", (playlist_id,))
        p = cursor.fetchone()
        if not p:
            raise HTTPException(status_code=404, detail="Playlist not found")
            
        comp = find(D, "competencies", "competency_id", p["competency_id"])
        label = comp["label"] if comp else p["competency_id"]
        
        # Load lessons with the learner's persisted watch progress
        l_cur = con.execute("SELECT * FROM curated_lessons WHERE playlist_id = ? ORDER BY sequence_no ASC", (playlist_id,))
        w_cur = con.execute("SELECT lesson_id, completed FROM lesson_progress WHERE user_id = ?", (current_user["user_id"],))
        watched = {r["lesson_id"]: bool(r["completed"]) for r in w_cur.fetchall()}
        lessons = [
            CuratedLessonDTO(
                lesson_id=l["lesson_id"],
                playlist_id=l["playlist_id"],
                sequence_no=l["sequence_no"],
                title=l["title"],
                youtube_video_id=l["youtube_video_id"],
                youtube_url=l["youtube_url"],
                duration_minutes=l["duration_minutes"],
                competency_id=l["competency_id"],
                has_transcript=bool(l["has_transcript"]),
                is_completed=watched.get(l["lesson_id"], False)
            ) for l in l_cur.fetchall()
        ]
        
        return CuratedPlaylistDTO(
            playlist_id=p["playlist_id"],
            title=p["title"],
            youtube_url=p["youtube_url"],
            channel_name=p["channel_name"],
            competency_id=p["competency_id"],
            competency_label=label,
            description=p["description"],
            category=p["category"],
            total_lessons=p["total_lessons"],
            status=p["status"],
            provider_badge="Curated YouTube Resource",
            lessons=lessons
        )
    finally:
        con.close()

@router.get("/lessons/{lesson_id}", response_model=LessonDetailResponse)
def get_lesson_detail(lesson_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Returns full lesson details including YouTube video ID, sync'd transcript chunks,
    and playlist navigation.
    """
    con = get_db_connection()
    try:
        D = load_db(con)
        cur = con.execute("SELECT * FROM curated_lessons WHERE lesson_id = ?", (lesson_id,))
        l = cur.fetchone()
        if not l:
            raise HTTPException(status_code=404, detail=f"Lesson '{lesson_id}' not found")
            
        # Get Playlist
        p_cur = con.execute("SELECT * FROM curated_playlists WHERE playlist_id = ?", (l["playlist_id"],))
        p = p_cur.fetchone()
        
        comp = find(D, "competencies", "competency_id", l["competency_id"])
        label = comp["label"] if comp else l["competency_id"]
        
        # Get Transcript chunks
        c_cur = con.execute("SELECT * FROM transcript_chunks WHERE lesson_id = ? ORDER BY start_seconds ASC", (lesson_id,))
        chunks = [
            TranscriptChunkDTO(
                chunk_id=c["chunk_id"],
                lesson_id=c["lesson_id"],
                course_id=c["course_id"],
                competency_id=c["competency_id"],
                topic=c["topic"],
                start_seconds=c["start_seconds"],
                end_seconds=c["end_seconds"],
                timestamp_label=c["timestamp_label"],
                text_content=c["text_content"],
                summary=c["summary"]
            ) for c in c_cur.fetchall()
        ]
        
        # Find next/prev lessons
        siblings_cur = con.execute("SELECT lesson_id, sequence_no FROM curated_lessons WHERE playlist_id = ? ORDER BY sequence_no ASC", (l["playlist_id"],))
        siblings = siblings_cur.fetchall()
        current_seq = l["sequence_no"]
        prev_id = next((s["lesson_id"] for s in siblings if s["sequence_no"] == current_seq - 1), None)
        next_id = next((s["lesson_id"] for s in siblings if s["sequence_no"] == current_seq + 1), None)
        
        # The learner's persisted watch status for this lesson
        w_cur = con.execute(
            "SELECT completed FROM lesson_progress WHERE user_id = ? AND lesson_id = ?",
            (current_user["user_id"], lesson_id)
        )
        w_row = w_cur.fetchone()
        is_completed = bool(w_row["completed"]) if w_row else False

        lesson_dto = CuratedLessonDTO(
            lesson_id=l["lesson_id"],
            playlist_id=l["playlist_id"],
            sequence_no=l["sequence_no"],
            title=l["title"],
            youtube_video_id=l["youtube_video_id"],
            youtube_url=l["youtube_url"],
            duration_minutes=l["duration_minutes"],
            competency_id=l["competency_id"],
            has_transcript=bool(l["has_transcript"]),
            is_completed=is_completed
        )
        
        playlist_dto = CuratedPlaylistDTO(
            playlist_id=p["playlist_id"],
            title=p["title"],
            youtube_url=p["youtube_url"],
            channel_name=p["channel_name"],
            competency_id=p["competency_id"],
            competency_label=label,
            description=p["description"],
            category=p["category"],
            total_lessons=p["total_lessons"],
            status=p["status"],
            provider_badge="Curated YouTube Resource"
        )
        
        return LessonDetailResponse(
            lesson=lesson_dto,
            playlist=playlist_dto,
            transcript_chunks=chunks,
            next_lesson_id=next_id,
            prev_lesson_id=prev_id,
            practice_available=True,
            provider_notice="Curated external video resource. Transcript and practice questions processed locally."
        )
    finally:
        con.close()

@router.get("/lessons/{lesson_id}/transcript", response_model=List[TranscriptChunkDTO])
def get_lesson_transcripts(lesson_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Returns transcript segments for a lesson."""
    con = get_db_connection()
    try:
        c_cur = con.execute("SELECT * FROM transcript_chunks WHERE lesson_id = ? ORDER BY start_seconds ASC", (lesson_id,))
        rows = c_cur.fetchall()
        return [
            TranscriptChunkDTO(
                chunk_id=c["chunk_id"],
                lesson_id=c["lesson_id"],
                course_id=c["course_id"],
                competency_id=c["competency_id"],
                topic=c["topic"],
                start_seconds=c["start_seconds"],
                end_seconds=c["end_seconds"],
                timestamp_label=c["timestamp_label"],
                text_content=c["text_content"],
                summary=c["summary"]
            ) for c in rows
        ]
    finally:
        con.close()

@router.get("/search", response_model=TranscriptSearchResponse)
def search_transcript_content(
    q: str = Query(..., min_length=2, description="Search keyword across lesson transcripts"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Full-text search across all lesson transcripts with topic and timestamp references."""
    con = get_db_connection()
    try:
        matches = search_transcripts(con, q)
        items = [
            TranscriptSearchResultItem(
                chunk_id=m["chunk_id"],
                lesson_id=m["lesson_id"],
                lesson_title=m["lesson_title"],
                playlist_title=m["playlist_title"],
                competency_id=m["competency_id"],
                topic=m["topic"],
                timestamp_label=m["timestamp_label"],
                start_seconds=m["start_seconds"],
                matching_snippet=m["matching_snippet"]
            ) for m in matches
        ]
        return TranscriptSearchResponse(
            query=q,
            total_matches=len(items),
            results=items
        )
    finally:
        con.close()

@router.post("/lessons/{lesson_id}/progress")
def record_lesson_progress(
    lesson_id: str,
    request: LessonProgressRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Updates learner progress on a lesson (watching completion). Persisted per-user."""
    con = get_db_connection()
    try:
        l_cur = con.execute("SELECT lesson_id FROM curated_lessons WHERE lesson_id = ?", (lesson_id,))
        if not l_cur.fetchone():
            raise HTTPException(status_code=404, detail=f"Lesson '{lesson_id}' not found in curriculum catalogue.")
        now = datetime.now(timezone.utc).isoformat()
        with con:
            con.execute("""
            INSERT INTO lesson_progress (user_id, lesson_id, completed, seconds_watched, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id, lesson_id) DO UPDATE SET
                completed = excluded.completed,
                seconds_watched = COALESCE(excluded.seconds_watched, lesson_progress.seconds_watched),
                updated_at = excluded.updated_at
            """, (current_user["user_id"], lesson_id, int(request.completed), request.seconds_watched, now))
        return {
            "status": "RECORDED",
            "lesson_id": lesson_id,
            "user_id": current_user["user_id"],
            "completed": request.completed,
            "notice": "Lesson progress updated. Practice quiz is recommended next."
        }
    finally:
        con.close()
