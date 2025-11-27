"""
Manim-based Video Generator
Uses Manim Community Edition for professional animated educational videos
"""
import os
from manim import *
from gtts import gTTS
import tempfile
import shutil


class PhotosynthesisScene(Scene):
    def construct(self):
        # Title
        title = Text("Photosynthesis", font_size=60, color=YELLOW)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP))
        
        # Create sun
        sun = Circle(radius=0.8, color=YELLOW, fill_opacity=1)
        sun.to_edge(UL).shift(DOWN * 0.5)
        
        # Sun rays
        rays = VGroup(*[
            Line(sun.get_center(), sun.get_center() + 1.5 * np.array([np.cos(angle), np.sin(angle), 0]))
            for angle in np.linspace(0, 2*PI, 12)
        ]).set_color(YELLOW)
        
        self.play(FadeIn(sun), Create(rays))
        self.play(Rotate(rays, PI/6), run_time=2, rate_func=linear)
        
        # Create plant
        stem = Line(DOWN * 2, UP * 0.5, color=GREEN, stroke_width=8)
        leaf1 = Ellipse(width=0.8, height=0.4, color=GREEN, fill_opacity=1).move_to(stem.get_center() + LEFT * 0.5)
        leaf2 = Ellipse(width=0.8, height=0.4, color=GREEN, fill_opacity=1).move_to(stem.get_center() + RIGHT * 0.5)
        plant = VGroup(stem, leaf1, leaf2).shift(DOWN * 0.5)
        
        self.play(GrowFromPoint(plant, plant.get_bottom()))
        
        # CO2 molecules
        co2_group = VGroup()
        for i in range(3):
            co2 = Text("CO₂", font_size=24, color=GRAY)
            co2.move_to(LEFT * 4 + UP * (1 - i))
            co2_group.add(co2)
        
        self.play(FadeIn(co2_group))
        self.play(co2_group.animate.move_to(plant.get_top()), run_time=2)
        
        # Water molecules
        h2o_group = VGroup()
        for i in range(3):
            h2o = Text("H₂O", font_size=24, color=BLUE)
            h2o.move_to(LEFT * 4 + DOWN * (1 + i * 0.5))
            h2o_group.add(h2o)
        
        self.play(FadeIn(h2o_group))
        self.play(h2o_group.animate.move_to(plant.get_bottom()), run_time=2)
        
        # Light energy
        light_arrows = VGroup(*[
            Arrow(sun.get_center(), plant.get_top() + UP * 0.3, color=YELLOW)
            for _ in range(3)
        ])
        self.play(Create(light_arrows), run_time=1)
        
        # Glucose production
        glucose = Text("C₆H₁₂O₆", font_size=30, color=ORANGE)
        glucose.next_to(plant, RIGHT * 2)
        
        # Oxygen release
        o2_group = VGroup()
        for i in range(4):
            o2 = Text("O₂", font_size=24, color=GREEN_A)
            o2.move_to(plant.get_top() + RIGHT * (1 + i * 0.5) + UP * 0.5)
            o2_group.add(o2)
        
        self.play(FadeIn(glucose), FadeIn(o2_group))
        self.play(o2_group.animate.shift(UP * 2), run_time=2)
        
        # Summary equation (using Text instead of MathTex to avoid LaTeX dependency)
        equation = Text(
            "6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂",
            font_size=32,
            color=WHITE
        ).to_edge(DOWN)
        
        self.play(Write(equation))
        self.wait(2)


