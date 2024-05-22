import vertexai
from vertexai.generative_models import GenerativeModel, Part
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'
vertexai.init(project='plcoud2024', location="us-central1")
model = GenerativeModel(model_name="gemini-1.0-pro-vision-001")

response = model.generate_content(
    [
        #Part.from_image(Image.load_from_file("image.jpg"))
        Part.from_uri(
            "gs://pcloud2024-1/image.jpg",
             mime_type="image/jpeg",
        ),
        "Cosa è rappresentato nell'immagine?",
    ]
)

print(response.text)

