import os
from typing import List
from pydantic import BaseModel
from google import genai
from google.genai import types
from config import settings

class TriageResult(BaseModel):
    severity: str
    disclaimer: str
    first_aid_steps: List[str]
    what_not_to_do: List[str]
    bounding_boxes: List[List[float]]
    voice_summary: str

def analyze_emergency(image_bytes: bytes, user_text: str, target_language: str) -> TriageResult:
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    prompt = f"""
    Analyze this emergency image and context: '{user_text}'.
    Target language: {target_language}.
    Provide structured triage result with severity (LOW, MEDIUM, HIGH, CRITICAL), 
    disclaimer, first aid steps, what NOT to do, bounding boxes [ymin, xmin, ymax, xmax], 
    and a 2-sentence voice summary in {target_language}.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            prompt
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=TriageResult,
        ),
    )
    return TriageResult.model_validate_json(response.text)