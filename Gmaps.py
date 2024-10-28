import requests
from bidi.algorithm import get_display # For correct RTL display


def chunk_list(lst, n):
    """Split a list into chunks of size n."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_closest_location(api_key, home_address, locations):
    """
    Finds the closest location by walking distance from home_address using Google Maps Distance Matrix API.
    """
    
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    
    # Maximum number of destinations per request
    max_destinations = 10  # Adjust based on your needs and limits

    closest_location = None
    min_distance = float('inf')

    # Split locations into chunks
    for location_chunk in chunk_list(locations, max_destinations):
        params = {
            "origins": home_address,
            "destinations": "|".join(location_chunk),
            "mode": "walking",
            "language": "he",  # Language set to Hebrew
            "key": api_key
        }
        
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if data["status"] != "OK":
            raise Exception(f"Error with Google Maps API request: {data['status']}")

        for i, row in enumerate(data["rows"][0]["elements"]):
            if row["status"] == "OK":
                distance = row["distance"]["value"]  # Distance in meters
                if distance < min_distance:
                    min_distance = distance
                    closest_location = location_chunk[i]
            else:
                print(f"Could not calculate distance to {location_chunk[i]}: {row['status']}")
    
    return closest_location, min_distance

# Example usage
api_key = "API_KEY"
home_address = "רחוב מספר, תל אביב, ישראל"  # Home address in Hebrew
locations = [
    "דרך דיין משה 34, תל אביב, ישראל",
    "דבורה הנביאה 128, תל אביב, ישראל",
    "יהודה הימית 34, תל אביב, ישראל",
    "אבן גבירול 170, תל אביב, ישראל",
    "אלפסי 11, תל אביב, ישראל",
    "המסגר 60, תל אביב, ישראל",
    "הארד 5, תל אביב, ישראל",
    "נחל הבשור 1, תל אביב, ישראל",
    "לבנון חיים 67, תל אביב, ישראל",
    "קהילת לבוב 24, תל אביב, ישראל",
    "ארלוזורוב 93, תל אביב, ישראל",
    "הירקון 61, תל אביב, ישראל",
    "אחימאיר 27, תל אביב, ישראל",
    "שד' שאול המלך 8, תל אביב, ישראל",
    "שד' ירושלים 2, תל אביב, ישראל",
    "הגייסות 8, תל אביב, ישראל",
    "אורי צבי גרינברג 25, תל אביב, ישראל",
    "בוני העיר 9, תל אביב, ישראל",
    "אחימאיר אבא 33, תל אביב, ישראל",
    "הירקון 313, תל אביב, ישראל",
    "החשמונאים 121, תל אביב, ישראל",
    "חבר הלאומים 1, תל אביב, ישראל",
    "החשמונאים 88, תל אביב, ישראל",
    "המלך ג'ורג' 62, תל אביב, ישראל",
    "נחלת יצחק 18, תל אביב, ישראל",
    "הדר יוסף 20, תל אביב, ישראל",
    "יהודה הנשיא 34, תל אביב, ישראל",
    "השלושה 2, תל אביב, ישראל",
    "שד' ירושלים 12, תל אביב, ישראל",
    "אחד העם 9, תל אביב, ישראל",
    """אצ"ל 59, תל אביב, ישראל""",
    "מניה וישראל 13, תל אביב, ישראל",
    "הקשת 15, תל אביב, ישראל",
    "קבוץ גלויות 106, תל אביב, ישראל",
    "דרך בן צבי 41, תל אביב, ישראל",
    "דרך בגין 53, תל אביב, ישראל",
    "נחלת יצחק 18, תל אביב, ישראל",
    "לוינסקי 108, תל אביב, ישראל",
    "דרך בגין 65, תל אביב, ישראל",
    "מטלון 2, תל אביב, ישראל",
    "עמישב 36, תל אביב, ישראל",
    "שד' ההשכלה 1, תל אביב, ישראל",
    "המסגר 19, תל אביב, ישראל",
    "יהונתן 4, תל אביב, ישראל",
    "רוזן פנחס 67, תל אביב, ישראל",
    "החשמונאים 96, תל אביב, ישראל",
    "הקשת 6, תל אביב, ישראל",
    """אצ"ל 16, תל אביב,ישראל""",
    "בראלי 18, תל אביב, ישראל",
    "גרינבוים 41, תל אביב, ישראל"
]


closest_location, distance = get_closest_location(api_key, home_address, locations)
formatted_location = get_display(closest_location)  # Corrects RTL text display

print(f"The closest location is {formatted_location} at a distance of {distance} meters by foot.")

