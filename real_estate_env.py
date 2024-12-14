import gymnasium as gym
import numpy as np
from gymnasium import spaces

class RealEstateEnv(gym.Env):
    """Custom Environment for Real Estate Price Prediction"""
    
    def __init__(self, data):
        super(RealEstateEnv, self).__init__()
        
        self.data = data
        self.current_step = 0
        
        # Define action space (predicted price adjustment)
        self.action_space = spaces.Box(
            low=np.array([0.5]), 
            high=np.array([2.0]), 
            dtype=np.float32
        )
        
        # Define observation space
        # [location_encoding, square_feet, bedrooms, bathrooms, year_built, property_type_encoding]
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0, 1800, 0]),
            high=np.array([100, 10000, 10, 10, 2024, 5]),
            dtype=np.float32
        )
        
    def reset(self, seed=None):
        super().reset(seed=seed)
        self.current_step = 0
        
        # Get initial observation
        observation = self._get_observation()
        info = {}
        
        return observation, info
    
    def step(self, action):
        # Execute action (price prediction)
        predicted_price = self._get_base_price() * action[0]
        
        # Calculate reward based on prediction accuracy
        actual_price = self.data[self.current_step]['price']
        reward = -abs(predicted_price - actual_price) / actual_price
        
        # Move to next step
        self.current_step += 1
        done = self.current_step >= len(self.data)
        
        observation = self._get_observation()
        info = {
            'predicted_price': predicted_price,
            'actual_price': actual_price
        }
        
        return observation, reward, done, False, info
    
    def _get_observation(self):
        if self.current_step >= len(self.data):
            return np.zeros(self.observation_space.shape[0])
            
        current_data = self.data[self.current_step]
        
        return np.array([
            self._encode_location(current_data['location']),
            current_data['square_feet'],
            current_data['bedrooms'],
            current_data['bathrooms'],
            current_data['year_built'],
            self._encode_property_type(current_data['property_type'])
        ], dtype=np.float32)
    
    def _get_base_price(self):
        current_data = self.data[self.current_step]
        # Simple base price calculation
        return current_data['square_feet'] * 100
    
    def _encode_location(self, location):
        # TODO: Implement proper location encoding
        # For now, return a random encoding between 0 and 100
        return np.random.randint(0, 100)
    
    def _encode_property_type(self, property_type):
        property_types = {
            'house': 0,
            'apartment': 1,
            'condo': 2,
            'townhouse': 3
        }
        return property_types.get(property_type, 4)  # 4 for unknown types
