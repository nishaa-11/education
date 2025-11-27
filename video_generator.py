"""
Video Generator Module
Generates educational videos from text input using MoviePy and gTTS
Creates animated visual elements based on content
"""
import os
from gtts import gTTS
from moviepy.editor import (
    AudioFileClip, CompositeVideoClip, 
    concatenate_videoclips, ColorClip, ImageClip, VideoClip
)
from PIL import Image, ImageDraw, ImageFont
import textwrap
import numpy as np
import math


class VideoGenerator:
    def __init__(self, output_dir="output"):
        """Initialize the video generator"""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Keywords that trigger specific animations
        self.animation_keywords = {
            'photosynthesis': ['plant', 'sun', 'leaf', 'chloroplast', 'light', 'energy'],
            'water': ['water', 'cycle', 'rain', 'evaporation', 'cloud', 'ocean', 'h2o'],
            'math': ['equation', 'number', 'calculate', 'formula', 'theorem', 'geometry'],
            'space': ['planet', 'star', 'orbit', 'galaxy', 'solar', 'gravity', 'universe'],
            'chemistry': ['atom', 'molecule', 'electron', 'chemical', 'reaction', 'element'],
            'biology': ['cell', 'dna', 'organism', 'bacteria', 'virus', 'protein'],
        }
        
    def generate_audio(self, text, filename="narration.mp3"):
        """Generate audio from text using gTTS"""
        audio_path = os.path.join(self.output_dir, filename)
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(audio_path)
        return audio_path
    
    def detect_content_type(self, text):
        """Detect what type of content to animate based on keywords"""
        text_lower = text.lower()
        for content_type, keywords in self.animation_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return content_type
        return 'default'
    
    def draw_sun(self, draw, x, y, radius, t, color='#FFD700'):
        """Draw animated sun with rays"""
        # Draw sun circle
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)
        
        # Draw animated rays
        num_rays = 12
        ray_length = radius * 0.6
        rotation = t * 50  # Rotation speed
        
        for i in range(num_rays):
            angle = (i * 360 / num_rays + rotation) * math.pi / 180
            x1 = x + (radius + 5) * math.cos(angle)
            y1 = y + (radius + 5) * math.sin(angle)
            x2 = x + (radius + ray_length + 5) * math.cos(angle)
            y2 = y + (radius + ray_length + 5) * math.sin(angle)
            draw.line([x1, y1, x2, y2], fill=color, width=3)
    
    def draw_plant(self, draw, x, y, height, t, growth_progress=1.0):
        """Draw animated plant with growth"""
        current_height = height * growth_progress
        
        # Stem
        stem_top = y - current_height
        draw.line([x, y, x, stem_top], fill='#228B22', width=6)
        
        # Leaves (with gentle sway)
        sway = math.sin(t * 2) * 5
        if growth_progress > 0.3:
            # Left leaf
            leaf_y = y - current_height * 0.6
            draw.ellipse([x-25+sway, leaf_y-15, x-5+sway, leaf_y+15], fill='#32CD32')
        if growth_progress > 0.5:
            # Right leaf
            leaf_y = y - current_height * 0.4
            draw.ellipse([x+5-sway, leaf_y-15, x+25-sway, leaf_y+15], fill='#32CD32')
        
        # Flower on top (only when fully grown)
        if growth_progress > 0.9:
            flower_y = stem_top
            # Petals
            petal_colors = ['#FF69B4', '#FF1493', '#FF69B4', '#FF1493']
            petal_size = 12
            for i in range(4):
                angle = (i * 90 + t * 30) * math.pi / 180
                px = x + petal_size * math.cos(angle)
                py = flower_y + petal_size * math.sin(angle)
                draw.ellipse([px-8, py-8, px+8, py+8], fill=petal_colors[i])
            # Center
            draw.ellipse([x-6, flower_y-6, x+6, flower_y+6], fill='#FFD700')
    
    def draw_water_drops(self, draw, t, width, height):
        """Draw animated water drops falling"""
        num_drops = 8
        for i in range(num_drops):
            # Stagger drops
            drop_offset = (t * 200 + i * 100) % height
            x = 100 + i * (width - 200) // num_drops
            y = drop_offset
            
            # Draw drop shape
            draw.ellipse([x-5, y-10, x+5, y+5], fill='#87CEEB')
            draw.ellipse([x-3, y-15, x+3, y-8], fill='#87CEEB')
    
    def draw_clouds(self, draw, t, width):
        """Draw animated moving clouds"""
        cloud_positions = [
            (150 + (t * 30) % width, 80),
            (400 + (t * 20) % width, 120),
            (700 + (t * 25) % width, 100)
        ]
        
        for cx, cy in cloud_positions:
            # Draw cloud as multiple circles
            cloud_color = '#E0E0E0'
            draw.ellipse([cx-40, cy-20, cx-10, cy+10], fill=cloud_color)
            draw.ellipse([cx-20, cy-30, cx+20, cy], fill=cloud_color)
            draw.ellipse([cx, cy-25, cx+30, cy+5], fill=cloud_color)
            draw.ellipse([cx+10, cy-20, cx+40, cy+10], fill=cloud_color)
    
    def draw_particles(self, draw, x, y, t, particle_type='energy'):
        """Draw animated particles (energy, CO2, O2, etc)"""
        num_particles = 6
        for i in range(num_particles):
            angle = (i * 60 + t * 100) * math.pi / 180
            distance = 30 + math.sin(t * 3 + i) * 10
            px = x + distance * math.cos(angle)
            py = y + distance * math.sin(angle)
            
            if particle_type == 'energy':
                color = '#FFD700'
            elif particle_type == 'co2':
                color = '#808080'
            else:
                color = '#00FF00'
            
            draw.ellipse([px-4, py-4, px+4, py+4], fill=color)
    
    def draw_atoms(self, draw, x, y, t, num_electrons=3):
        """Draw animated atom with orbiting electrons"""
        # Nucleus
        draw.ellipse([x-15, y-15, x+15, y+15], fill='#FF6347')
        
        # Orbiting electrons
        for i in range(num_electrons):
            orbit_radius = 40 + i * 15
            angle = (t * 120 + i * 120) * math.pi / 180
            ex = x + orbit_radius * math.cos(angle)
            ey = y + orbit_radius * math.sin(angle)
            draw.ellipse([ex-6, ey-6, ex+6, ey+6], fill='#4169E1')
            
            # Draw orbit path
            draw.ellipse([x-orbit_radius, y-orbit_radius, x+orbit_radius, y+orbit_radius], 
                        outline='#CCCCCC', width=1)
    
    def draw_dna_helix(self, draw, x, y, t, height=200):
        """Draw animated DNA double helix"""
        num_pairs = 15
        twist_speed = t * 2
        
        for i in range(num_pairs):
            # Calculate positions along helix
            progress = i / num_pairs
            y_pos = y - height/2 + progress * height
            
            # Sine wave for helix shape
            offset1 = math.sin(progress * 4 * math.pi + twist_speed) * 30
            offset2 = math.sin(progress * 4 * math.pi + twist_speed + math.pi) * 30
            
            x1 = x + offset1
            x2 = x + offset2
            
            # Draw base pairs
            draw.line([x1, y_pos, x2, y_pos], fill='#FF1493', width=2)
            
            # Draw backbone circles
            draw.ellipse([x1-4, y_pos-4, x1+4, y_pos+4], fill='#4169E1')
            draw.ellipse([x2-4, y_pos-4, x2+4, y_pos+4], fill='#FFD700')
    
    def draw_planets(self, draw, center_x, center_y, t):
        """Draw animated solar system"""
        # Sun at center
        draw.ellipse([center_x-25, center_y-25, center_x+25, center_y+25], fill='#FDB813')
        
        # Planets orbiting
        planets = [
            {'radius': 60, 'size': 8, 'color': '#8B7355', 'speed': 2},
            {'radius': 100, 'size': 12, 'color': '#4169E1', 'speed': 1.5},
            {'radius': 140, 'size': 10, 'color': '#DC143C', 'speed': 1},
        ]
        
        for planet in planets:
            angle = (t * 50 * planet['speed']) * math.pi / 180
            px = center_x + planet['radius'] * math.cos(angle)
            py = center_y + planet['radius'] * math.sin(angle)
            
            # Draw orbit path
            draw.ellipse([center_x - planet['radius'], center_y - planet['radius'],
                         center_x + planet['radius'], center_y + planet['radius']],
                        outline='#CCCCCC', width=1)
            
            # Draw planet
            size = planet['size']
            draw.ellipse([px-size, py-size, px+size, py+size], fill=planet['color'])
    
    def create_text_clip(self, text, duration, fontsize=50, color='white', bg_color='#1e3a8a'):
        """Create animated text clip with visual elements based on content"""
        width, height = 1280, 720
        
        # Detect content type
        content_type = self.detect_content_type(text)
        
        # Try to load a font
        try:
            font = ImageFont.truetype("arial.ttf", fontsize)
        except:
            try:
                font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", fontsize)
            except:
                font = ImageFont.load_default()
        
        # Wrap text (shorter for more animation space)
        wrapped_text = '\n'.join(textwrap.wrap(text, width=30))
        
        def make_frame(t):
            """Generate frame at time t with content-aware animations"""
            # Create background gradient
            img = Image.new('RGB', (width, height), self._hex_to_rgb(bg_color))
            draw = ImageDraw.Draw(img)
            
            # Draw animated elements based on content type
            if content_type == 'photosynthesis':
                # Draw sun
                self.draw_sun(draw, 1050, 150, 50, t)
                # Draw plant with growth animation
                growth = min(1.0, t / (duration * 0.6))
                self.draw_plant(draw, 200, 600, 250, t, growth)
                # Draw energy particles around plant
                self.draw_particles(draw, 200, 450, t, 'energy')
                # Draw CO2 and O2 molecules
                self.draw_particles(draw, 350, 300, t, 'co2')
                self.draw_particles(draw, 450, 300, t, 'o2')
                
            elif content_type == 'water':
                # Draw clouds
                self.draw_clouds(draw, t, width)
                # Draw falling rain
                self.draw_water_drops(draw, t, width, height)
                # Draw ocean waves at bottom
                wave_height = 50
                for i in range(0, width, 20):
                    wave_y = height - 100 + math.sin((i + t * 100) * 0.02) * 15
                    draw.ellipse([i-10, wave_y-10, i+10, wave_y+10], fill='#4169E1')
                    
            elif content_type == 'chemistry':
                # Draw animated atoms
                self.draw_atoms(draw, 250, 300, t, 3)
                self.draw_atoms(draw, 550, 300, t, 2)
                # Draw connecting bonds
                draw.line([265, 300, 535, 300], fill='#FFFFFF', width=3)
                
            elif content_type == 'biology':
                # Draw DNA helix
                self.draw_dna_helix(draw, 200, 360, t, 400)
                # Draw cell structure
                cell_x, cell_y = 950, 350
                draw.ellipse([cell_x-80, cell_y-80, cell_x+80, cell_y+80], 
                           outline='#32CD32', width=3)
                # Nucleus
                draw.ellipse([cell_x-30, cell_y-30, cell_x+30, cell_y+30], fill='#9370DB')
                
            elif content_type == 'space':
                # Draw solar system
                self.draw_planets(draw, 250, 350, t)
                # Draw stars
                for i in range(30):
                    star_x = (i * 137 + int(t * 20)) % width
                    star_y = (i * 211) % (height - 200)
                    brightness = int(200 + 55 * math.sin(t * 3 + i))
                    draw.ellipse([star_x-2, star_y-2, star_x+2, star_y+2], 
                               fill=(brightness, brightness, brightness))
                    
            elif content_type == 'math':
                # Draw geometric shapes with animation
                center_x, center_y = 250, 350
                rotation = t * 30
                
                # Rotating triangle
                angles = [0, 120, 240]
                triangle_points = []
                for angle in angles:
                    rad = (angle + rotation) * math.pi / 180
                    x = center_x + 80 * math.cos(rad)
                    y = center_y + 80 * math.sin(rad)
                    triangle_points.extend([x, y])
                draw.polygon(triangle_points, outline='#FFD700', width=3)
                
                # Floating numbers
                numbers = ['π', 'Σ', '∫', '√', '∞']
                for i, num in enumerate(numbers):
                    num_x = 800 + math.sin(t + i) * 50
                    num_y = 200 + i * 80 + math.cos(t * 2 + i) * 20
                    draw.text((num_x, num_y), num, font=font, fill='#FFD700')
            
            # Animation parameters for text
            fade_duration = 0.5
            if t < fade_duration:
                opacity = int(255 * (t / fade_duration))
            else:
                opacity = 255
            
            # Calculate text position (bottom half of screen)
            try:
                bbox = draw.textbbox((0, 0), wrapped_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            except:
                text_width = 400
                text_height = 100
            
            x = (width - text_width) // 2
            y = height - text_height - 80
            
            # Draw text background for readability
            padding = 20
            draw.rectangle([x - padding, y - padding, 
                          x + text_width + padding, y + text_height + padding],
                         fill=(0, 0, 0, 180))
            
            # Draw text
            draw.text((x, y), wrapped_text, font=font, fill='white', align='center')
            
            return np.array(img)
        
        # Create VideoClip from make_frame function
        clip = VideoClip(make_frame, duration=duration)
        
        return clip
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def create_transition_clip(self, duration=0.3):
        """Create a transition effect between clips"""
        width, height = 1280, 720
        
        def make_frame(t):
            # Create a gradient fade effect
            progress = t / duration
            darkness = int(50 * progress)
            img = Image.new('RGB', (width, height), (darkness, darkness, darkness))
            return np.array(img)
        
        from moviepy.editor import VideoClip
        return VideoClip(make_frame, duration=duration)
    
    def generate_video(self, text, output_filename="educational_video.mp4"):
        """Generate complete animated video from text"""
        print("Generating audio narration...")
        audio_path = self.generate_audio(text)
        
        print("Loading audio...")
        audio_clip = AudioFileClip(audio_path)
        audio_duration = audio_clip.duration
        
        print("Creating animated video clips...")
        # Split text into sentences for better visual pacing
        sentences = [s.strip() + '.' for s in text.split('.') if s.strip()]
        
        if not sentences:
            sentences = [text]
        
        # Calculate duration per sentence (with transition time)
        transition_duration = 0.2
        content_duration = audio_duration - (len(sentences) - 1) * transition_duration
        duration_per_sentence = content_duration / len(sentences)
        
        # Create video clips for each sentence with animations
        clips = []
        colors = ['white', 'white', '#FFD700', 'white']  # Vary colors for interest
        bg_colors = ['#1e3a8a', '#2d3748', '#1e3a8a', '#2563eb']  # Vary backgrounds
        
        for i, sentence in enumerate(sentences):
            # Create animated text clip
            clip = self.create_text_clip(
                sentence, 
                duration=duration_per_sentence,
                fontsize=45,
                color=colors[i % len(colors)],
                bg_color=bg_colors[i % len(bg_colors)]
            )
            clips.append(clip)
            
            # Add transition between clips (except after last clip)
            if i < len(sentences) - 1:
                transition = self.create_transition_clip(transition_duration)
                clips.append(transition)
        
        print("Concatenating animated clips...")
        final_video = concatenate_videoclips(clips, method="compose")
        
        # Add audio
        final_video = final_video.set_audio(audio_clip)
        
        # Export video
        output_path = os.path.join(self.output_dir, output_filename)
        print(f"Rendering animated video to {output_path}...")
        final_video.write_videofile(
            output_path,
            fps=30,  # Higher FPS for smoother animations
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            preset='medium'
        )
        
        print("Video generation complete!")
        return output_path


# Example usage
if __name__ == "__main__":
    generator = VideoGenerator()
    
    sample_text = """
    Welcome to this educational video. 
    Today we will learn about photosynthesis. 
    Photosynthesis is the process by which plants convert sunlight into energy. 
    This process is essential for life on Earth.
    """
    
    video_path = generator.generate_video(sample_text.strip())
    print(f"Video saved to: {video_path}")
