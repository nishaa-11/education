"""
Three.js GPU-Accelerated Video Generator
Uses Puppeteer to render Three.js animations and capture frames
Much faster and higher quality than PIL
"""
import os
import subprocess
import json
from gtts import gTTS
from pathlib import Path


class ThreeJSVideoGenerator:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.html_path = Path(__file__).parent / "threejs_animation.html"
        
    def generate_audio(self, text, filename="narration.mp3"):
        """Generate audio from text"""
        audio_path = os.path.join(self.output_dir, filename)
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(audio_path)
        return audio_path
    
    def detect_content_type(self, text):
        """Detect content type"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['photosynthesis', 'plant', 'chlorophyll', 'leaf', 
                                                'sunlight', 'carbon dioxide', 'co2', 'oxygen']):
            return 'photosynthesis'
        
        return 'default'
    
    def render_threejs_video(self, animation_type, duration, output_path):
        """Render Three.js animation using Puppeteer and FFmpeg"""
        
        # Create Node.js script to capture frames
        capture_script = f"""
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {{
    const browser = await puppeteer.launch({{
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
    }});
    
    const page = await browser.newPage();
    await page.setViewport({{ width: 1920, height: 1080 }});
    
    const htmlPath = 'file:///' + path.resolve('{str(self.html_path).replace(chr(92), '/')}');
    const url = htmlPath + '?type={animation_type}&duration={duration}';
    
    console.log('Loading animation...');
    await page.goto(url, {{ waitUntil: 'networkidle0' }});
    
    console.log('Capturing frames...');
    const framesDir = '{self.output_dir}/frames';
    if (!fs.existsSync(framesDir)) {{
        fs.mkdirSync(framesDir, {{ recursive: true }});
    }}
    
    const fps = 30;
    const totalFrames = Math.floor({duration} * fps);
    
    for (let i = 0; i < totalFrames; i++) {{
        await page.screenshot({{
            path: `${{framesDir}}/frame_${{String(i).padStart(5, '0')}}.png`,
            type: 'png'
        }});
        
        // Wait for next frame
        await page.evaluate(() => new Promise(resolve => requestAnimationFrame(resolve)));
        
        if (i % 30 === 0) {{
            console.log(`Captured ${{i}}/${{totalFrames}} frames`);
        }}
    }}
    
    console.log('Frame capture complete!');
    await browser.close();
    
    console.log('Frames saved to:', framesDir);
}})();
"""
        
        # Save capture script
        capture_script_path = os.path.join(self.output_dir, "capture.js")
        with open(capture_script_path, 'w') as f:
            f.write(capture_script)
        
        print("Rendering Three.js animation...")
        print("Installing Node.js dependencies...")
        
        # Install dependencies
        subprocess.run(['npm', 'install'], cwd=Path(__file__).parent, shell=True, check=True)
        
        print("Capturing frames with Puppeteer...")
        # Run capture script
        subprocess.run(['node', capture_script_path], shell=True, check=True)
        
        print("Encoding video with FFmpeg...")
        # Combine frames with FFmpeg
        frames_pattern = os.path.join(self.output_dir, 'frames', 'frame_%05d.png')
        
        subprocess.run([
            'ffmpeg', '-y',
            '-framerate', '30',
            '-i', frames_pattern,
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '18',
            '-pix_fmt', 'yuv420p',
            output_path
        ], check=True)
        
        # Cleanup frames
        import shutil
        frames_dir = os.path.join(self.output_dir, 'frames')
        if os.path.exists(frames_dir):
            shutil.rmtree(frames_dir)
        
        return output_path
    
    def add_audio_to_video(self, video_path, audio_path, output_path):
        """Add audio track to video"""
        subprocess.run([
            'ffmpeg', '-y',
            '-i', video_path,
            '-i', audio_path,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-shortest',
            output_path
        ], check=True)
        
        # Remove temp video
        os.remove(video_path)
    
    def generate_video(self, text, output_filename="educational_video.mp4"):
        """Generate complete video"""
        print("🎬 Starting GPU-accelerated video generation...")
        
        # Generate audio
        print("📢 Generating narration...")
        audio_path = self.generate_audio(text)
        
        # Get audio duration
        from moviepy.editor import AudioFileClip
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration
        audio_clip.close()
        
        # Detect content type
        content_type = self.detect_content_type(text)
        print(f"🎨 Detected content type: {content_type}")
        
        # Render Three.js animation
        temp_video = os.path.join(self.output_dir, f"temp_{output_filename}")
        self.render_threejs_video(content_type, duration, temp_video)
        
        # Add audio
        print("🔊 Adding audio track...")
        output_path = os.path.join(self.output_dir, output_filename)
        self.add_audio_to_video(temp_video, audio_path, output_path)
        
        print(f"✅ Video generated: {output_path}")
        return output_path


if __name__ == "__main__":
    generator = ThreeJSVideoGenerator()
    
    text = """
    Photosynthesis is the process by which plants convert sunlight into energy.
    Plants absorb carbon dioxide from the air and water from the soil.
    Using light energy, they produce glucose and oxygen.
    """
    
    generator.generate_video(text.strip(), "photosynthesis_threejs.mp4")
