import vertexai
from vertexai.generative_models import GenerativeModel
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'
vertexai.init(project='plcoud2024', location="europe-west8")

model = GenerativeModel(model_name="gemini-1.0-pro")

response = model.generate_content(
    "Scrivi un breve paragrafo sull'uso di tecnologie cloud nell'ambito del pervasive computing"
)

print(response.text)