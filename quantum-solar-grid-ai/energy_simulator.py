import numpy as np

def simulate_energy(weather_condition=None):
    """
    Simulates a smart home energy environment by generating random realistic values.

    Args:
        weather_condition (str): Weather condition like 'Clear', 'Clouds', 'Rain' to adjust solar generation.

    Returns:
        dict: A dictionary containing simulated energy values.
            - solar_generation: float, 0-10 kWh (adjusted by weather)
            - consumption: float, 1-8 kWh
            - battery_level: float, 0-100 percent
            - grid_price: float, ₹3-₹12 per kWh
    """
    # Adjust solar generation based on weather
    if weather_condition:
        if 'clear' in weather_condition.lower():
            solar_range = (6, 10)  # High solar on clear days
        elif 'cloud' in weather_condition.lower():
            solar_range = (2, 6)   # Moderate on cloudy
        elif 'rain' in weather_condition.lower() or 'snow' in weather_condition.lower():
            solar_range = (0, 2)   # Low on rainy/snowy
        else:
            solar_range = (0, 10)  # Default
    else:
        solar_range = (0, 10)  # Default if no weather

    # Generate random values using numpy
    solar_generation = np.random.uniform(*solar_range)
    consumption = np.random.uniform(1, 8)
    battery_level = np.random.uniform(0, 100)
    grid_price = np.random.uniform(3, 12)

    return {
        "solar_generation": round(solar_generation, 1),
        "consumption": round(consumption, 1),
        "battery_level": round(battery_level, 1),
        "grid_price": round(grid_price, 1)
    }