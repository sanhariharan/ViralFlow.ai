from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class ContentRequest(BaseModel):
    base_content: str
    platforms: List[str]
    tone: str

class ContentMetadata(BaseModel):
    intent: str
    audience: str
    keywords: List[str]
    topic: str
    tone: str
    summary: str

class PlatformContent(BaseModel):
    platform: str
    content: str
    hashtags: List[str] = []
    schedule: Optional[str] = None

class GenerationResponse(BaseModel):
    platform_outputs: Dict[str, str]
    hashtags: Dict[str, List[str]]
    schedules: Dict[str, str]
    visuals: List[str] = []
    metadata: Dict[str, Any] = {}

class VisualsRequest(BaseModel):
    topic: str
    keywords: List[str]
