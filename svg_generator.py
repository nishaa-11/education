"""
SVG-based Animation Generator
Creates smooth, professional animations using SVG graphics and MoviePy
Each element is generated separately and composited
"""
import os
import numpy as np
from moviepy import VideoClip, AudioFileClip
from PIL import Image, ImageDraw
from gtts import gTTS
import math


class SVGAnimationGenerator:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.width = 1920
        self.height = 1080
        
    def generate_audio(self, text, filename="narration.mp3"):
        """Generate audio from text"""
        audio_path = os.path.join(self.output_dir, filename)
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(audio_path)
        return audio_path
    
    def create_gradient_background(self, color1, color2, duration):
        """Create smooth gradient background"""
        def make_frame(t):
            img = Image.new('RGBA', (self.width, self.height))
            pixels = img.load()
            
            for y in range(self.height):
                ratio = y / self.height
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                
                for x in range(self.width):
                    pixels[x, y] = (r, g, b, 255)
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=duration).set_opacity(1.0)
    
    def create_smooth_sun(self, duration, position=(300, 250), size=120):
        """Create animated sun with smooth rays"""
        def make_frame(t):
            img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            x, y = position
            
            # Pulsating effect
            pulse = 1 + 0.05 * math.sin(t * 2)
            current_size = max(10, int(size * pulse))
            
            # Draw glow layers
            for i in range(3):
                glow_size = max(10, current_size + i * 15)
                opacity = int(40 - i * 10)
                draw.ellipse([x - glow_size, y - glow_size, 
                            x + glow_size, y + glow_size],
                           fill=(255, 215, 0, opacity))
            
            # Main sun
            draw.ellipse([x - current_size, y - current_size,
                         x + current_size, y + current_size],
                        fill=(255, 223, 0, 255))
            
            # Rotating rays (fewer for performance)
            num_rays = 12
            rotation = t * 20
            for i in range(num_rays):
                angle = (i * 360 / num_rays + rotation) * math.pi / 180
                
                length = current_size + 50
                width = 6
                
                x1 = x + (current_size + 10) * math.cos(angle)
                y1 = y + (current_size + 10) * math.sin(angle)
                x2 = x + (current_size + length) * math.cos(angle)
                y2 = y + (current_size + length) * math.sin(angle)
                
                draw.line([int(x1), int(y1), int(x2), int(y2)], fill=(255, 215, 0, 255), width=width)
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=duration)
    
    def create_growing_plant(self, duration, position=(960, 900), max_height=400):
        """Create smooth growing plant with realistic leaves and flower"""
        def make_frame(t):
            img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            x, y = position
            
            # Growth progress (0 to 1)
            growth = min(1.0, t / (duration * 0.7))
            current_height = int(max_height * growth)
            
            # Gentle sway
            sway = math.sin(t * 1.5) * 8
            
            # Draw stem with gradient
            stem_segments = 20
            for i in range(stem_segments):
                seg_height = current_height / stem_segments
                seg_y = y - (i * seg_height)
                seg_x = x + sway * (i / stem_segments)
                
                # Stem color gradient (darker at bottom)
                green = 100 + int(55 * (i / stem_segments))
                
                if i < stem_segments - 1:
                    next_y = y - ((i + 1) * seg_height)
                    next_x = x + sway * ((i + 1) / stem_segments)
                    draw.line([seg_x, seg_y, next_x, next_y],
                            fill=(34, green, 34, 255), width=12)
            
            # Draw leaves at different heights
            if growth > 0.3:
                for leaf_data in [
                    {'height': 0.3, 'side': 'left', 'size': 80},
                    {'height': 0.5, 'side': 'right', 'size': 90},
                    {'height': 0.7, 'side': 'left', 'size': 85},
                ]:
                    if growth > leaf_data['height']:
                        leaf_y = y - current_height * leaf_data['height']
                        leaf_x = x + sway * leaf_data['height']
                        
                        # Leaf sway
                        leaf_sway = math.sin(t * 2 + leaf_data['height'] * 5) * 12
                        
                        if leaf_data['side'] == 'left':
                            offset_x = -leaf_sway - 20
                        else:
                            offset_x = leaf_sway + 20
                        
                        # Draw realistic leaf shape
                        leaf_size = leaf_data['size']
                        leaf_points = [
                            (int(leaf_x), int(leaf_y)),
                            (int(leaf_x + offset_x - leaf_size//3), int(leaf_y - leaf_size//2)),
                            (int(leaf_x + offset_x - leaf_size), int(leaf_y)),
                            (int(leaf_x + offset_x - leaf_size//3), int(leaf_y + leaf_size//2)),
                        ]
                        draw.polygon(leaf_points, fill=(50, 205, 50, 255))
                        
                        # Leaf vein
                        draw.line([leaf_x, leaf_y, leaf_x + offset_x - leaf_size, leaf_y],
                                fill=(34, 139, 34, 255), width=3)
            
            # Draw flower when fully grown
            if growth > 0.95:
                flower_x = x + sway
                flower_y = y - current_height
                
                # Flower animation
                bloom = min(1.0, (t - duration * 0.7) / (duration * 0.3))
                
                # Petals
                petal_colors = [(255, 105, 180), (255, 20, 147), (255, 182, 193), (255, 105, 180), (255, 20, 147)]
                num_petals = 5
                
                for i in range(num_petals):
                    angle = (i * 360 / num_petals + t * 20) * math.pi / 180
                    petal_dist = 25 * bloom
                    px = int(flower_x + petal_dist * math.cos(angle))
                    py = int(flower_y + petal_dist * math.sin(angle))
                    
                    petal_size = max(2, int(20 * bloom))
                    draw.ellipse([px - petal_size, py - petal_size,
                                px + petal_size, py + petal_size],
                               fill=petal_colors[i])
                
                # Flower center
                center_size = max(2, int(15 * bloom))
                draw.ellipse([int(flower_x) - center_size, int(flower_y) - center_size,
                            int(flower_x) + center_size, int(flower_y) + center_size],
                           fill=(255, 215, 0, 255))
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=duration)
    
    def create_floating_particles(self, duration, start_pos, end_pos, count=8, color=(100, 200, 255), label=""):
        """Create smooth floating particles with trails"""
        def make_frame(t):
            img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            for i in range(count):
                # Stagger particles
                offset = i * 0.15
                progress = min(1.0, (t + offset) / duration)
                
                if progress > 0:
                    # Sine wave motion
                    wave = math.sin(progress * math.pi * 2 + i) * 40
                    
                    x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress + wave
                    y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress
                    
                    # Particle glow
                    for glow in range(3):
                        size = 15 - glow * 5
                        opacity = int(200 - glow * 60)
                        draw.ellipse([x - size, y - size, x + size, y + size],
                                   fill=(*color, opacity))
                    
                    # Main particle
                    draw.ellipse([x - 8, y - 8, x + 8, y + 8], fill=(*color, 255))
                    
                    # Label on first particle
                    if i == 0 and label and progress > 0.3:
                        from PIL import ImageFont
                        try:
                            font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 32)
                        except:
                            font = ImageFont.load_default()
                        
                        draw.text((x + 20, y - 10), label, fill=(*color, 255), font=font)
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=duration)
    
    def create_text_overlay(self, text, duration, position='bottom', font_size=48):
        """Create smooth text overlay with fade in/out"""
        def make_frame(t):
            img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            from PIL import ImageFont
            try:
                font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Fade in/out
            fade_duration = 0.5
            if t < fade_duration:
                opacity = int(255 * (t / fade_duration))
            elif t > duration - fade_duration:
                opacity = int(255 * ((duration - t) / fade_duration))
            else:
                opacity = 255
            
            # Text position
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (self.width - text_width) // 2
            if position == 'top':
                y = 80
            elif position == 'bottom':
                y = self.height - text_height - 100
            else:
                y = (self.height - text_height) // 2
            
            # Text shadow
            for offset in range(1, 5):
                draw.text((x + offset, y + offset), text, fill=(0, 0, 0, opacity // 2), font=font)
            
            # Main text
            draw.text((x, y), text, fill=(255, 255, 255, opacity), font=font)
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=duration)
    
    def generate_photosynthesis_video(self, text, output_filename="photosynthesis.mp4"):
        """Generate photosynthesis video with separate composited elements"""
        print("Generating audio...")
        audio_path = self.generate_audio(text)
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration
        
        print("Creating visual elements...")
        
        # Background gradient (sky blue to light green)
        bg = self.create_gradient_background((135, 206, 250), (144, 238, 144), duration)
        
        # Sun
        sun = self.create_smooth_sun(duration, position=(300, 250), size=100)
        
        # Plant
        plant = self.create_growing_plant(duration, position=(960, 950), max_height=450)
        
        # CO2 particles (gray)
        co2 = self.create_floating_particles(duration, 
                                            start_pos=(200, 500),
                                            end_pos=(960, 600),
                                            count=6,
                                            color=(120, 120, 120),
                                            label="CO₂")
        
        # H2O particles (blue)
        h2o = self.create_floating_particles(duration,
                                            start_pos=(200, 900),
                                            end_pos=(960, 850),
                                            count=6,
                                            color=(0, 150, 255),
                                            label="H₂O")
        
        # O2 particles rising (light green)
        o2 = self.create_floating_particles(duration,
                                           start_pos=(960, 500),
                                           end_pos=(1400, 200),
                                           count=8,
                                           color=(144, 238, 144),
                                           label="O₂")
        
        # Glucose indicator
        glucose = self.create_floating_particles(duration,
                                                start_pos=(960, 600),
                                                end_pos=(1400, 600),
                                                count=4,
                                                color=(255, 165, 0),
                                                label="C₆H₁₂O₆")
        
        # Title
        title = self.create_text_overlay("Photosynthesis", duration, position='top', font_size=72)
        
        # Equation
        equation = self.create_text_overlay("6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂",
                                          duration, position='bottom', font_size=42)

        print("Compositing layers...")

        # Composite all layers - convert RGBA to RGB for MoviePy compatibility
        def convert_to_rgb(clip):
            """Convert RGBA frames to RGB"""
            def make_frame(t):
                frame = clip.get_frame(t)
                if frame.shape[2] == 4:  # RGBA
                    # Composite RGBA onto white background
                    rgb = frame[:, :, :3]
                    alpha = frame[:, :, 3:4] / 255.0
                    white_bg = np.ones_like(rgb) * 255
                    return (rgb * alpha + white_bg * (1 - alpha)).astype(np.uint8)
                return frame
            return VideoClip(make_frame, duration=clip.duration)
        
        # Convert all clips to RGB
        bg_rgb = convert_to_rgb(bg)
        
        # Composite layers one by one with proper alpha blending
        def composite_frame(t):
            """Composite all layers frame by frame"""
            # Start with background
            result = bg_rgb.get_frame(t).astype(np.float32)
            
            # Composite each layer
            for layer in [sun, co2, h2o, plant, o2, glucose, title, equation]:
                frame = layer.get_frame(t)
                if frame.shape[2] == 4:  # Has alpha
                    rgb = frame[:, :, :3].astype(np.float32)
                    alpha = frame[:, :, 3:4].astype(np.float32) / 255.0
                    result = rgb * alpha + result * (1 - alpha)
                else:
                    result = frame.astype(np.float32)
            
            return result.astype(np.uint8)
        
        video = VideoClip(composite_frame, duration=duration)
        video = video.set_audio(audio_clip)
        
        # Export
        output_path = os.path.join(self.output_dir, output_filename)
        print(f"Rendering final video to {output_path}...")
        video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac',
                             bitrate='3000k', preset='ultrafast', threads=4)
        
        print(f"✅ Video generated: {output_path}")
        return output_path
    
    def detect_content_type(self, text):
        """Detect content type"""
        text_lower = text.lower()

        # Photosynthesis detection - broader keywords
        photosynthesis_keywords = ['photosynthesis', 'plant', 'chlorophyll', 'leaf', 'leaves',
                                   'sunlight', 'carbon dioxide', 'co2', 'oxygen', 'o2',
                                   'glucose', 'green', 'sun', 'light energy']
        if any(word in text_lower for word in photosynthesis_keywords):
            return 'photosynthesis'

        return None
    
    def generate_video(self, text, output_filename="educational_video.mp4"):
        """Generate video based on content"""
        content_type = self.detect_content_type(text)
        
        if content_type == 'photosynthesis':
            return self.generate_photosynthesis_video(text, output_filename)
        else:
            # Fallback to basic generator
            print("Using fallback generator for unknown content type")
            from video_generator import VideoGenerator
            gen = VideoGenerator(self.output_dir)
            return gen.generate_video(text, output_filename)


if __name__ == "__main__":
    generator = SVGAnimationGenerator()
    
    text = """
    Photosynthesis is the process by which plants convert sunlight into energy.
    Plants absorb carbon dioxide from the air and water from the soil.
    Using light energy, they combine these to produce glucose and oxygen.
    The oxygen is released into the atmosphere for us to breathe.
    """
    
    generator.generate_video(text.strip(), "photosynthesis_pro.mp4")
