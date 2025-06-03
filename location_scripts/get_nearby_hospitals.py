import requests

def get_nearby_hospitals(latitude: float, longitude: float, radius: int = 2000, max_results: int = 5):
    """
    Fetch nearby hospitals and nursing homes using Overpass API.
    Args:
        latitude (float): Latitude of the user/device
        longitude (float): Longitude of the user/device
        radius (int): Search radius in meters (default = 2000m)
        max_results (int): Maximum number of hospitals to return (default = 6)

    Returns:
        List of dicts with hospital names and types.
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
      node["amenity"="nursing_home"](around:{radius},{latitude},{longitude});
      way["amenity"="nursing_home"](around:{radius},{latitude},{longitude});
      relation["amenity"="nursing_home"](around:{radius},{latitude},{longitude});
      node["amenity"="hospital"](around:{radius},{latitude},{longitude});
      way["amenity"="hospital"](around:{radius},{latitude},{longitude});
      relation["amenity"="hospital"](around:{radius},{latitude},{longitude});
    );
    out center;
    """

    try:
        response = requests.get(overpass_url, params={'data': query}, timeout=10)
        response.raise_for_status()
        data = response.json()

        hospitals = []
        for element in data.get('elements', []):
            name = element['tags'].get('name')
            amenity_type = element['tags'].get('amenity')
            if name:
                hospitals.append({
                    "name": name,
                    "type": amenity_type
                })

        return hospitals[:max_results]

    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch nearby hospitals: {e}")
        return []
