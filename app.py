"""
Flask API Server for Educational Video Generator
Provides REST endpoints for video generation
Uses AI (Gemini) to generate animations for any topic
"""
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from manim_ai_generator import ManimAIGenerator
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Manim AI generator
try:
    generator = ManimAIGenerator()
    print("✅ Using AI-powered Manim generator with Gemini")
except Exception as e:
    print(f"❌ Failed to initialize generator: {e}")
    print("💡 Make sure GEMINI_API_KEY is set in .env file")
    generator = None

# Store generation status
generation_status = {}


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def generate_video():
    """
    Generate video from text input
    Body: {"text": "Your educational content here"}
    """
    try:
        if generator is None:
            return jsonify({'error': 'Generator not initialized. Check GEMINI_API_KEY in .env'}), 500
        
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        user_prompt = data['text'].strip()
        
        if not user_prompt:
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        if len(user_prompt) < 10:
            return jsonify({'error': 'Text is too short. Please provide at least 10 characters.'}), 400
        
        # Generate unique ID
        video_id = str(uuid.uuid4())
        
        # Update status
        generation_status[video_id] = {
            'status': 'processing',
            'created_at': datetime.now().isoformat()
        }
        
        # Generate video with full AI pipeline
        print(f"Starting video generation for ID: {video_id}")
        result = generator.generate_video(user_prompt, output_name=f"video_{video_id}")
        
        # Update status
        generation_status[video_id] = {
            'status': 'completed',
            'video_path': result['video_path'],
            'elaboration': result['elaboration'],
            'narration': result['narration'],
            'created_at': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'video_id': video_id,
            'message': 'Video generated successfully!',
            'download_url': f'/api/download/{video_id}',
            'elaboration': result['elaboration'],
            'narration': result['narration']
        }), 200
        
    except Exception as e:
        print(f"Error generating video: {str(e)}")
        return jsonify({'error': f'Failed to generate video: {str(e)}'}), 500


@app.route('/api/status/<video_id>', methods=['GET'])
def check_status(video_id):
    """Check the status of a video generation"""
    if video_id not in generation_status:
        return jsonify({'error': 'Video ID not found'}), 404
    
    return jsonify(generation_status[video_id]), 200


@app.route('/api/download/<video_id>', methods=['GET'])
def download_video(video_id):
    """Download generated video"""
    if video_id not in generation_status:
        return jsonify({'error': 'Video ID not found'}), 404
    
    status = generation_status[video_id]
    
    if status['status'] != 'completed':
        return jsonify({'error': 'Video is still processing'}), 400
    
    video_path = status['video_path']
    
    if not os.path.exists(video_path):
        return jsonify({'error': 'Video file not found'}), 404
    
    filename = os.path.basename(video_path)
    return send_file(
        video_path,
        mimetype='video/mp4',
        as_attachment=True,
        download_name=filename
    )


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Educational Video Generator API'
    }), 200


if __name__ == '__main__':
    print("Starting Educational Video Generator API...")
    print("Server running at http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000)
