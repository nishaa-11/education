"""
AI-Powered Animation Generator
Uses Gemini API to generate custom animations for any topic
"""
import os
import json
from gtts import gTTS
from moviepy.editor import AudioFileClip, VideoClip
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import math
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AIAnimationGenerator:
    def __init__(self, output_dir="output", gemini_api_key=None):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.width = 1920
        self.height = 1080
        
        # Configure Gemini
        api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("Please set GEMINI_API_KEY environment variable or pass gemini_api_key parameter")
        
        model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        print(f"🤖 Using model: {model_name}")
        
    def generate_audio(self, text, filename="narration.mp3"):
        """Generate audio from text"""
        audio_path = os.path.join(self.output_dir, filename)
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(audio_path)
        return audio_path
    
    def generate_animation_code(self, topic):
        """Use Gemini to generate animation specifications"""
        prompt = f"""
You are an expert animation designer. Create a detailed animation specification for an educational video about: {topic}

Generate a JSON specification with the following structure:
{{
    "title": "Main title to display",
    "background": {{
        "type": "gradient",
        "color1": [R, G, B],
        "color2": [R, G, B]
    }},
    "elements": [
        {{
            "type": "shape",  // Options: "circle", "rectangle", "ellipse", "polygon"
            "name": "element name",
            "color": [R, G, B],
            "position": [x, y],  // 0-1920 for x, 0-1080 for y
            "size": [width, height],
            "animation": {{
                "type": "movement",  // Options: "movement", "rotation", "scale", "pulse", "none"
                "start": [x, y] or rotation_angle or scale_value,
                "end": [x, y] or rotation_angle or scale_value,
                "duration_ratio": 0.5  // 0-1, portion of total video
            }}
        }},
        {{
            "type": "particle_system",
            "name": "particle name",
            "color": [R, G, B],
            "count": 8,
            "start_pos": [x, y],
            "end_pos": [x, y],
            "label": "CO₂"
        }},
        {{
            "type": "text",
            "content": "Label text",
            "position": [x, y],
            "size": 36,
            "color": [R, G, B]
        }}
    ]
}}

Rules:
1. Keep it simple - max 5-8 elements
2. Use colors that make sense (sun=yellow, plants=green, water=blue, etc)
3. Position center is [960, 540]
4. Make animations smooth and educational
5. Include particle systems for molecular concepts
6. Add text labels for key elements

Return ONLY valid JSON, no other text.
"""
        
        print("🤖 Asking Gemini to design animation...")
        response = self.model.generate_content(prompt)
        
        # Extract JSON from response
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith('```'):
            response_text = response_text.split('```')[1]
            if response_text.startswith('json'):
                response_text = response_text[4:]
        
        spec = json.loads(response_text.strip())
        print("✅ Animation design received!")
        return spec
    
    def render_element(self, element, t, duration, draw):
        """Render a single element at time t"""
        
        if element['type'] == 'circle':
            x, y = element['position']
            radius = element['size'][0] // 2
            color = tuple(element['color'])
            
            # Apply animation
            if 'animation' in element:
                anim = element['animation']
                progress = min(1.0, t / (duration * anim.get('duration_ratio', 1.0)))
                
                if anim['type'] == 'pulse':
                    scale = 1 + 0.1 * math.sin(t * 3)
                    radius = int(radius * scale)
                elif anim['type'] == 'movement':
                    start_x, start_y = anim['start']
                    end_x, end_y = anim['end']
                    x = int(start_x + (end_x - start_x) * progress)
                    y = int(start_y + (end_y - start_y) * progress)
            
            # Draw glow
            for i in range(3):
                glow_radius = radius + i * 15
                opacity = max(20, 80 - i * 20)
                draw.ellipse([x - glow_radius, y - glow_radius,
                            x + glow_radius, y + glow_radius],
                           fill=(*color, opacity))
            
            # Main circle
            draw.ellipse([x - radius, y - radius, x + radius, y + radius],
                        fill=(*color, 255))
        
        elif element['type'] == 'rectangle':
            x, y = element['position']
            w, h = element['size']
            color = tuple(element['color'])
            
            # Apply animation
            if 'animation' in element and element['animation']['type'] == 'scale':
                anim = element['animation']
                progress = min(1.0, t / (duration * anim.get('duration_ratio', 1.0)))
                scale = anim['start'] + (anim['end'] - anim['start']) * progress
                w = int(w * scale)
                h = int(h * scale)
            
            draw.rectangle([x - w//2, y - h//2, x + w//2, y + h//2],
                         fill=(*color, 255))
        
        elif element['type'] == 'ellipse':
            x, y = element['position']
            w, h = element['size']
            color = tuple(element['color'])
            
            # Apply rotation
            rotation = 0
            if 'animation' in element and element['animation']['type'] == 'rotation':
                rotation = t * element['animation'].get('speed', 30)
            
            # For rotation, draw as polygon approximation
            points = []
            for i in range(20):
                angle = (i * 18 + rotation) * math.pi / 180
                px = x + w//2 * math.cos(angle)
                py = y + h//2 * math.sin(angle)
                points.append((int(px), int(py)))
            
            if len(points) > 2:
                draw.polygon(points, fill=(*color, 255))
        
        elif element['type'] == 'particle_system':
            color = tuple(element['color'])
            count = element['count']
            start_pos = element['start_pos']
            end_pos = element['end_pos']
            
            for i in range(count):
                offset = i * 0.15
                progress = min(1.0, (t + offset) / duration)
                
                if progress > 0:
                    wave = math.sin(progress * math.pi * 3 + i) * 50
                    x = int(start_pos[0] + (end_pos[0] - start_pos[0]) * progress + wave)
                    y = int(start_pos[1] + (end_pos[1] - start_pos[1]) * progress)
                    
                    # Particle with glow
                    for glow in range(3, 0, -1):
                        size = 10 + glow * 3
                        opacity = int(150 - glow * 40)
                        draw.ellipse([x-size, y-size, x+size, y+size],
                                   fill=(*color, opacity))
                    
                    draw.ellipse([x-8, y-8, x+8, y+8], fill=(*color, 255))
        
        elif element['type'] == 'text':
            try:
                font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", element['size'])
            except:
                font = ImageFont.load_default()
            
            x, y = element['position']
            color = tuple(element['color'])
            text = element['content']
            
            # Shadow
            draw.text((x + 2, y + 2), text, fill=(0, 0, 0, 150), font=font)
            # Main text
            draw.text((x, y), text, fill=(*color, 255), font=font)
    
    def create_animated_frame(self, spec, duration):
        """Create animation from specification"""
        def make_frame(t):
            # Background
            bg_img = Image.new('RGB', (self.width, self.height))
            pixels = bg_img.load()
            
            bg = spec['background']
            color1 = bg['color1']
            color2 = bg['color2']
            
            for y in range(self.height):
                ratio = y / self.height
                r = int(color1[0] + (color2[0] - color1[0]) * ratio)
                g = int(color1[1] + (color2[1] - color1[1]) * ratio)
                b = int(color1[2] + (color2[2] - color1[2]) * ratio)
                for x in range(self.width):
                    pixels[x, y] = (r, g, b)
            
            # Create RGBA overlay for elements
            overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Render all elements
            for element in spec['elements']:
                self.render_element(element, t, duration, draw)
            
            # Composite
            bg_img = bg_img.convert('RGBA')
            result = Image.alpha_composite(bg_img, overlay)
            
            return np.array(result.convert('RGB'))
        
        return VideoClip(make_frame, duration=duration)
    
    def create_text_overlay(self, title, text, duration):
        """Create text overlay"""
        sentences = [s.strip() + '.' for s in text.split('.') if s.strip()]
        
        def make_frame(t):
            img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            try:
                title_font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 80)
                text_font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 42)
            except:
                title_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
            
            # Title at top
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (self.width - title_width) // 2
            
            for offset in range(1, 5):
                draw.text((title_x + offset, 50 + offset), title, 
                         fill=(0, 0, 0, 100), font=title_font)
            draw.text((title_x, 50), title, fill=(255, 255, 255, 255), font=title_font)
            
            # Current sentence at bottom
            if sentences:
                sentence_duration = duration / len(sentences)
                sentence_idx = min(int(t / sentence_duration), len(sentences) - 1)
                current_text = sentences[sentence_idx]
                
                # Wrap text
                words = current_text.split()
                lines = []
                current_line = []
                
                for word in words:
                    current_line.append(word)
                    test_line = ' '.join(current_line)
                    bbox = draw.textbbox((0, 0), test_line, font=text_font)
                    if bbox[2] - bbox[0] > self.width - 200:
                        if len(current_line) > 1:
                            current_line.pop()
                            lines.append(' '.join(current_line))
                            current_line = [word]
                
                if current_line:
                    lines.append(' '.join(current_line))
                
                # Text box
                text_height = len(lines) * 55
                box_y = self.height - text_height - 80
                draw.rectangle([50, box_y - 20, self.width - 50, self.height - 40],
                             fill=(0, 0, 0, 180))
                
                # Text lines
                for i, line in enumerate(lines):
                    bbox = draw.textbbox((0, 0), line, font=text_font)
                    line_width = bbox[2] - bbox[0]
                    text_x = (self.width - line_width) // 2
                    text_y = box_y + i * 55
                    
                    draw.text((text_x + 2, text_y + 2), line, fill=(0, 0, 0, 200), font=text_font)
                    draw.text((text_x, text_y), line, fill=(255, 255, 255, 255), font=text_font)
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=duration)
    
    def generate_video(self, topic, text, output_filename="ai_generated.mp4"):
        """Generate video using AI-designed animations"""
        print(f"🎬 Generating video for: {topic}")
        
        # Generate audio
        print("📢 Generating narration...")
        audio_path = self.generate_audio(text)
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration
        
        # Get animation spec from Gemini
        spec = self.generate_animation_code(topic)
        
        print("🎨 Rendering animation...")
        # Create animation
        animation = self.create_animated_frame(spec, duration)
        
        # Create text overlay
        text_overlay = self.create_text_overlay(spec['title'], text, duration)
        
        # Composite
        def composite(t):
            anim_frame = animation.get_frame(t)
            text_frame = text_overlay.get_frame(t)
            
            # Alpha blend text over animation
            if text_frame.shape[2] == 4:
                rgb = text_frame[:, :, :3]
                alpha = text_frame[:, :, 3:4] / 255.0
                result = (rgb * alpha + anim_frame * (1 - alpha)).astype(np.uint8)
            else:
                result = anim_frame
            
            return result
        
        video = VideoClip(composite, duration=duration)
        video = video.set_audio(audio_clip)
        
        output_path = os.path.join(self.output_dir, output_filename)
        print(f"💾 Encoding video...")
        video.write_videofile(output_path, fps=24, codec='libx264',
                             preset='ultrafast', threads=4, audio_codec='aac')
        
        print(f"✅ Video generated: {output_path}")
        return output_path


if __name__ == "__main__":
    # Test
    generator = AIAnimationGenerator(gemini_api_key="YOUR_API_KEY_HERE")
    
    topic = "Water cycle"
    text = """
    The water cycle describes how water moves through Earth's systems.
    Water evaporates from oceans and lakes into the atmosphere.
    It condenses into clouds and falls as precipitation.
    The water then flows back to the oceans, completing the cycle.
    """
    
    generator.generate_video(topic, text.strip(), "water_cycle_ai.mp4")
