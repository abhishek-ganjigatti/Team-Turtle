from flask import Flask, render_template, request, jsonify
from model import RealEstateRL
import os
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
import googlemaps
import numpy as np

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Initialize Google Maps client
gmaps = googlemaps.Client(key='AIzaSyD6cabFRuL0Q1w3iDh9q0_HjEAqF3hUsUU')

# Initialize the RL model
try:
    model = RealEstateRL()
    logger.info("Model initialized successfully")
except Exception as e:
    logger.error(f"Error initializing model: {str(e)}")
    model = None

@app.route('/')
def home():
    return render_template('index.html')

def get_location_analytics(latitude, longitude, base_price):
    """Get price analytics for nearby locations"""
    try:
        # Get nearby locations
        places_result = gmaps.places_nearby(
            location=(float(latitude), float(longitude)),
            radius=5000,  # 5km radius
            type='real_estate_agency'
        )

        # Simulate different price points based on location
        # In a real application, this would come from your database
        nearby_avg = base_price * np.random.uniform(0.8, 1.2)
        city_avg = base_price * np.random.uniform(0.9, 1.3)
        state_avg = base_price * np.random.uniform(1.0, 1.4)

        return {
            'nearby_avg': nearby_avg,
            'city_avg': city_avg,
            'state_avg': state_avg
        }
    except Exception as e:
        logger.error(f"Error getting location analytics: {str(e)}")
        return None

def get_future_predictions(base_price):
    """Generate future price predictions"""
    try:
        # Generate growth factors for different time periods
        # In a real application, these would come from your ML model
        predictions = {
            '6_months': base_price * 1.1,
            '1_year': base_price * 1.2,
            '2_years': base_price * 1.4,
            '5_years': base_price * 1.8
        }
        return predictions
    except Exception as e:
        logger.error(f"Error generating future predictions: {str(e)}")
        return None

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if model is None:
            raise Exception("Model not properly initialized")

        if not request.is_json:
            raise Exception("Request must be JSON")

        data = request.get_json()
        logger.debug(f"Received prediction request with data: {data}")

        required_fields = ['location', 'latitude', 'longitude', 'square_feet', 
                         'bedrooms', 'bathrooms', 'year_built', 'property_type']
        for field in required_fields:
            if field not in data:
                raise Exception(f"Missing required field: {field}")

        features = {
            'location': str(data.get('location')),
            'square_feet': float(data.get('square_feet')),
            'bedrooms': int(data.get('bedrooms')),
            'bathrooms': float(data.get('bathrooms')),
            'year_built': int(data.get('year_built')),
            'property_type': str(data.get('property_type'))
        }
        
        logger.debug(f"Processed features: {features}")
        predicted_price = model.predict(features)
        logger.info(f"Base prediction successful: {predicted_price}")

        # Get location-based analytics
        location_analytics = get_location_analytics(
            data.get('latitude'), 
            data.get('longitude'),
            predicted_price
        )

        # Get future predictions
        future_predictions = get_future_predictions(predicted_price)
        
        response_data = {
            'success': True,
            'predicted_price': float(predicted_price)
        }

        # Add analytics if available
        if location_analytics:
            response_data.update(location_analytics)
        if future_predictions:
            response_data.update(future_predictions)

        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response

if __name__ == '__main__':
    # Enable debug mode for development
    app.run(host='127.0.0.1', port=5000, debug=True)
