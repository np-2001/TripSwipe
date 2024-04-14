from flask import Flask, request, jsonify
import google.generativeai as genai 
from dotenv import load_dotenv
import os
import json
from DetermineUser import TravelAttractionData, Swipe
from flask_cors import CORS

load_dotenv('secrets.env')
gemini_api_key = os.getenv('GEMINI_API_KEY')

app = Flask(__name__)
data = TravelAttractionData()
swiped = Swipe(TravelAttractionData=data)

CORS(app, resources={r"/preferences": {"origins": "http://localhost:58990"}})

@app.route("/") 
def intialize():
	return data.recieveActivity()

@app.route("/generate-locations",methods=["GET"])
def generate():
	preferences = str(request.args.get('data'))
	genai.configure(api_key=gemini_api_key)
	model = genai.GenerativeModel(model_name='models/gemini-1.5-pro-latest',system_instruction="You are a travel agent who knows popular spots in the area the user is asking for things to do in that also provides business name recommendations. You must stick to the location the user asks for recommendations from")
	response = model.generate_content("Generate me a itinerary in with these likes and dislikes, return in JSON: "+ preferences)

	return response.text

#{"Like":Boolean}
@app.route("/swipe",methods=["POST"])
def swipe():
	swipe_result = request.form.get("Like")
	swiped.swipe(swipe_result)
	swiped.newAttraction()
	return swiped.touristAttraction.recieveActivity()


@app.route("/preferences",methods=["GET"])
def preference():
	location = str(request.args.get('location'))

	itinerary = {
		"Day 1": {
			"Morning": "Meiji Shrine",
			"Afternoon": "Harajuku",
			"Evening": "Shibuya Crossing"
		},
		"Day 2": {
			"Morning": "Imperial Palace East Garden",
			"Afternoon": "Akihabara",
			"Evening": "Tokyo Dome City Attractions"
		},
		"Day 3": {
			"Morning": "Sensō-ji Temple",
			"Afternoon": "Ueno Park", 
			"Evening": "Ginza District"
		},
		"Day 4": {
			"Morning": "Tokyo National Museum",
			"Afternoon": "Tokyo Tower",
			"Evening": "Roppongi Hills"
		},
		"Day 5": {
			"Morning": "Ghibli Museum", 
			"Afternoon": "Odaiba", 
			"Evening": "Shinjuku Golden Gai"
		}
	}
	return jsonify(itinerary)
	
	# return swiped.retrieve(location)