def riegel_predict(time_s, distance_km, target_km=42.195, exponent=1.06):
    """Predict marathon time using Riegel's model.
    Input time_s: time in seconds for a given distance (distance_km)
    Returns predicted time in seconds for target_km (default: marathon distance)"""
    return time_s * (target_km / distance_km) ** exponent
