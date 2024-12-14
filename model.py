import os
import numpy as np
from stable_baselines3 import PPO
from real_estate_env import RealEstateEnv
import logging

logger = logging.getLogger(__name__)

class RealEstateRL:
    def __init__(self):
        self.model = None
        self.env = None
        try:
            self._initialize_environment()
            self._load_or_create_model()
        except Exception as e:
            logger.error(f"Error initializing RealEstateRL: {str(e)}")
            raise
    
    def _initialize_environment(self):
        try:
            # Initialize with dummy data for now
            self.dummy_data = [{
                'location': 'downtown',
                'square_feet': 1500,
                'bedrooms': 3,
                'bathrooms': 2,
                'year_built': 2000,
                'property_type': 'house',
                'price': 300000
            }]
            self.env = RealEstateEnv(self.dummy_data)
            logger.info("Environment initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing environment: {str(e)}")
            raise
    
    def _load_or_create_model(self):
        try:
            model_dir = 'real_estate_price_model'
            model_path = os.path.join(model_dir, 'model.zip')
            
            if os.path.exists(model_path):
                try:
                    self.model = PPO.load(model_path, env=self.env)
                    logger.info("Model loaded successfully!")
                except Exception as e:
                    logger.warning(f"Error loading model: {e}. Creating new model.")
                    self._create_new_model()
            else:
                logger.info("No existing model found. Creating new model.")
                self._create_new_model()
        except Exception as e:
            logger.error(f"Error in _load_or_create_model: {str(e)}")
            raise
    
    def _create_new_model(self):
        try:
            logger.info("Creating new model...")
            self.model = PPO(
                "MlpPolicy",
                self.env,
                verbose=1,
                learning_rate=0.0003,
                n_steps=2048,
                batch_size=64,
                n_epochs=10,
                gamma=0.99,
                gae_lambda=0.95,
                clip_range=0.2
            )
            logger.info("New model created successfully")
        except Exception as e:
            logger.error(f"Error creating new model: {str(e)}")
            raise
    
    def train(self, episodes=1000):
        """Train the model on the available data"""
        try:
            if self.model is None:
                raise Exception("Model not initialized")
            
            self.model.learn(total_timesteps=episodes)
            
            # Save the trained model
            os.makedirs('real_estate_price_model', exist_ok=True)
            self.model.save('real_estate_price_model/model.zip')
            logger.info(f"Model trained and saved successfully after {episodes} episodes")
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            raise
    
    def predict(self, features):
        """Make price predictions using the trained model"""
        try:
            if self.model is None:
                raise Exception("Model not initialized")
            
            # Validate input features
            self._validate_features(features)
            
            # Convert features to observation format
            observation = np.array([
                self._encode_location(features['location']),
                float(features['square_feet']),
                int(features['bedrooms']),
                float(features['bathrooms']),
                int(features['year_built']),
                self._encode_property_type(features['property_type'])
            ], dtype=np.float32)
            
            logger.debug(f"Processed observation: {observation}")
            
            # Get model prediction
            action, _ = self.model.predict(observation)
            
            # Calculate base price in rupees (assuming 100 USD per sq ft)
            base_price = float(features['square_feet']) * 8300  # Approximately ₹8300 per sq ft
            
            # Apply the model's price adjustment
            predicted_price = base_price * action[0]
            
            logger.info(f"Prediction successful: ₹{predicted_price:,.2f}")
            return predicted_price
            
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            raise
    
    def _validate_features(self, features):
        required_fields = ['location', 'square_feet', 'bedrooms', 'bathrooms', 'year_built', 'property_type']
        for field in required_fields:
            if field not in features:
                raise ValueError(f"Missing required feature: {field}")
        
        try:
            float(features['square_feet'])
            int(features['bedrooms'])
            float(features['bathrooms'])
            int(features['year_built'])
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid feature value: {str(e)}")
    
    def _encode_location(self, location):
        try:
            # TODO: Implement proper location encoding
            return np.random.randint(0, 100)
        except Exception as e:
            logger.error(f"Error encoding location: {str(e)}")
            raise
    
    def _encode_property_type(self, property_type):
        try:
            property_types = {
                'house': 0,
                'apartment': 1,
                'condo': 2,
                'townhouse': 3
            }
            return property_types.get(str(property_type).lower(), 4)
        except Exception as e:
            logger.error(f"Error encoding property type: {str(e)}")
            raise
