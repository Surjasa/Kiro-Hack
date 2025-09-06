from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db import get_db
from schemas import ScriptGenerateRequest, ScriptResponse
from typing import List
import crud

router = APIRouter(prefix="/scripts", tags=["scripts"])

def generate_script_code(input_text: str) -> str:
    """Mock script generation - replace with actual AI/LLM integration"""
    return f"""# Generated script from: {input_text[:50]}...
def main():
    print("Hello from generated script!")
    # TODO: Implement based on: {input_text}
    pass

if __name__ == "__main__":
    main()
"""

@router.post("/generate-script", response_model=ScriptResponse)
def create_script(
    request: ScriptGenerateRequest,
    db: Session = Depends(get_db)
):
    try:
        generated_code = generate_script_code(request.input_text)
        script = crud.create_script(db, request, generated_code)
        return script
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[ScriptResponse])
def get_scripts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    return crud.get_scripts(db, skip=skip, limit=limit, search=search)