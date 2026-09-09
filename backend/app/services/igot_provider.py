from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import sqlite3
from app.database import get_db_connection, load_db
from app.engine import find

class BaseCourseProvider(ABC):
    @abstractmethod
    def get_provider_id(self) -> str:
        pass
        
    @abstractmethod
    def get_provider_name(self) -> str:
        pass
        
    @abstractmethod
    def get_badge_label(self) -> str:
        pass
        
    @abstractmethod
    def get_status(self) -> str:
        pass
        
    @abstractmethod
    def get_course_catalogue(self) -> List[Dict[str, Any]]:
        pass
        
    @abstractmethod
    def get_learner_training_history(self, user_id: str) -> List[Dict[str, Any]]:
        pass

class YouTubeProvider(BaseCourseProvider):
    def get_provider_id(self) -> str:
        return "YOUTUBE_CURATED"
        
    def get_provider_name(self) -> str:
        return "Curated YouTube Playlists"
        
    def get_badge_label(self) -> str:
        return "Curated YouTube Resource"
        
    def get_status(self) -> str:
        return "ACTIVE"
        
    def get_course_catalogue(self) -> List[Dict[str, Any]]:
        con = get_db_connection()
        try:
            cur = con.execute("SELECT * FROM curated_playlists WHERE status = 'ACTIVE'")
            return [dict(r) for r in cur.fetchall()]
        finally:
            con.close()
            
    def get_learner_training_history(self, user_id: str) -> List[Dict[str, Any]]:
        con = get_db_connection()
        try:
            cur = con.execute("SELECT * FROM practice_attempts WHERE user_id = ?", (user_id,))
            return [dict(r) for r in cur.fetchall()]
        finally:
            con.close()

class IGOTSimulatorProvider(BaseCourseProvider):
    def get_provider_id(self) -> str:
        return "IGOT_SIMULATOR"
        
    def get_provider_name(self) -> str:
        return "iGOT Karmayogi Integration Simulator"
        
    def get_badge_label(self) -> str:
        return "Simulated iGOT Integration"
        
    def get_status(self) -> str:
        return "SIMULATED_ACTIVE"
        
    def get_course_catalogue(self) -> List[Dict[str, Any]]:
        con = get_db_connection()
        try:
            D = load_db(con)
            return D.get("courses", [])
        finally:
            con.close()
            
    def get_learner_training_history(self, user_id: str) -> List[Dict[str, Any]]:
        con = get_db_connection()
        try:
            D = load_db(con)
            return [x for x in D.get("training_records", []) if x.get("user_id") == user_id]
        finally:
            con.close()

class FutureIGOTConnector(BaseCourseProvider):
    def get_provider_id(self) -> str:
        return "IGOT_LIVE_CONNECTOR"
        
    def get_provider_name(self) -> str:
        return "Direct iGOT Karmayogi Open API"
        
    def get_badge_label(self) -> str:
        return "Disabled (Awaiting MoSPI Production Credentials)"
        
    def get_status(self) -> str:
        return "DISABLED_PENDING_CREDENTIALS"
        
    def get_course_catalogue(self) -> List[Dict[str, Any]]:
        return []
        
    def get_learner_training_history(self, user_id: str) -> List[Dict[str, Any]]:
        return []

class ProviderRegistry:
    def __init__(self):
        self.providers = [
            YouTubeProvider(),
            IGOTSimulatorProvider(),
            FutureIGOTConnector()
        ]
        
    def get_all_providers(self) -> List[Dict[str, Any]]:
        return [
            {
                "provider_id": p.get_provider_id(),
                "name": p.get_provider_name(),
                "badge_label": p.get_badge_label(),
                "status": p.get_status(),
                "is_active": p.get_status() in ("ACTIVE", "SIMULATED_ACTIVE"),
                "is_live_external": p.get_provider_id() == "YOUTUBE_CURATED",
                "notice": "Never claims live iGOT access without verified API authorization."
            }
            for p in self.providers
        ]
        
    def get_provider(self, provider_id: str) -> Optional[BaseCourseProvider]:
        for p in self.providers:
            if p.get_provider_id() == provider_id:
                return p
        return None

provider_registry = ProviderRegistry()
