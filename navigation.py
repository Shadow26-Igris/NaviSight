import requests
import html
from tts import TextToSpeech

class Navigation:
    def __init__(self, api_key):
        """
        Initialize navigation with Google Maps API key.
        """
        self.api_key = api_key
        self.tts = TextToSpeech()

    def get_directions(self, origin, destination):
        """
        Query Google Maps Directions API and speak turn-by-turn instructions.
        origin, destination: strings describing locations
        """
        url = f"https://maps.googleapis.com/maps/api/directions/json"
        params = {
            'origin': origin,
            'destination': destination,
            'key': self.api_key,
            'mode': 'walking'
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            self.tts.speak("Failed to get directions. Please try again later.")
            return False
        
        data = response.json()
        if data['status'] != 'OK':
            self.tts.speak(f"Google Maps error: {data['status']}")
            return False
        
        # Speak summarized directions step by step
        legs = data['routes'][0]['legs']
        self.tts.speak(f"Starting navigation from {origin} to {destination}.")
        for leg in legs:
            for step in leg['steps']:
                instruction = html.unescape(step['html_instructions'])
                # Remove HTML tags roughly by replacing them (or use regex if needed)
                instruction_text = instruction.replace('<b>', '').replace('</b>', '')
                instruction_text = instruction_text.replace('<div style="font-size:0.9em">', ". ").replace('</div>', '')
                print(f"Instruction: {instruction_text}")  # For debug
                self.tts.speak(instruction_text)
        self.tts.speak("You have arrived at your destination.")
        return True

if __name__ == "__main__":
    # Demo usage with placeholder origin/destination
    api_key = 'YOUR_GOOGLE_MAPS_API_KEY'
    navigation = Navigation(api_key)
    navigation.get_directions("Times Square, New York, NY", "Central Park, New York, NY")
