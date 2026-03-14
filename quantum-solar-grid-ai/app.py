from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from energy_simulator import simulate_energy
from qiskit_optimizer import optimize_decision
import requests

# Serve the frontend from the `frontend/` folder.
app = Flask(
    __name__,
    static_folder='frontend',
    static_url_path=''  # allow serving files directly from root
)
CORS(app)  # Enable CORS for all routes

WEATHER_API_KEY = '0a228300c1914eafab0162359261403'
WEATHER_CITY = 'Delhi'  # You can change this to user's location

def get_weather():
    """Fetch current weather data from OpenWeatherMap."""
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={WEATHER_API_KEY}&units=metric'
        response = requests.get(url)
        data = response.json()
        return {
            'temperature': data['main']['temp'],
            'condition': data['weather'][0]['main'],
            'description': data['weather'][0]['description']
        }
    except Exception as e:
        print(f"Weather API error: {e}")
        return {'temperature': 25, 'condition': 'Clear', 'description': 'Clear sky'}  # Fallback

@app.route('/')
def serve_index():
    """Serve the main dashboard page."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/run-optimization', methods=['GET'])
def run_optimization():
    """
    API endpoint to run the energy simulation and quantum optimization.

    Returns:
        JSON: Response containing energy data and decision.
    """
    # Get weather data
    weather = get_weather()

    # Simulate energy environment with weather influence
    energy_data = simulate_energy(weather['condition'])

    # Run quantum optimizer
    decision = optimize_decision(energy_data)

    # Prepare response
    response = {
        "solar_generation": energy_data["solar_generation"],
        "consumption": energy_data["consumption"],
        "battery_level": energy_data["battery_level"],
        "grid_price": energy_data["grid_price"],
        "decision": decision["decision_text"],
        "weather": weather
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)