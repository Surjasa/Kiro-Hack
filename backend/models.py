from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from db import Base

class Script(Base):
    __tablename__ = "scripts"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)
    generated_code = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Artwork(Base):
    __tablename__ = "artworks"

    id = Column(Integer, primary_key=True, index=True)
    input_spec = Column(Text, nullable=False)
    spec_type = Column(String(50), nullable=False)  # "yaml" or "english"
    generated_code = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())