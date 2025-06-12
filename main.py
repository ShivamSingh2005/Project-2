from fastapi import FastAPI, File, UploadFile
import requests
import fitz
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    doc = fitz.open(stream= await file.read(), filetype="pdf")
    all_text = ""
    for page in doc:
        text= page.get_text()
        all_text += text
    doc.close()
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    response = requests.post(
      url="https://openrouter.ai/api/v1/chat/completions",
      headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
      },
      json={
        "model": "openai/gpt-4o-mini",
        "messages": [
          {"role": "user", "content": f"The text given below is the resume of a person. Give me a structured resume in json format.\n {all_text}"},
        ],
        "response_format": {
          "type": "json_schema",
          "json_schema": {
            "name": "resume",
            "strict": True,
            "schema": {
              "type": "object",
              "properties": {
                "Education": {
                  "type": "string",
                  "description": "Educational qualifications in resume",
                },
                "Work experience": {
                  "type": "string",
                  "description": "Past work experience",
                },
                "Skills": {
                  "type": "string",
                  "description": "Skills in the resume",
                },
                "Awards and accomplishments": {
                  "type": "string",
                  "description": "Awards and accomplishments in the resume",
                },
                "Certifications": {
                  "type": "string",
                  "description": "Certifications in the resume",
                },
              },
              "required": ["Education", "Work experience", "Skills", "Awards and accomplishments", "Certifications" ],
              "additionalProperties": False,
            },
          },
        },
      },
    )
    data = response.json()
    weather_info = data["choices"][0]["message"]["content"]
    return weather_info

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, port=8000)   