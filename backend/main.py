from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import engine, Base
from routers import scripts, artworks

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Code Alchemist API",
    description="Generate scripts and artwork from natural language",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(scripts.router)
app.include_router(artworks.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Code Alchemist API"}

@app.get("/hello")
def say_hello():
    return {"message": "Hello, World!"}

@app.post("/scripts/generate-script")
def generate_script(input_text: str):
    return {"script": f'print("{input_text}")'}

