from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db import get_db
from schemas import ArtworkGenerateRequest, ArtworkResponse
from typing import List
import crud
import yaml

router = APIRouter(prefix="/artworks", tags=["artworks"])

def generate_artwork_code(input_spec: str, spec_type: str) -> str:
    """Mock artwork generation - replace with actual AI/LLM integration"""
    if spec_type == "yaml":
        try:
            spec_data = yaml.safe_load(input_spec)
            spec_summary = f"YAML spec with keys: {list(spec_data.keys()) if isinstance(spec_data, dict) else 'parsed data'}"
        except:
            spec_summary = "YAML parsing failed, treating as text"
    else:
        spec_summary = f"English description: {input_spec[:100]}..."
    
    return f"""import React from 'react';

// Generated React component from: {spec_summary}
const GeneratedArtwork = () => {{
  return (
    <div style={{{{ padding: '20px', textAlign: 'center' }}}}>
      <h2>Generated Artwork</h2>
      <canvas 
        width="400" 
        height="300" 
        style={{{{ border: '1px solid #ccc' }}}}
        ref={{(canvas) => {{
          if (canvas) {{
            const ctx = canvas.getContext('2d');
            // TODO: Implement artwork based on: {input_spec[:50]}...
            ctx.fillStyle = '#4CAF50';
            ctx.fillRect(50, 50, 300, 200);
            ctx.fillStyle = 'white';
            ctx.font = '16px Arial';
            ctx.fillText('Generated Art', 150, 150);
          }}
        }}}}
      />
    </div>
  );
}};

export default GeneratedArtwork;
"""

@router.post("/generate-art", response_model=ArtworkResponse)
def create_artwork(
    request: ArtworkGenerateRequest,
    db: Session = Depends(get_db)
):
    try:
        generated_code = generate_artwork_code(request.input_spec, request.spec_type)
        artwork = crud.create_artwork(db, request, generated_code)
        return artwork
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[ArtworkResponse])
def get_artworks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    return crud.get_artworks(db, skip=skip, limit=limit, search=search)