# Smart Real Estate Mapping and Analysis

This project is a web-based real estate price predictor and neighborhood hotspot analyzer. It uses machine learning and Google Maps API to predict real estate prices based on user inputs (such as location, square footage, number of rooms, etc.) and also provides a tool to analyze nearby hotspots like schools, hospitals, parks, and restaurants using the Google Maps Places API.

### Features

- **Real Estate Price Prediction**: 
  - Predict the price of a property based on location, square footage, number of rooms, property type, and more.
  - Display predicted prices along with price comparisons to nearby, city, and state averages.
  - Show future price trends for the property.
  
- **Neighborhood Hotspot Analyzer**:
  - Search for nearby hotspots (schools, restaurants, hospitals, parks, etc.) based on a specified radius.
  - Visualize the data with markers and a heatmap on a map.
  - Display nearby places in a list with information such as rating and vicinity.

### Technologies Used

- **Frontend**:
  - HTML, CSS, JavaScript (with Bootstrap for UI)
  - Google Maps JavaScript API
  - Chart.js for visualizing predictions

- **Backend**:
  - Python Flask for the API
  - Machine learning model for real estate price prediction (using pre-trained models)
  
- **Other Tools**:
  - Google Places API for searching nearby places

### Setup Instructions

#### 1. Clone the repository:
```bash
git clone https://github.com/your-username/real-estate-price-predictor.git
cd real-estate-price-predictor
```

#### 2. Install dependencies for the backend (Flask and other libraries):
Make sure you have Python 3.x installed.

```bash
pip install -r requirements.txt
```

#### 3. Set up Google Maps API:
- Obtain an API key from the [Google Cloud Console](https://console.cloud.google.com/).
- Replace `API_KEY` in `config.js` with your actual Google Maps API key.

#### 4. Running the Backend:
To run the Flask backend locally, use the following command:

```bash
python app.py
```

This will start the Flask server on `http://127.0.0.1:5000/`.

#### 5. Running the Frontend:
The frontend is a static website. To view it, simply open the `index.html` file in a browser.

#### 6. Testing:
Test the API and frontend together by submitting the form on the web page and ensuring the predictions are returned and displayed correctly.

---

## Directory Structure

```
real-estate-price-predictor/
├── app.py                  # Main Flask app for handling prediction requests
├── app.js                  # JavaScript file for handling frontend logic
├── config.js               # Configuration file for Google Maps API key and other settings
├── requirements.txt        # Python dependencies for backend
├── static/                 # Folder containing static assets (CSS, images, etc.)
│   └── styles.css          # Custom CSS for styling the frontend
├── templates/              # Folder containing HTML templates (Flask)
│   └── index.html          # Main HTML file for the frontend
└── __pycache__/            # Compiled Python bytecode (automatically generated)
```

### Explanation of Key Files

- `app.py`: This file contains the Flask app and routes for handling requests to the backend. It listens for prediction requests and returns predicted property prices based on input data.
  
- `app.js`: The frontend JavaScript responsible for handling user interactions, sending requests to the backend, and displaying results on the page (including map and charts).
  
- `config.js`: Contains configuration settings, including the Google Maps API key and default settings (e.g., map center, zoom level).
  
- `requirements.txt`: Lists the Python dependencies, including Flask and any machine learning libraries you might use (e.g., scikit-learn, pandas).

- `index.html`: The main HTML page that is loaded by the browser. It contains the form for user input, map visualization, and displays the predicted price.

- `styles.css`: The CSS file for styling the frontend of the application.

---

### Contributing

1. Fork this repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make changes and commit (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a new pull request.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Let me know if you need any additional changes or have other specific details to include!
