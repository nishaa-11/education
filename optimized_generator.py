"""
Optimized Animation Generator
Uses pre-rendered sprite sheets and MoviePy for fast, high-quality animations
No external dependencies beyond Python packages
"""
import os
import numpy as np
from moviepy import VideoClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFilter
from gtts import gTTS
import math


class OptimizedVideoGenerator:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.width = 1920
        self.height = 1080
        
        # Pre-calculate and cache animations
        self.animation_cache = {}
        
    def generate_audio(self, text, filename="narration.mp3"):
        """Generate audio"""
        audio_path = os.path.join(self.output_dir, filename)
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(audio_path)
        return audio_path
    
    def create_optimized_sun(self, duration):
        """Optimized sun with glow - pre-rendered"""
        print("Pre-rendering sun animation...")
        
        # Pre-render sun at different rotation angles (30 frames)
        cached_frames = []
        for frame_idx in range(30):
            img = Image.new('RGBA', (600, 600), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            rotation = frame_idx * 12  # 360/30
            
            # Sun glow (gradient circles)
            for i in range(5, 0, -1):
                size = 120 + i * 25
                opacity = max(20, 80 - i * 15)
                draw.ellipse([300-size, 300-size, 300+size, 300+size],
                           fill=(255, 215, 0, opacity))
            
            # Main sun
            draw.ellipse([180, 180, 420, 420], fill=(255, 223, 0, 255))
            
            # Rays
            for i in range(12):
                angle = (i * 30 + rotation) * math.pi / 180
                x1 = 300 + 130 * math.cos(angle)
                y1 = 300 + 130 * math.sin(angle)
                x2 = 300 + 200 * math.cos(angle)
                y2 = 300 + 200 * math.sin(angle)
                draw.line([x1, y1, x2, y2], fill=(255, 215, 0, 255), width=10)
            
            # Apply blur for smoothness
            img = img.filter(ImageFilter.GaussianBlur(radius=2))
            cached_frames.append(np.array(img))
        
        def make_frame(t):
            # Use cached frame (loop through 30 frames)
            frame_idx = int((t * 10) % 30)  # 10 fps animation loop
            
            # Create full canvas
            canvas = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
            sun_frame = Image.fromarray(cached_frames[frame_idx])
            canvas.paste(sun_frame, (100, 50), sun_frame)
            
            return np.array(canvas)
        
        return VideoClip(make_frame, duration=duration)
    
    def create_optimized_plant(self, duration):
        """Optimized growing plant"""
        print("Pre-rendering plant animation...")
        
        def make_frame(t):
            img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Growth progress
            growth = min(1.0, t / (duration * 0.6))
            height = int(500 * growth)
            
            if height < 10:
                return np.array(img)
            
            # Sway
            sway = math.sin(t * 1.5) * 15 * growth
            
            x, y = self.width // 2, self.height - 100
            
            # Stem (thick line with segments for smoothness)
            segments = max(10, height // 20)
            for i in range(segments):
                seg_y = y - (i * height / segments)
                seg_x = x + sway * (i / segments)
                
                if i < segments - 1:
                    next_y = y - ((i + 1) * height / segments)
                    next_x = x + sway * ((i + 1) / segments)
                    
                    # Draw thick stem
                    for thickness in range(15, 0, -2):
                        alpha = int(255 * (thickness / 15))
                        draw.line([seg_x, seg_y, next_x, next_y],
                                fill=(34, 139, 34, alpha), width=thickness)
            
            # Leaves (only when grown enough)
            if growth > 0.4:
                for leaf_pos, side in [(0.4, -1), (0.6, 1), (0.75, -1)]:
                    if growth > leaf_pos:
                        leaf_y = y - height * leaf_pos
                        leaf_x = x + sway * leaf_pos
                        leaf_sway = math.sin(t * 2 + leaf_pos * 5) * 20
                        
                        # Leaf shape
                        offset = side * (70 + leaf_sway)
                        points = [
                            (int(leaf_x), int(leaf_y)),
                            (int(leaf_x + offset), int(leaf_y - 40)),
                            (int(leaf_x + offset * 1.5), int(leaf_y)),
                            (int(leaf_x + offset), int(leaf_y + 40)),
                        ]
                        draw.polygon(points, fill=(50, 205, 50, 255))
                        draw.line([leaf_x, leaf_y, leaf_x + offset * 1.5, leaf_y],
                                fill=(34, 139, 34, 255), width=3)
            
            # Flower (when fully grown)
            if growth > 0.95:
                flower_x = x + sway
                flower_y = y - height
                bloom = min(1.0, (t - duration * 0.6) / (duration * 0.3))
                
                # Petals
                colors = [(255, 105, 180), (255, 20, 147), (255, 182, 193)]
                for i in range(6):
                    angle = (i * 60 + t * 30) * math.pi / 180
                    petal_x = flower_x + 40 * bloom * math.cos(angle)
                    petal_y = flower_y + 40 * bloom * math.sin(angle)
                    size = int(30 * bloom)
                    if size > 2:
                        draw.ellipse([petal_x-size, petal_y-size, petal_x+size, petal_y+size],
                                   fill=colors[i % 3])
                
                # Center
                center_size = int(20 * bloom)
                if center_size > 2:
                    draw.ellipse([flower_x-center_size, flower_y-center_size,
                                flower_x+center_size, flower_y+center_size],
                               fill=(255, 215, 0, 255))
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=duration)
    
    def create_particle_system(self, duration, start, end, color, count=15, label=""):
        """Optimized particle system"""
        def make_frame(t):
            img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            for i in range(count):
                offset = i * 0.1
                progress = min(1.0, (t + offset) / duration)
                
                if progress > 0:
                    # Smooth bezier-like curve
                    wave = math.sin(progress * math.pi * 3 + i) * 60
                    
                    x = int(start[0] + (end[0] - start[0]) * progress + wave)
                    y = int(start[1] + (end[1] - start[1]) * progress)
                    
                    # Particle with glow
                    for glow in range(3, 0, -1):
                        size = 12 + glow * 4
                        opacity = int(150 - glow * 40)
                        draw.ellipse([x-size, y-size, x+size, y+size],
                                   fill=(*color, opacity))
                    
                    draw.ellipse([x-10, y-10, x+10, y+10], fill=(*color, 255))
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=duration)
    
    def create_text_overlay(self, text, duration):
        """Create text overlay with title and narration"""
        from PIL import ImageFont
        
        # Split text into sentences
        sentences = [s.strip() + '.' for s in text.split('.') if s.strip()]
        
        def make_frame(t):
            img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            try:
                title_font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 80)
                text_font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 48)
            except:
                title_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
            
            # Title at top (always visible)
            title = "Photosynthesis"
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (self.width - title_width) // 2
            
            # Shadow
            for offset in range(1, 6):
                draw.text((title_x + offset, 60 + offset), title, 
                         fill=(0, 0, 0, 100), font=title_font)
            # Main title
            draw.text((title_x, 60), title, fill=(255, 255, 255, 255), font=title_font)
            
            # Current sentence at bottom (rotates through sentences)
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
                
                # Draw text box background
                text_height = len(lines) * 60
                box_y = self.height - text_height - 80
                draw.rectangle([50, box_y - 20, self.width - 50, self.height - 40],
                             fill=(0, 0, 0, 180))
                
                # Draw text lines
                for i, line in enumerate(lines):
                    bbox = draw.textbbox((0, 0), line, font=text_font)
                    line_width = bbox[2] - bbox[0]
                    text_x = (self.width - line_width) // 2
                    text_y = box_y + i * 60
                    
                    # Shadow
                    draw.text((text_x + 2, text_y + 2), line, 
                             fill=(0, 0, 0, 200), font=text_font)
                    # Main text
                    draw.text((text_x, text_y), line, 
                             fill=(255, 255, 255, 255), font=text_font)
            
            # Labels for elements (minimal)
            label_font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 36) if title_font != ImageFont.load_default() else text_font
            
            # Fade in labels after 2 seconds
            if t > 2:
                label_alpha = min(255, int((t - 2) * 127))
                
                # Sun label
                draw.text((150, 380), "Sunlight", fill=(255, 255, 255, label_alpha), font=label_font)
                
                # CO2 arrow
                if t > 3:
                    draw.text((250, 520), "CO₂ →", fill=(200, 200, 200, label_alpha), font=label_font)
                
                # O2 arrow
                if t > 4:
                    draw.text((1200, 300), "← O₂", fill=(144, 238, 144, label_alpha), font=label_font)
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=duration)
    
    def generate_photosynthesis_video(self, text, output_filename):
        """Generate optimized video"""
        print("🎬 Generating audio...")
        audio_path = self.generate_audio(text)
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration
        
        print("🎨 Creating optimized animations...")
        
        # Background gradient
        bg_img = Image.new('RGB', (self.width, self.height))
        pixels = bg_img.load()
        for y in range(self.height):
            ratio = y / self.height
            r = int(135 + (144 - 135) * ratio)
            g = int(206 + (238 - 206) * ratio)
            b = int(250 + (144 - 250) * ratio)
            for x in range(self.width):
                pixels[x, y] = (r, g, b)
        
        bg_array = np.array(bg_img)
        
        # Create all elements (fewer particles)
        sun = self.create_optimized_sun(duration)
        plant = self.create_optimized_plant(duration)
        co2 = self.create_particle_system(duration, (300, 520), (self.width//2, 600), 
                                         (120, 120, 120), count=6)  # Reduced from 12
        o2 = self.create_particle_system(duration, (self.width//2, 400), (1400, 280),
                                        (144, 238, 144), count=8)  # Reduced from 15
        
        # Text overlay
        text_layer = self.create_text_overlay(text, duration)
        
        print("🎞️ Compositing and rendering...")
        
        # Manual compositing with alpha blending
        def composite(t):
            result = bg_array.copy()
            
            for layer in [sun, co2, plant, o2, text_layer]:
                frame = layer.get_frame(t)
                if frame.shape[2] == 4:
                    rgb = frame[:, :, :3]
                    alpha = frame[:, :, 3:4] / 255.0
                    result = (rgb * alpha + result * (1 - alpha)).astype(np.uint8)
            
            return result
        
        video = VideoClip(composite, duration=duration)
        video = video.set_audio(audio_clip)
        
        output_path = os.path.join(self.output_dir, output_filename)
        print("💾 Encoding video...")
        video.write_videofile(output_path, fps=24, codec='libx264',
                             preset='ultrafast', threads=4, audio_codec='aac')
        
        print(f"✅ Done: {output_path}")
        return output_path
    
    def detect_content_type(self, text):
        text_lower = text.lower()
        if any(w in text_lower for w in ['photosynthesis', 'plant', 'sun', 'co2', 'oxygen', 'leaf']):
            return 'photosynthesis'
        return None
    
    def generate_video(self, text, output_filename="video.mp4"):
        content_type = self.detect_content_type(text)
        
        if content_type == 'photosynthesis':
            return self.generate_photosynthesis_video(text, output_filename)
        else:
            # Fallback
            from video_generator import VideoGenerator
            gen = VideoGenerator(self.output_dir)
            return gen.generate_video(text, output_filename)


if __name__ == "__main__":
    gen = OptimizedVideoGenerator()
    text = "Photosynthesis is how plants convert sunlight into energy using carbon dioxide and water to produce glucose and oxygen."
    gen.generate_video(text, "test.mp4")
