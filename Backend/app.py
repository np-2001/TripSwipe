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
	preferences = str(request.args.get('data'))
	
	genai.configure(api_key=gemini_api_key)
	model = genai.GenerativeModel(model_name='models/gemini-1.5-pro-latest', system_instruction="You are a travel agent creating a 3 day intinerary for client in JSON. Note it needs to be in english.")
	response = model.generate_content("Generate a schedule with these preferences, in json, only provide names of businesses/locations, no extra detail, a vacation like experience, also make sure to some must see attractions"+ preferences)
	
	return response.text