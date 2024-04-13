from flask import Flask, request
import google.generativeai as genai 
from dotenv import load_dotenv
import os

load_dotenv('secrets.env')
gemini_api_key = os.getenv('GEMINI_API_KEY')

app = Flask(__name__)

@app.route("/") 
def home():
	return "Hello, world!"

@app.route("/generate-locations",methods=["GET"])
def generate():
	preferences = request.args.get('preferences')

	
	genai.configure(api_key=gemini_api_key)
	model = genai.GenerativeModel(model_name='models/gemini-1.5-pro-latest',system_instruction="You are a travel agent and a tour guide who knows popular spots in the area")
	response = model.generate_content("Generate me a itinerary with these likes and dislikes: "+preferences)

	return response.text