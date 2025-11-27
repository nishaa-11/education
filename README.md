# Educational Video Generator

A free, open-source educational video generator that creates videos from text input with automatic narration.

## Features
- Text-to-video generation
- Automatic voiceover using Google Text-to-Speech
- Customizable text animations and styling
- REST API for integration
- Simple web interface

## Tech Stack
- **Backend**: Python + Flask
- **Video Generation**: MoviePy
- **Text-to-Speech**: gTTS
- **Frontend**: HTML/CSS/JavaScript

## Installation

1. Clone the repository
2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. Enter your educational content and generate a video!

## API Endpoints

- `POST /generate` - Generate video from text
  - Body: `{"text": "Your educational content here"}`
  - Returns: Video file path

## License
MIT License - Free to use and modify
