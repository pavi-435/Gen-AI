from flask import Flask, request, jsonify, render_template
import requests
import io
from PIL import Image
import base64
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory

app = Flask(__name__)

# Initialize the Translator using deep-translator
translator = GoogleTranslator(source='auto', target='en')

# Ensure consistent language detection results
DetectorFactory.seed = 0

# Hugging Face API URLs and token
TEXT_MODEL_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-Nemo-Instruct-2407"
IMAGE_MODEL_API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
headers = {"Authorization": "Hugging Face Token"}

# Function to query the text generation model
def query_text_model(prompt):
    structured_prompt = f"Please describe '{prompt}' in bullet points. Keep the response short, relevant, and concise."
    try:
        response = requests.post(TEXT_MODEL_API_URL, headers=headers, json={"inputs": structured_prompt})
        if response.status_code == 200:
            response_json = response.json()
            if isinstance(response_json, list) and len(response_json) > 0:
                generated_text = response_json[0].get('generated_text', 'No response')
                clean_text = generated_text.replace("**", "")
                points = [line.strip() for line in clean_text.split("\n") if line.strip()]
                if points:
                    points.pop(0)  # Remove the first point
                return points
            return []
        else:
            error_message = response.json().get('error', 'Unknown error')
            raise ValueError(f"Text generation failed with status code: {response.status_code}, Error: {error_message}")
    except requests.exceptions.RequestException as e:
        print("Request Error:", str(e))
        return None

# Function to format the response with bold topic and bullet points
def format_text_response(prompt, points):
    formatted_response = f"<strong>{prompt}:</strong><ul>"
    for point in points:
        formatted_response += f"<li style='text-indent: 20px;'>{point}</li>"
    formatted_response += "</ul>"
    return formatted_response

# Function to query the image generation model
def query_image_model(prompt):
    try:
        response = requests.post(IMAGE_MODEL_API_URL, headers=headers, json={"inputs": prompt})
        if response.status_code == 200 and response.headers['Content-Type'].startswith('image/'):
            return response.content
        else:
            raise ValueError("Image generation failed or unexpected content type")
    except requests.exceptions.RequestException as e:
        print("Request Error:", str(e))
        return None

# Function to convert image to base64
def image_to_base64(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    response_type = data.get('response_type', 'text')

    if response_type == 'image':
        image_bytes = query_image_model(user_input)
        if image_bytes:
            image_base64 = image_to_base64(image_bytes)
            return jsonify({"response": f'<img src="data:image/jpeg;base64,{image_base64}"/>'})
        else:
            return jsonify({"response": "Image generation failed"})

    elif response_type == 'translation':
        try:
            detected_language = detect(user_input)
        except Exception as e:
            return jsonify({"response": "Sorry, language detection failed. Please try again."})
        try:
            translated_input = translator.translate(user_input)
            return jsonify({"response": translated_input})
        except Exception as e:
            return jsonify({"response": "Sorry, translation failed. Please try again."})

    else:
        text_points = query_text_model(user_input)
        if text_points:
            formatted_response = format_text_response(user_input, text_points)
            return jsonify({"response": formatted_response})
        else:
            return jsonify({"response": "Text generation failed"})

if __name__ == '__main__':
    app.run(debug=True)
