from flask import Flask, request
import google.generativeai as genai 
from dotenv import load_dotenv
import os
from determineUser import TravelAttractionData, Swipe
load_dotenv('secrets.env')
gemini_api_key = os.getenv('GEMINI_API_KEY')

app = Flask(__name__)
data = TravelAttractionData()
swiped = Swipe(TravelAttractionData=data)

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