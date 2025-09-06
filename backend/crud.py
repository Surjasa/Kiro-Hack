from sqlalchemy.orm import Session
from models import Script, Artwork
from schemas import ScriptGenerateRequest, ArtworkGenerateRequest

def create_script(db: Session, request: ScriptGenerateRequest, generated_code: str):
    db_script = Script(
        input_text=request.input_text,
        generated_code=generated_code
    )
    db.add(db_script)
    db.commit()
    db.refresh(db_script)
    return db_script

def create_artwork(db: Session, request: ArtworkGenerateRequest, generated_code: str):
    db_artwork = Artwork(
        input_spec=request.input_spec,
        spec_type=request.spec_type,
        generated_code=generated_code
    )
    db.add(db_artwork)
    db.commit()
    db.refresh(db_artwork)
    return db_artwork

def get_scripts(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(Script)
    if search:
        query = query.filter(Script.input_text.contains(search))
    return query.offset(skip).limit(limit).all()

def get_artworks(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(Artwork)
    if search:
        query = query.filter(Artwork.input_spec.contains(search))
    return query.offset(skip).limit(limit).all()