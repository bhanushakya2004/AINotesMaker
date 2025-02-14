# import requests
# from fastapi import FastAPI, HTTPException, Query

# # Set your OpenRouter API key
# api_key = "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"

# app = FastAPI()

# def get_ai_notes(content_type, subject_area, detail_level, note_taking_style, include_example):
#     url = "https://openrouter.ai/api/v1/completions"
    
#     prompt = f"""
#     Generate detailed notes for the subject '{subject_area}' with content type '{content_type}'. 
#     The notes should be at a '{detail_level}' level and include examples, explanations, bullet points, and in-depth insights.
#     The notes should follow a Harvard-style note format with proper structure: 
#     - Introduction 
#     - Key Concepts 
#     - Detailed Explanations 
#     - Examples with Applications 
#     - Summary/Conclusion 
#     Make sure to avoid any markdown symbols like '**', and focus on a clean and formal style.
#     """

#     data = {
#         "model": "deepseek/deepseek-chat:free",
#         "prompt": prompt,
#         "max_tokens": 2000
#     }
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#     }
#     response = requests.post(url, json=data, headers=headers)
    
#     if response.status_code == 200:
#         ai_text = response.json()['choices'][0]['text'].strip()
#         return ai_text if ai_text else "No content generated."
#     else:
#         return f"Error fetching AI notes: {response.status_code}"

# # FastAPI endpoint to fetch AI-generated notes in JSON format
# @app.get("/generate-notes/")
# async def generate_notes(
#     content_type: str = Query("Study Material", max_length=50),
#     subject_area: str = Query("Physics", max_length=50),
#     detail_level: str = Query("High", max_length=50),
#     note_taking_style: str = Query("Bullet Points", max_length=50),
#     include_example: bool = Query(True)
# ):
#     # Fetch AI-generated notes
#     ai_notes = get_ai_notes(content_type, subject_area, detail_level, note_taking_style, include_example)

#     if ai_notes == "No content generated.":
#         raise HTTPException(status_code=500, detail="Error fetching AI notes.")

#     # Return AI notes as JSON response
#     return {
#         "subject_area": subject_area,
#         "content_type": content_type,
#         "detail_level": detail_level,
#         "note_taking_style": note_taking_style,
#         "include_example": include_example,
#         "ai_generated_notes": ai_notes
#     }

# # To run the app, use the following command:
# # uvicorn main:app --reload

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

# Create FastAPI app
app = FastAPI()

# Allow requests from all origins (or specify the exact allowed origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific origins like ["http://yourfrontend.com"]
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Set your OpenRouter API key
api_key = "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"

def get_ai_notes(content_type, subject_area, detail_level, note_taking_style, include_example):
    url = "https://openrouter.ai/api/v1/completions"
    
    prompt = f"""
    Generate detailed notes for the subject '{subject_area}' with content type '{content_type}'. 
    The notes should be at a '{detail_level}' level and include examples, explanations, bullet points, and in-depth insights.
    The notes should follow a Harvard-style note format with proper structure: 
    - Introduction 
    - Key Concepts 
    - Detailed Explanations 
    - Examples with Applications 
    - Summary/Conclusion 
    Make sure to avoid any markdown symbols like '**', and focus on a clean and formal style.
    """

    data = {
        "model": "deepseek/deepseek-chat:free",
        "prompt": prompt,
        "max_tokens": 2000
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        ai_text = response.json()['choices'][0]['text'].strip()
        return ai_text if ai_text else "No content generated."
    else:
        return f"Error fetching AI notes: {response.status_code}"

@app.get("/generate-notes/")
async def generate_notes(
    content_type: str = Query("Lecture Notes", max_length=50),
    subject_area: str = Query("Mathematics", max_length=50),
    detail_level: str = Query("Medium", max_length=50),
    note_taking_style: str = Query("Outline", max_length=50),
    include_example: bool = Query(True)
):
    ai_notes = get_ai_notes(content_type, subject_area, detail_level, note_taking_style, include_example)
    
    if ai_notes == "No content generated.":
        return {"error": "Error fetching AI notes."}
    
    return {"notes": ai_notes}