class WaterCycleScene(Scene):
    def construct(self):
        title = Text("The Water Cycle", font_size=60, color=BLUE)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP))
        
        # Ocean
        ocean = Rectangle(width=14, height=2, color=BLUE, fill_opacity=0.8)
        ocean.to_edge(DOWN, buff=0)
        ocean_label = Text("Ocean", font_size=24).move_to(ocean.get_center())
        
        self.play(FadeIn(ocean), Write(ocean_label))
        
        # Sun
        sun = Circle(radius=0.6, color=YELLOW, fill_opacity=1)
        sun.to_edge(UR)
        self.play(FadeIn(sun))
        
        # Evaporation
        water_particles = VGroup()
        for i in range(8):
            particle = Dot(color=BLUE_A, radius=0.08)
            particle.move_to(ocean.get_top() + RIGHT * (i - 4) * 0.8)
            water_particles.add(particle)
        
        self.play(FadeIn(water_particles))
        self.play(water_particles.animate.shift(UP * 3), run_time=2)
        
        evap_label = Text("Evaporation", font_size=24, color=BLUE)
        evap_label.next_to(ocean, RIGHT, buff=1).shift(UP)
        self.play(Write(evap_label))
        
        # Cloud formation
        cloud = Ellipse(width=3, height=1, color=WHITE, fill_opacity=0.9)
        cloud.move_to(UP * 2 + LEFT * 2)
        
        self.play(
            Transform(water_particles, cloud),
            FadeOut(evap_label)
        )
        
        cond_label = Text("Condensation", font_size=24, color=WHITE)
        cond_label.next_to(cloud, UP)
        self.play(Write(cond_label))
        self.wait(1)
        self.play(FadeOut(cond_label))
        
        # Precipitation (rain)
        rain_drops = VGroup()
        for i in range(10):
            drop = Line(ORIGIN, DOWN * 0.3, color=BLUE, stroke_width=3)
            drop.move_to(cloud.get_bottom() + RIGHT * (i - 5) * 0.4)
            rain_drops.add(drop)
        
        precip_label = Text("Precipitation", font_size=24, color=BLUE)
        precip_label.next_to(cloud, RIGHT, buff=1)
        
        self.play(Create(rain_drops), Write(precip_label))
        self.play(rain_drops.animate.shift(DOWN * 3), run_time=2)
        self.play(FadeOut(rain_drops), FadeOut(precip_label))
        
        # Collection
        collection_arrow = Arrow(ocean.get_top() + RIGHT * 3, ocean.get_center() + RIGHT * 3, color=BLUE)
        collect_label = Text("Collection", font_size=24, color=BLUE)
        collect_label.next_to(collection_arrow, RIGHT)
        
        self.play(Create(collection_arrow), Write(collect_label))
        self.wait(2)


class DNAScene(Scene):
    def construct(self):
        title = Text("DNA Structure", font_size=60, color=PURPLE)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP))
        
        # Create DNA double helix
        helix_points_1 = []
        helix_points_2 = []
        base_pairs = []
        
        t_values = np.linspace(0, 4*PI, 40)
        for t in t_values:
            x = t - 2*PI
            y1 = np.sin(t)
            y2 = np.sin(t + PI)
            helix_points_1.append([x, y1, 0])
            helix_points_2.append([x, y2, 0])
        
        # Draw the two strands
        strand1 = VMobject(color=BLUE)
        strand1.set_points_smoothly(helix_points_1)
        
        strand2 = VMobject(color=RED)
        strand2.set_points_smoothly(helix_points_2)
        
        # Base pairs connecting strands
        base_pair_group = VGroup()
        for i in range(0, len(helix_points_1), 2):
            line = Line(helix_points_1[i], helix_points_2[i], color=YELLOW, stroke_width=2)
            base_pair_group.add(line)
        
        dna = VGroup(strand1, strand2, base_pair_group)
        
        self.play(Create(strand1), Create(strand2), run_time=3)
        self.play(Create(base_pair_group), run_time=2)
        
        # Rotate the DNA
        self.play(Rotate(dna, PI/2, axis=UP), run_time=3)
        
        # Labels
        label1 = Text("Sugar-Phosphate\nBackbone", font_size=20, color=BLUE)
        label1.to_edge(LEFT).shift(UP)
        
        label2 = Text("Base Pairs:\nA-T, G-C", font_size=20, color=YELLOW)
        label2.to_edge(RIGHT).shift(UP)
        
        self.play(Write(label1), Write(label2))
        self.wait(2)


