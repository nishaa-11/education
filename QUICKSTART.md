# Quick Start Guide

## Installation

1. **Install Python** (3.8 or higher)
   - Download from [python.org](https://www.python.org/downloads/)

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   If you encounter issues with MoviePy on Windows, you may need to install ImageMagick:
   - Download from [imagemagick.org](https://imagemagick.org/script/download.php)

## Running the Application

### Option 1: Web Interface (Recommended)

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your browser and go to:
   ```
   http://localhost:5000
   ```

3. Enter your educational content and click "Generate Video"

4. Download your video when ready!

### Option 2: Python Script

Run the example script to generate sample videos:
```bash
python example.py
```

Videos will be saved in the `output/` folder.

### Option 3: Use as Python Module

```python
from video_generator import VideoGenerator

generator = VideoGenerator()
text = "Your educational content here"
video_path = generator.generate_video(text)
print(f"Video saved to: {video_path}")
```

## Customization

### Change Video Style

Edit `video_generator.py` and modify the `create_text_clip` method:

```python
# Change background color
bg_color='#1e3a8a'  # Dark blue (default)
# Try: '#2d3748' (dark gray), '#0f172a' (darker blue)

# Change text size
fontsize=45  # Default
# Try: 40 (smaller), 55 (larger)

# Change text color
color='white'  # Default
# Try: 'yellow', '#FFD700' (gold)
```

### Adjust Video Quality

Edit the `write_videofile` parameters in `video_generator.py`:

```python
final_video.write_videofile(
    output_path,
    fps=24,        # Frames per second (try 30 for smoother)
    codec='libx264',
    bitrate='5000k'  # Add this for higher quality
)
```

## Tips

- **Text Length**: Longer text = longer video. Keep it concise for best results.
- **Punctuation**: Use periods to split text into separate clips.
- **Processing Time**: Videos typically take 30-60 seconds to generate.
- **Audio Language**: Edit `video_generator.py` line 22 to change language:
  ```python
  tts = gTTS(text=text, lang='en', slow=False)
  # Change 'en' to 'es' (Spanish), 'fr' (French), etc.
  ```

## Troubleshooting

### "No module named 'moviepy'"
```bash
pip install moviepy
```

### "ffmpeg not found"
MoviePy requires ffmpeg. Install via:
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- **Mac**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

### Video generation is slow
- Normal! First run downloads models and caches them
- Subsequent generations are faster
- Consider shorter text for faster processing

### Audio/video out of sync
- This is rare but can happen with very long text
- Try splitting into multiple shorter videos

## API Reference

### POST /api/generate
Generate a video from text.

**Request:**
```json
{
  "text": "Your educational content here"
}
```

**Response:**
```json
{
  "success": true,
  "video_id": "uuid-here",
  "download_url": "/api/download/uuid-here"
}
```

### GET /api/download/{video_id}
Download the generated video file.

### GET /api/health
Check if the API is running.

## Advanced Features (Coming Soon)

- Multiple voice options
- Custom background images
- Animation effects
- Multiple language support
- Batch processing
- Custom fonts and colors via web UI

## License

MIT License - Free to use and modify for any purpose.
