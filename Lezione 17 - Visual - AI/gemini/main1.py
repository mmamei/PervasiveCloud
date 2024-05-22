import vertexai
from vertexai.generative_models import GenerativeModel
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'
vertexai.init(project='plcoud2024', location="us-central1")

model = GenerativeModel(model_name="gemini-1.0-pro-002")

response = model.generate_content(
    "Scrivi un breve paragrafo sull'uso di tecnologie cloud nell'ambito del pervasive computing"
)

print(response.text)