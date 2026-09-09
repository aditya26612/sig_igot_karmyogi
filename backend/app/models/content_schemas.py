from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class TranscriptChunkDTO(BaseModel):
    chunk_id: str
    lesson_id: str
    course_id: str
    competency_id: str
    topic: str
    start_seconds: int
    end_seconds: int
    timestamp_label: str
    text_content: str
    summary: Optional[str] = None

class CuratedLessonDTO(BaseModel):
    lesson_id: str
    playlist_id: str
    sequence_no: int
    title: str
    youtube_video_id: str
    youtube_url: str
    duration_minutes: int
    competency_id: str
    has_transcript: bool
    is_completed: bool = False

class CuratedPlaylistDTO(BaseModel):
    playlist_id: str
    title: str
    youtube_url: str
    channel_name: str
    competency_id: str
    competency_label: str
    description: str
    category: str
    total_lessons: int
    status: str
    provider_badge: str = "Curated YouTube Resource"
    lessons: Optional[List[CuratedLessonDTO]] = None

class LessonDetailResponse(BaseModel):
    lesson: CuratedLessonDTO
    playlist: CuratedPlaylistDTO
    transcript_chunks: List[TranscriptChunkDTO]
    next_lesson_id: Optional[str] = None
    prev_lesson_id: Optional[str] = None
    practice_available: bool = True
    provider_notice: str = "External curated video. Does not claim official iGOT LMS hosting."

class TranscriptSearchResultItem(BaseModel):
    chunk_id: str
    lesson_id: str
    lesson_title: str
    playlist_title: str
    competency_id: str
    topic: str
    timestamp_label: str
    start_seconds: int
    matching_snippet: str

class TranscriptSearchResponse(BaseModel):
    query: str
    total_matches: int
    results: List[TranscriptSearchResultItem]

class LessonProgressRequest(BaseModel):
    completed: bool = True
    seconds_watched: Optional[int] = None
