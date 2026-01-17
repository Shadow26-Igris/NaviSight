// Unified speak function: Uses backend TTS with browser fallback
async function speak(text) {
  if (!text) return;

  try {
    const response = await fetch('http://localhost:5000/voice/speak', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });

    if (!response.ok) throw new Error('TTS backend failed');

    const audioBlob = await response.blob();
    const audioUrl = URL.createObjectURL(audioBlob);

    const audio = new Audio(audioUrl);
    audio.play();
  } catch (err) {
    console.warn("Falling back to browser speech:", err);
    speakFallback(text);
  }
}

// Fallback TTS using browser (SpeechSynthesis)
function speakFallback(text) {
  if ('speechSynthesis' in window && text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = 1;
    utterance.pitch = 1;
    speechSynthesis.speak(utterance);
  } else {
    console.error("No speech synthesis available.");
  }
}

// Automatically speak on page load
document.addEventListener("DOMContentLoaded", () => {
  // Initial instructions
  setTimeout(() => {
    speak("Welcome to NaviSight. This is a smart navigation assistant for the visually impaired. You are on the home page.");
    speak("The camera feed is below. Use the tab key to explore the page.");
  }, 1000);

  // Describe sections when in view
  speakOnView("#features", "These are the key features of NaviSight: obstacle detection, voice guidance, and GPS navigation.");
  speakOnView("#how-it-works", "This section explains how NaviSight works in three steps.");

  // Auto-start geolocation tracking
  trackLocationAndRequestDirections();

  // Fetch latest alert every 10 seconds
  setInterval(() => {
    fetch('http://localhost:5000/latest_alert')
      .then(res => res.json())
      .then(data => {
        const alert = data.alert;
        if (alert) {
          speak(alert);
          document.getElementById("latest-alert").textContent = `Latest alert: ${alert}`;
        }
      })
      .catch(err => console.error("Alert fetch error:", err));
  }, 10000);
});

// Speak when a section comes into view
function speakOnView(selector, message) {
  const section = document.querySelector(selector);
  if (!section) {
    console.warn(`Section not found: ${selector}`);
    return;
  }

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        speak(message);
        observer.disconnect();
      }
    });
  }, { threshold: 0.3 });

  observer.observe(section);
}

// Location + route planning
let destinationCoords = null;

function startNavigation() {
  const destinationInput = document.getElementById("destination-input").value;
  if (!destinationInput) {
    speak("Please enter a destination.");
    return;
  }

  fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(destinationInput)}&format=json`)
    .then(res => res.json())
    .then(data => {
      if (data.length === 0) {
        speak("Could not find that destination.");
        return;
      }

      destinationCoords = {
        lat: parseFloat(data[0].lat),
        lng: parseFloat(data[0].lon)
      };

      document.getElementById("destination").textContent = `Destination: ${destinationInput}`;
      watchUserLocation();
    })
    .catch(err => {
      console.error("Geocoding error:", err);
      speak("Failed to get destination coordinates.");
    });
}

function watchUserLocation() {
  if (!navigator.geolocation) {
    speak("Geolocation is not supported.");
    return;
  }

  navigator.geolocation.watchPosition((position) => {
    const userLat = position.coords.latitude;
    const userLng = position.coords.longitude;

    document.getElementById("current-location").textContent =
      `Your location: ${userLat.toFixed(5)}, ${userLng.toFixed(5)}`;

    if (destinationCoords) {
      fetch('http://localhost:5000/route/get-directions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_lat: userLat,
          user_lng: userLng,
          destination_lat: destinationCoords.lat,
          destination_lng: destinationCoords.lng
        })
      })
        .then(res => res.json())
        .then(data => {
          if (data.distance) {
            const dist = data.distance.toFixed(2);
            document.getElementById("distance-info").textContent = `Distance: ${dist} kilometers`;
            speak(`You are ${dist} kilometers away from your destination.`);
          } else {
            speak("Could not get route information.");
          }
        });
    }
  }, (err) => {
    console.error("Location error:", err);
    speak("Failed to get your current location.");
  });
}
