import speech_recognition as sr

class VoiceCommand:
    def __init__(self):
        """
        Initialize the speech recognizer.
        """
        self.recognizer = sr.Recognizer()
    
    def listen(self, timeout=5, phrase_time_limit=7):
        """
        Listen from microphone and return recognized text.
        Returns None if recognition fails.
        """
        with sr.Microphone() as source:
            print("Listening for voice command...")
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                command = self.recognizer.recognize_google(audio)
                print(f"Recognized command: {command}")
                return command
            except sr.WaitTimeoutError:
                print("Listening timed out while waiting for phrase to start")
                return None
            except sr.UnknownValueError:
                print("Could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                return None

if __name__ == "__main__":
    vc = VoiceCommand()
    while True:
        cmd = vc.listen()
        if cmd:
            print(f"You said: {cmd}")
        else:
            print("No command detected.")
