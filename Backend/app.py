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

CORS(app, resources={r"/generate-location": {"origins": "http://localhost:58888"}})

format = {
		"Day 1": {
			"Morning": "Meiji Shrine",
			"Breakfast" : "",
			"Afternoon": "Harajuku",
			"Lunch" : "",
			"Evening": "Shibuya Crossing",
			"Dinner" : "",
			"Desciption" : "Relaxing description"
		},
		"Day 2": {
			"Morning": "Meiji Shrine",
			"Breakfast" : "",
			"Afternoon": "Harajuku",
			"Lunch" : "",
			"Evening": "Shibuya Crossing",
			"Dinner" : "",
			"Desciption" : "Relaxing description"
		},
		"Day 3": {
			"Morning": "Meiji Shrine",
			"Breakfast" : "",
			"Afternoon": "Harajuku",
			"Lunch" : "",
			"Evening": "Shibuya Crossing",
			"Dinner" : "",
			"Desciption" : "Relaxing description"
		}
	}

@app.route("/") 
def intialize():
	return data.recieveActivity()

@app.route("/generate-location",methods=["GET"])
def generate():
	# location = str(request.args.get('location'))
	preferences = swiped.retrieve("Sydney, Austrailia")
	genai.configure(api_key=gemini_api_key)
	model = genai.GenerativeModel(model_name='models/gemini-1.5-pro-latest',system_instruction="You are a travel agent who knows popular spots in the area the user is asking for things to do in that also provides business name recommendations. You must stick to the location the user asks for recommendations from")
	response = model.generate_content("Generate me a itinerary in with these likes and dislikes, return in JSON, no whitespace at the beginning or end, double quotes, description should be good bu less than or equal to 7 words: " + preferences + " and should output in this format " + str(format))
	
	print(response.text[5: -5])
	data_dict = json.loads(response.text[7: -5])
	return jsonify(data_dict)

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
			"Evening": "Roppongi Hills",
		},
		"Day 5": {
			"Morning": "Ghibli Museum", 
			"Afternoon": "Odaiba", 
			"Evening": "Shinjuku Golden Gai"
		}
	}
	return jsonify(itinerary)
	
	# return swiped.retrieve(location)