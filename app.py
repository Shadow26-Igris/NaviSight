from flask import Flask, render_template, jsonify, Response
from flask_cors import CORS

# Import Blueprints
from routes.voice import voice_bp
from routes.route import route_bp
from routes.vision import vision_bp

from main import get_latest_alert
from main import main_generator 

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(voice_bp)
app.register_blueprint(route_bp)
app.register_blueprint(vision_bp)

@app.route('/latest_alert')
def latest_alert():
    return jsonify({'alert': get_latest_alert()})

@app.route('/video_stream')
def video_stream():
    return Response(main_generator(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Home route
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