class SolarSystemScene(Scene):
    def construct(self):
        title = Text("Solar System", font_size=60, color=YELLOW)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP))
        
        # Sun
        sun = Circle(radius=0.5, color=YELLOW, fill_opacity=1)
        sun.move_to(ORIGIN)
        self.play(FadeIn(sun))
        
        # Planets
        planets_data = [
            {"name": "Mercury", "radius": 0.15, "orbit": 1.5, "color": GRAY, "speed": 2},
            {"name": "Venus", "radius": 0.2, "orbit": 2, "color": ORANGE, "speed": 1.5},
            {"name": "Earth", "radius": 0.2, "orbit": 2.5, "color": BLUE, "speed": 1},
            {"name": "Mars", "radius": 0.18, "orbit": 3, "color": RED, "speed": 0.8},
        ]
        
        orbits = VGroup()
        planets = VGroup()
        
        for p_data in planets_data:
            # Orbit path
            orbit = Circle(radius=p_data["orbit"], color=WHITE, stroke_width=1)
            orbit.move_to(ORIGIN)
            orbits.add(orbit)
            
            # Planet
            planet = Circle(radius=p_data["radius"], color=p_data["color"], fill_opacity=1)
            planet.move_to(RIGHT * p_data["orbit"])
            planets.add(planet)
        
        self.play(Create(orbits))
        self.play(FadeIn(planets))
        
        # Animate orbits
        def update_planet(mob, dt, orbit_radius, speed):
            angle = dt * speed
            mob.rotate(angle, about_point=ORIGIN)
        
        for i, planet in enumerate(planets):
            planet.add_updater(
                lambda m, dt, r=planets_data[i]["orbit"], s=planets_data[i]["speed"]: 
                update_planet(m, dt, r, s)
            )
        
        self.wait(5)
        
        # Remove updaters
        for planet in planets:
            planet.clear_updaters()


class ManimVideoGenerator:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Content type to scene mapping
        self.scene_map = {
            'photosynthesis': PhotosynthesisScene,
            'water': WaterCycleScene,
            'biology': DNAScene,
            'space': SolarSystemScene,
        }
    
    def detect_content_type(self, text):
        """Detect content type from text"""
        text_lower = text.lower()
        
        keywords = {
            'photosynthesis': ['photosynthesis', 'plant', 'chlorophyll', 'glucose', 'sunlight'],
            'water': ['water cycle', 'evaporation', 'precipitation', 'rain', 'cloud'],
            'biology': ['dna', 'gene', 'chromosome', 'helix', 'nucleotide'],
            'space': ['solar system', 'planet', 'orbit', 'sun', 'mars', 'earth'],
        }
        
        for content_type, words in keywords.items():
            if any(word in text_lower for word in words):
                return content_type
        
        return None
    
    def generate_audio(self, text, filename="narration.mp3"):
        """Generate audio from text"""
        audio_path = os.path.join(self.output_dir, filename)
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(audio_path)
        return audio_path
    
    def generate_video(self, text, output_filename="educational_video.mp4"):
        """Generate video using Manim"""
        content_type = self.detect_content_type(text)
        
        if content_type and content_type in self.scene_map:
            print(f"Detected content type: {content_type}")
            print("Generating animation with Manim...")
            
            # Get the scene class
            scene_class = self.scene_map[content_type]
            
            # Render the scene
            temp_dir = tempfile.mkdtemp()
            config.output_file = output_filename
            config.media_dir = temp_dir
            
            scene = scene_class()
            scene.render()
            
            # Get the rendered video path
            video_path = os.path.join(temp_dir, "videos", "1080p60", output_filename)
            
            # Generate audio
            print("Generating narration...")
            audio_path = self.generate_audio(text)
            
            # Combine video and audio using MoviePy
            from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
            
            video_clip = VideoFileClip(video_path)
            audio_clip = AudioFileClip(audio_path)
            
            # Adjust video duration to match audio
            if video_clip.duration < audio_clip.duration:
                video_clip = video_clip.loop(duration=audio_clip.duration)
            else:
                video_clip = video_clip.subclip(0, audio_clip.duration)
            
            final_clip = video_clip.set_audio(audio_clip)
            
            # Export
            output_path = os.path.join(self.output_dir, output_filename)
            final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
            
            # Close clips before cleanup
            video_clip.close()
            audio_clip.close()
            final_clip.close()
            
            # Cleanup
            try:
                shutil.rmtree(temp_dir)
            except PermissionError:
                print(f"Note: Temporary files at {temp_dir} couldn't be deleted (files in use)")
            
            print(f"✅ Video generated: {output_path}")
            return output_path
        else:
            print("Content type not recognized, using generic animation")
            # Fall back to basic text-based video
            from video_generator import VideoGenerator
            basic_gen = VideoGenerator(self.output_dir)
            return basic_gen.generate_video(text, output_filename)


# Example usage
if __name__ == "__main__":
    generator = ManimVideoGenerator()
    
    text = """
    Photosynthesis is the process by which plants convert sunlight into energy.
    Plants absorb carbon dioxide and water, and using light energy, they produce glucose and oxygen.
    """
    
    generator.generate_video(text.strip(), "photosynthesis_manim.mp4")
