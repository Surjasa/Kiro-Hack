from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class ScriptGenerateRequest(BaseModel):
    input_text: str

class ScriptResponse(BaseModel):
    id: int
    input_text: str
    generated_code: str
    created_at: datetime

    class Config:
        from_attributes = True

class ArtworkGenerateRequest(BaseModel):
    input_spec: str
    spec_type: Literal["yaml", "english"] = "english"

class ArtworkResponse(BaseModel):
    id: int
    input_spec: str
    spec_type: str
    generated_code: str
    created_at: datetime

    class Config:
        from_attributes = True