"""
AI-Powered Manim Video Generator
Pipeline: User Prompt → Gemini Elaborates → Gemini Generates Manim Code → Execute → Video
"""
import os
import re
import subprocess
import tempfile
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


class ManimAIGenerator:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        print(f"Using model: {model_name}")
    
    def _call_gemini_with_retry(self, prompt, max_retries=3):
        """Call Gemini API with retry logic for rate limits"""
        import time
        
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                error_str = str(e)
                if '429' in error_str or 'Resource exhausted' in error_str:
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt) * 2  # Exponential backoff: 2s, 4s, 8s
                        print(f"⚠️ Rate limit hit. Waiting {wait_time}s before retry {attempt + 2}/{max_retries}...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise Exception("API rate limit exceeded. Please wait a few minutes and try again.")
                else:
                    raise e
        
        raise Exception("Failed after all retries")
    
    def detect_scene_type(self, user_prompt):
        """Intelligently detect if 3D is needed for this topic"""
        
        # Keywords that require 3D
        require_3d = [
            'cube', 'sphere', 'pyramid', 'cone', 'cylinder', '3d', 'three dimensional',
            'solid', 'volume', 'surface', 'rotation in space', 'spatial', 'dimension',
            'polyhedron', 'prism', 'torus', 'geometry 3d'
        ]
        
        # Keywords that work best in 2D
        better_2d = [
            'function', 'graph', 'equation', 'chart', 'diagram', 'flow', 'tree',
            'network', 'circle', 'square', 'triangle', 'percentage', 'angle',
            'algebra', 'fraction', 'ratio', 'animation', 'step by step'
        ]
        
        prompt_lower = user_prompt.lower()
        
        # Count matches
        d3_score = sum(1 for keyword in require_3d if keyword in prompt_lower)
        d2_score = sum(1 for keyword in better_2d if keyword in prompt_lower)
        
        # Use 3D only if explicitly needed, default to 2D for speed
        use_3d = d3_score > d2_score and d3_score > 0
        
        print(f"🔍 Scene Type Detection: {'3D detected' if use_3d else '2D selected'} (3D score: {d3_score}, 2D score: {d2_score})")
        return use_3d
    
    def elaborate_prompt(self, user_prompt):
        """Step 1: Ask Gemini to elaborate the educational content"""
        
        prompt = f"""
You are an expert educator. A user wants to learn about: "{user_prompt}"

Create a SIMPLE, CLEAR explanation for a 30 second animation.

Format your response as:
1. **Title**: A clear, concise title
2. **Narration Script**: Write EXACTLY 4-5 sentences explaining the concept (total speaking time: EXACTLY 30 seconds at normal speech pace)
3. **Key Visual Elements**: List 5-7 visual elements to animate (be specific about colors, shapes, movements)
4. **Animation Timeline**: Break into detailed steps with timing:
   - Step 1: (5 seconds) Initial setup and title
   - Step 2: (7 seconds) Introduce first concept with visuals
   - Step 3: (7 seconds) Show transformation or interaction
   - Step 4: (7 seconds) Demonstrate key point with emphasis
   - Step 5: (4 seconds) Show final result and hold

Include details like "highlight element", "rotate object", "fade between states", etc.
Total duration MUST be: EXACTLY 30 seconds.
Narration MUST be SHORT - only 4-5 sentences to fit in 30 seconds.
"""
        
        print("📝 Step 1: Elaborating educational content...")
        elaboration = self._call_gemini_with_retry(prompt)
        print("✅ Content elaborated!")
        print(f"\n{elaboration}\n")
        
        return elaboration
    
    def generate_manim_code(self, elaboration, use_3d=False):
        """Step 2: Ask Gemini to generate Manim code with optional 3D support"""

        # Choose between 2D and 3D instructions
        if use_3d:
            scene_type = "ThreeDScene"
        else:
            scene_type = "Scene"

        prompt = f"""
You are an EXPERT Manim Community v0.19.0 animator. Generate CLEAN, EXECUTABLE Python code.

SCENE TYPE: {scene_type}
EDUCATIONAL CONTENT:
{elaboration}

═══════════════════════════════════════════════════════════════
MANDATORY STRUCTURE (MUST FOLLOW EXACTLY):
═══════════════════════════════════════════════════════════════

from manim import *

class EducationScene({scene_type}):
    def construct(self):
        # NARRATION: "Your narration here"
        # Step 1: Create objects
        obj = Circle(radius=1, color=BLUE, fill_opacity=0.5)
        self.play(Create(obj), run_time=2)
        self.wait(1)

═══════════════════════════════════════════════════════════════
ALLOWED MANIM OBJECTS (ONLY USE THESE):
═══════════════════════════════════════════════════════════════

**Basic Shapes:**
- Circle(radius=1, color=BLUE, fill_opacity=0.5, stroke_width=3)
- Square(side_length=2, color=RED, fill_opacity=0.7)
- Rectangle(width=3, height=2, color=GREEN)
- Triangle() - creates equilateral triangle
- Polygon(point1, point2, point3, ..., color=YELLOW)
- Line(start, end, color=WHITE, stroke_width=3)
- Arrow(start, end, color=ORANGE, stroke_width=3)
- Dot(radius=0.1, color=PURPLE, fill_opacity=1)

**Text:**
- Text("Hello", font_size=48, color=WHITE)
- Use Unicode: "x²", "π", "√", "∑", "∫", "≈", "≤", "≥", "×", "÷"

**Groups:**
- VGroup(obj1, obj2, obj3)

═══════════════════════════════════════════════════════════════
CORRECT SYNTAX PATTERNS (COPY THESE EXACTLY):
═══════════════════════════════════════════════════════════════

✅ CORRECT DOT:
dot = Dot(radius=0.2, color=RED, fill_opacity=1)

❌ WRONG: Dot(ORIGIN, radius=0.2)  # Never pass position as first arg

✅ CORRECT POSITIONING:
circle = Circle(radius=1)
circle.shift(UP * 2 + RIGHT * 3)
circle.move_to(ORIGIN)
circle.next_to(other_obj, UP, buff=0.5)

✅ CORRECT STYLING:
obj.set_color(BLUE)
obj.set_fill(opacity=0.5)  # Note: opacity= not fill_opacity=
obj.set_stroke(width=3, opacity=0.8)  # Note: opacity= not stroke_opacity=
# NEVER use fill_opacity= in set_stroke() - it only accepts color, width, opacity

✅ CORRECT ANIMATIONS:
self.play(Create(obj), run_time=2)
self.play(FadeIn(obj), run_time=1.5)
self.play(FadeOut(obj), run_time=1)
self.play(Write(text), run_time=2)
self.play(GrowFromCenter(circle), run_time=1.5)
self.play(ReplacementTransform(obj1, obj2), run_time=2)
self.play(Indicate(obj), run_time=1)
self.play(Circumscribe(obj), run_time=2)
self.play(Flash(obj), run_time=1)
self.wait(1)  # Minimum 0.5 seconds

✅ CORRECT COLORS (ONLY THESE):
RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE, PINK, TEAL, GOLD, WHITE, BLACK, GRAY

✅ CORRECT VERTICES:
triangle = Triangle()
vertices = triangle.get_vertices()  # Returns list of points
point_a = vertices[0]
point_b = vertices[1]

═══════════════════════════════════════════════════════════════
FORBIDDEN (WILL CAUSE ERRORS):
═══════════════════════════════════════════════════════════════

❌ NEVER USE THESE:
- Tex, MathTex, Matrix, LaTeX (causes compilation errors)
- TracedPath (not in Manim v0.19)
- normalize(), rotate_vector() (don't exist)
- get_vertex_coords() (use get_vertices())
- get_frame() (use get_center() or get_top() instead)
- config.frame_width, config.frame_height (already defined as FRAME_WIDTH, FRAME_HEIGHT)
- opacity= in constructors (use fill_opacity=)
- GRAY_A, LIGHT_GRAY, DARK_GRAY (invalid colors)
- Dot(point, radius=...) (wrong syntax)
- self.wait(0) (minimum is 0.5)
- Complex numpy operations or custom helper functions
- Method chaining after .animate (e.g., obj.animate.shift().rotate() - use separate play() calls)

❌ NEVER USE THESE PARAMETERS:
- uv_resolution=
- dash_length=
- angle_in_degrees=
- opacity= in Dot(), Circle(), etc constructors (use fill_opacity=)
- fill_opacity= in set_stroke() (only accepts color, width, opacity)

═══════════════════════════════════════════════════════════════
TIMING REQUIREMENTS:
═══════════════════════════════════════════════════════════════

- Total video: 25-30 seconds
- Each animation: run_time=1 to 3 seconds
- Each wait: 0.5 to 2 seconds
- Add # NARRATION: "..." before each major step

═══════════════════════════════════════════════════════════════
SIMPLE ANIMATION EXAMPLE (FOLLOW THIS PATTERN):
═══════════════════════════════════════════════════════════════

```python
from manim import *

class EducationScene(Scene):
    def construct(self):
        # NARRATION: "A circle is a round shape"
        title = Text("What is a Circle?", font_size=60, color=WHITE)
        self.play(FadeIn(title), run_time=2)
        self.wait(1)
        self.play(FadeOut(title), run_time=1)
        
        # NARRATION: "It has a center point"
        center = Dot(radius=0.15, color=RED, fill_opacity=1)
        label = Text("Center", font_size=36, color=WHITE)
        label.next_to(center, DOWN, buff=0.5)
        self.play(GrowFromCenter(center), run_time=1.5)
        self.play(FadeIn(label), run_time=1)
        self.wait(2)
        
        # NARRATION: "And all points at equal distance form the circle"
        circle = Circle(radius=2, color=BLUE, stroke_width=4)
        self.play(Create(circle), run_time=3)
        self.wait(2)
        
        # NARRATION: "This distance is called the radius"
        radius = Line(center.get_center(), circle.point_at_angle(0), color=YELLOW, stroke_width=3)
        radius_text = Text("Radius", font_size=32, color=YELLOW)
        radius_text.next_to(radius, UP, buff=0.3)
        self.play(Create(radius), FadeIn(radius_text), run_time=2)
        self.wait(3)
```

═══════════════════════════════════════════════════════════════
YOUR TASK:
═══════════════════════════════════════════════════════════════

1. Generate SIMPLE, CLEAN code following the example above
2. Use ONLY allowed shapes and animations
3. NO complex math, NO custom functions, NO invalid methods
4. Total duration: 25-30 seconds
5. Return ONLY code wrapped in ```python ... ```
6. NO explanations, NO markdown outside code block

Generate the code NOW:"""
        
        print("🎨 Step 2: Generating Manim code with AI...")
        response = self._call_gemini_with_retry(prompt)
        
        # Extract code from markdown
        code = response.strip()
        if '```python' in code:
            code = code.split('```python')[1].split('```')[0].strip()
        elif '```' in code:
            code = code.split('```')[1].split('```')[0].strip()
        
        # Validate and fix common Manim generation errors
        code = self._fix_generated_manim_code(code)
        
        print("✅ Manim code generated!")
        return code
    
    def _fix_generated_manim_code(self, code):
        """Fix common errors in AI-generated Manim code"""
        import re
        
        # Fix 1: Replace self.camera.animate.set_background_color() with self.camera.background_color =
        code = re.sub(
            r'self\.play\(self\.camera\.animate\.set_background_color\(([^)]+)\)',
            r'self.camera.background_color = \1\n        self.wait(0.5)\n        # Background changed',
            code
        )
        
        # Fix 2: Remove invalid .animate calls on camera
        code = code.replace('self.camera.animate', '# self.camera.animate (invalid)')
        
        # Fix 3: Replace invalid camera animations with proper background setting
        code = re.sub(
            r'self\.play\(\s*self\.camera\.background_color = ([^,)]+)',
            r'self.camera.background_color = \1\n        self.play(',
            code
        )
        
        # Fix 4: Fix double fill_fill_opacity (from bad regex replacement)
        code = code.replace('fill_fill_opacity=', 'fill_opacity=')
        code = code.replace('stroke_stroke_opacity=', 'stroke_opacity=')
        
        # Fix 5: Replace opacity= with fill_opacity= for mobjects, but only if not already fill_opacity
        # First handle parameters that have opacity= as keyword argument (not already prefixed)
        code = re.sub(r'(?<!fill_)(?<!stroke_)opacity=', 'fill_opacity=', code)
        
        # Fix 6: Remove TracedPath which is not in standard Manim
        code = code.replace('TracedPath(', '# TracedPath not supported - use Circle instead\n        # Circle(')
        
        # Fix 7: Ensure all Dot() calls use proper syntax - remove position as first arg if present
        # Dot(point, radius=...) -> Dot(radius=...)
        code = re.sub(
            r'Dot\s*\(\s*[A-Z_]+[A-Z_0-9]*\s*,\s*',
            r'Dot(',
            code
        )
        # Also handle Dot with coordinates as first arg
        code = re.sub(
            r'Dot\s*\(\s*(?:moving_dot\.get_center\(\)|[a-z_]+\.get_center\(\))\s*,\s*',
            r'Dot(',
            code
        )
        
        # Fix 8: Remove config.frame_width and config.frame_height usage (use injected constants)
        code = code.replace('config.frame_width', 'FRAME_WIDTH')
        code = code.replace('config.frame_height', 'FRAME_HEIGHT')
        
        # Fix 9: Fix invalid color names that aren't in Manim
        invalid_colors = {
            'GRAY_A': 'GRAY',
            'GREY_A': 'GRAY',
            'LIGHT_GRAY': 'GRAY',
            'LIGHT_GREY': 'GRAY',
            'DARK_GRAY': 'GRAY',
            'DARK_GREY': 'GRAY',
        }
        for invalid, valid in invalid_colors.items():
            code = code.replace(invalid, valid)
        
        # Fix 10: Remove .move_to() calls after object creation in same line
        # Dot(...).move_to(...) -> Dot(...)
        code = re.sub(
            r'(Dot\([^)]*\))\.move_to\([^)]*\)',
            r'\1',
            code
        )
        code = re.sub(
            r'(Circle\([^)]*\))\.move_to\([^)]*\)',
            r'\1',
            code
        )
        
        # Fix 11: Fix DashedLine - ensure stroke_width instead of stroke_opacity in wrong place
        code = re.sub(
            r'DashedLine\(([^)]+)\)\.set_stroke\(width=(\d+), fill_opacity=',
            r'DashedLine(\1).set_stroke(width=\2, opacity=',
            code
        )
        
        # Fix 12: Remove invalid wait(0) calls - minimum 0.5 seconds
        code = re.sub(r'self\.wait\(0\)', r'self.wait(0.5)', code)
        code = re.sub(r'self\.wait\(0\.0\)', r'self.wait(0.5)', code)
        
        # Fix 13: Replace get_vertex_coords() with get_vertices()
        code = code.replace('.get_vertex_coords()', '.get_vertices()')
        
        # Fix 14: Remove lines calling normalize() 
        code = re.sub(r'^.*normalize\(.*$', '# normalize() removed - not available in Manim v0.19', code, flags=re.MULTILINE)
        
        # Fix 15: Remove lines calling rotate_vector()
        code = re.sub(r'^.*rotate_vector\(.*$', '# rotate_vector() removed - not available in Manim v0.19', code, flags=re.MULTILINE)
        
        # Fix 16: Fix set_fill() calls - use opacity= not fill_opacity=
        code = re.sub(r'\.set_fill\(\s*fill_opacity=', '.set_fill(opacity=', code)
        code = re.sub(r'\.set_fill\(([^,)]+),\s*fill_opacity=', r'.set_fill(\1, opacity=', code)
        
        # Fix 17: Fix set_stroke() calls - remove fill_opacity and fix stroke_opacity
        # Remove fill_opacity= from set_stroke() calls (not a valid parameter)
        code = re.sub(r'\.set_stroke\(([^)]*),\s*fill_opacity=[^,)]+', r'.set_stroke(\1', code)
        code = re.sub(r'\.set_stroke\(\s*fill_opacity=[^,)]+,?\s*', '.set_stroke(', code)
        # Fix stroke_opacity= to opacity=
        code = re.sub(r'\.set_stroke\(\s*stroke_opacity=', '.set_stroke(opacity=', code)
        code = re.sub(r'\.set_stroke\(([^,)]+),\s*stroke_opacity=', r'.set_stroke(\1, opacity=', code)
        
        # Fix 18: Remove Tex, MathTex, Matrix which require LaTeX
        code = re.sub(r'(Tex|MathTex|Matrix)\(', r'Text(  # \1 replaced with Text\n        # Text(', code)
        
        # Fix 19: Fix invalid parameters in constructors
        invalid_params = ['uv_resolution=', 'dash_length=', 'angle_in_degrees=']
        for param in invalid_params:
            code = re.sub(rf'{param}[^,)]+,?\s*', '', code)
        
        # Fix 20: Ensure imports are clean
        code = re.sub(r'from manim import normalize_vector', '# Invalid import removed', code)
        code = re.sub(r'import normalize_vector', '# Invalid import removed', code)
        
        # Fix 21: Remove variable assignments that call normalize() or rotate_vector()
        code = re.sub(r'^\s*\w+\s*=.*normalize\(.*$', '# Line removed - normalize() not available', code, flags=re.MULTILINE)
        code = re.sub(r'^\s*\w+\s*=.*rotate_vector\(.*$', '# Line removed - rotate_vector() not available', code, flags=re.MULTILINE)
        
        # Fix 22: Replace complex vector math with simple UP/DOWN/LEFT/RIGHT
        # If we see any remaining problematic vector operations, comment them out
        code = re.sub(r'^\s*normal_vector.*$', 'normal_vector_c = UP  # Simplified - complex rotation removed', code, flags=re.MULTILINE)
        
        # Fix 23: Remove .get_frame() calls on potentially None objects
        # Replace variable.get_frame() with safer alternatives
        code = re.sub(r'\.get_frame\(\)', '.get_center()  # get_frame() replaced', code)
        
        # Fix 24: Remove method chaining after .animate that might fail
        # e.g., obj.animate.method1().method2() -> obj.animate.method1()
        code = re.sub(r'(\.animate\.[^(]+\([^)]*\))\.[a-zA-Z_]+\(', r'\1  # Chaining removed\n        # .', code)
        
        return code
    
    def extract_narration(self, code):
        """Extract narration from code comments"""
        narration_lines = []
        for line in code.split('\n'):
            if '# NARRATION:' in line:
                text = line.split('# NARRATION:')[1].strip().strip('"\'')
                narration_lines.append(text)
        
        narration = ' '.join(narration_lines)
        return narration if narration else "Watch this educational animation."
    
    def _add_audio_with_ffmpeg(self, video_path, narration, audio_path=None):
        """Fallback: Add audio using FFmpeg directly instead of MoviePy"""
        from gtts import gTTS
        import tempfile
        import subprocess
        import os
        
        print("\n🔧 Using FFmpeg direct merge (MoviePy fallback)...")
        
        # Generate audio if not provided
        if audio_path is None:
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            audio_path = temp_audio.name
            tts = gTTS(text=narration, lang='en', slow=False)
            tts.save(audio_path)
            print(f"🎵 Audio generated: {audio_path}")
        
        # Get video duration using ffprobe
        probe_cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]
        video_duration = float(subprocess.check_output(probe_cmd).decode().strip())
        
        # Get audio duration
        probe_cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            audio_path
        ]
        audio_duration = float(subprocess.check_output(probe_cmd).decode().strip())
        
        print(f"📊 Video: {video_duration:.1f}s, Audio: {audio_duration:.1f}s")
        
        # Create output path
        output_path = video_path.replace('.mp4', '_with_audio.mp4')
        
        # Use FFmpeg to merge - extend shorter media to match longer
        if abs(video_duration - audio_duration) < 1.0:
            # Close enough - simple merge
            ffmpeg_cmd = [
                'ffmpeg', '-y',
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                output_path
            ]
        elif video_duration > audio_duration:
            # Video longer - extend audio with silence
            ffmpeg_cmd = [
                'ffmpeg', '-y',
                '-i', video_path,
                '-i', audio_path,
                '-filter_complex', f'[1:a]apad=whole_dur={video_duration}[a]',
                '-map', '0:v',
                '-map', '[a]',
                '-c:v', 'copy',
                '-c:a', 'aac',
                output_path
            ]
        else:
            # Audio longer - loop last frame of video
            ffmpeg_cmd = [
                'ffmpeg', '-y',
                '-i', video_path,
                '-i', audio_path,
                '-filter_complex', f'[0:v]tpad=stop_mode=clone:stop_duration={audio_duration - video_duration}[v]',
                '-map', '[v]',
                '-map', '1:a',
                '-c:v', 'libx264',
                '-preset', 'ultrafast',
                '-c:a', 'aac',
                output_path
            ]
        
        print("🚀 Running FFmpeg merge...")
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"❌ FFmpeg failed: {result.stderr}")
            raise Exception(f"FFmpeg merge failed: {result.stderr}")

        # Replace original with merged version
        if os.path.exists(video_path):
            os.remove(video_path)
        os.rename(output_path, video_path)

        # Cleanup temp audio
        try:
            if audio_path and os.path.exists(audio_path):
                os.unlink(audio_path)
        except:
            pass

        print("✅ Audio merged successfully with FFmpeg!")
    
    def execute_manim(self, code, output_name="animation", use_3d=False):
        """Step 3: Execute the Manim code
        
        Args:
            code: The Manim Python code to execute
            output_name: Output filename
            use_3d: Whether this is a 3D scene (affects rendering)
        """
        
        print("🎬 Step 3: Executing Manim code...")
        
        # Create temporary Python file
        temp_dir = Path(tempfile.gettempdir()) / "manim_ai"
        temp_dir.mkdir(exist_ok=True)
        
        # Fix: Inject FRAME_WIDTH and FRAME_HEIGHT definitions if they are missing
        # This fixes NameError: name 'FRAME_WIDTH' is not defined in newer Manim versions
        if "from manim import *" in code:
            code = code.replace(
                "from manim import *", 
                "from manim import *\n\n# Fix for Manim versions where these are not exported\nFRAME_WIDTH = 14.0  # Default Manim frame width\nFRAME_HEIGHT = 8.0  # Default Manim frame height\nFRAME_X_RADIUS = 7.0\nFRAME_Y_RADIUS = 4.0\n"
            )
        
        # Remove any problematic imports that might be in the generated code
        code = code.replace("from manim.utils.space_ops import normalize_vector\n", "")
        code = code.replace("from manim.utils.space_ops import normalize_vector", "")
        
        code_file = temp_dir / "scene.py"
        code_file.write_text(code, encoding='utf-8')
        
        print(f"📄 Code saved to: {code_file}")
        print("\n--- GENERATED CODE ---")
        print(code)
        print("--- END CODE ---\n")

        # Run Manim
        # Adjust quality based on 3D (3D takes longer, use lower quality)
        quality_flag = "-ql"  # Low quality (fast)
        if not use_3d:
            quality_flag = "-qm"  # Medium quality for 2D (faster than 3D)
        
        # Manim command
        cmd = [
            "manim",
            quality_flag,
            "--format", "mp4",
            "--media_dir", str(self.output_dir),
            "--disable_caching",
            "--fps", "30",  # 30fps for smooth animations
            str(code_file),
            "EducationScene"
        ]
        
        print(f"🚀 Running: {' '.join(cmd)}")
        
        try:
            # Timeout: 2D is fast (60s), 3D is slower (120s)
            timeout = 120 if use_3d else 60
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(temp_dir)
            )
            
            if result.returncode != 0:
                print("❌ Manim execution failed!")
                print("STDERR:", result.stderr)
                print("STDOUT:", result.stdout)
                raise Exception(f"Manim failed: {result.stderr}")
            
            print("✅ Manim execution successful!")
            print(result.stdout)
            
            # Find the generated video - search recursively from temp_dir and output_dir
            print("\n🔍 Searching for generated video...")
            
            # Try to find EducationScene.mp4 recursively
            import shutil
            video_files = []
            
            # Search in temp_dir recursively
            if temp_dir.exists():
                video_files.extend(list(temp_dir.rglob("*.mp4")))
            
            # Search in output_dir recursively  
            if self.output_dir.exists():
                video_files.extend(list(self.output_dir.rglob("*.mp4")))
            
            # Filter to only recent videos (created in last 60 seconds)
            import time
            current_time = time.time()
            recent_videos = [v for v in video_files if current_time - v.stat().st_mtime < 60]
            
            if recent_videos:
                # Get the most recently created video
                latest_video = max(recent_videos, key=lambda p: p.stat().st_mtime)
                final_path = self.output_dir / f"{output_name}.mp4"

                # Ensure source file is fully written
                print("⏳ Waiting for file to be fully written...")
                time.sleep(0.5)

                # Copy to output directory
                shutil.copy2(latest_video, final_path)

                # Verify the copy is readable
                if not final_path.exists() or final_path.stat().st_size < 1000:
                    raise Exception(f"Copied file is invalid: {final_path}")

                print(f"✅ Video saved: {final_path}")
                print(f"📂 Original: {latest_video}")
                print(f"📊 Size: {final_path.stat().st_size / 1024:.1f} KB")

                # Give the OS a moment to release file handles
                time.sleep(0.5)

                return str(final_path)
            else:
                # Detailed debug info
                print("\n❌ No recent video found!")
                print("Searched in:")
                print(f"  - {temp_dir}")
                print(f"  - {self.output_dir}")
                print(f"\nAll .mp4 files found: {len(video_files)}")
                for vf in video_files[:5]:  # Show first 5
                    age = current_time - vf.stat().st_mtime
                    print(f"  - {vf} (age: {age:.0f}s)")

                raise Exception(f"No recent video file found. Checked {len(video_files)} total mp4 files.")

        except subprocess.TimeoutExpired:
            timeout_used = 180 if use_3d else 120
            raise Exception(f"Manim execution timed out (>{timeout_used}s)")
        except Exception as e:
            print(f"❌ Error executing Manim: {e}")
            print("💡 This might be an issue with the AI-generated code.")
            print("📝 Check the generated code above for errors.")
            raise
    
    def add_audio_to_video(self, video_path, narration):
        """Add narration audio to video using gTTS"""
        from gtts import gTTS
        from moviepy import VideoFileClip, AudioFileClip
        import tempfile
        import os
        import time

        print("\n🎵 Adding narration audio...")

        # Validate video file is readable BEFORE attempting audio merge
        print(f"🔍 Validating video file: {video_path}")
        if not os.path.exists(video_path):
            raise Exception(f"Video file not found: {video_path}")

        file_size = os.path.getsize(video_path)
        print(f"📊 Video file size: {file_size / 1024:.1f} KB")

        if file_size < 1000:
            raise Exception(f"Video file too small ({file_size} bytes), likely corrupted")

        # Wait a moment to ensure file is fully written and released by Manim
        time.sleep(1)

        # Try to load video with retry logic
        max_retries = 3
        video = None
        for attempt in range(max_retries):
            try:
                print(f"🎬 Loading video (attempt {attempt + 1}/{max_retries})...")
                # Use ffmpeg_reader explicitly to avoid issues
                video = VideoFileClip(video_path, audio=False, verbose=False)
                print(f"✅ Video loaded successfully: {video.duration:.1f}s, {video.size}")
                break
            except Exception as e:
                if video:
                    video.close()
                    video = None
                if attempt == max_retries - 1:
                    print(f"❌ Failed to load video after {max_retries} attempts")
                    print(f"Error: {e}")
                    # Try using FFmpeg directly as fallback
                    print("🔧 Attempting FFmpeg direct merge as fallback...")
                    return self._add_audio_with_ffmpeg(video_path, narration, None)
                print(f"⚠️ Attempt {attempt + 1} failed, retrying in 2 seconds...")
                time.sleep(2)

        # If we got here, video loaded successfully
        if video is None:
            raise Exception("Video failed to load")
        
        # Generate audio
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tts = gTTS(text=narration, lang='en', slow=False)
        tts.save(temp_audio.name)
        
        # Load audio
        audio = AudioFileClip(temp_audio.name)
        
        print(f"📊 Video duration: {video.duration:.1f}s, Audio duration: {audio.duration:.1f}s")
        
        # Video duration constraints: 30s minimum, 60s maximum
        min_duration = 30.0
        max_duration = 60.0
        
        if video.duration > max_duration:
            print(f"⚠️ Video too long: {video.duration:.1f}s - trimming to {max_duration}s")
            video = video.subclip(0, max_duration)
            target_duration = max_duration
        elif video.duration < min_duration:
            print(f"⏱️ Video is {video.duration:.1f}s - extending to {min_duration}s")
            from moviepy import CompositeVideoClip
            # Hold final frame for the remaining duration
            extended_video = CompositeVideoClip([video])
            extended_video = extended_video.set_duration(min_duration)
            video.close()
            video = extended_video
            target_duration = min_duration
        else:
            target_duration = video.duration
            print(f"✅ Video duration {target_duration:.1f}s is within 30-60s range")
        
        if audio.duration > target_duration:
            print(f"✂️ Trimming audio from {audio.duration:.1f}s to {target_duration:.1f}s")
            audio = audio.subclip(0, target_duration)
        elif audio.duration < target_duration:
            print(f"🔊 Extending audio to {target_duration:.1f}s with silence padding")
            from moviepy import CompositeAudioClip, AudioClip
            silence = AudioClip(lambda t: [0, 0], duration=target_duration - audio.duration, fps=audio.fps)
            audio = CompositeAudioClip([audio, silence.set_start(audio.duration)])
            audio = audio.set_duration(target_duration)
        
        # Set both to exact target duration
        video = video.set_duration(target_duration)
        audio = audio.set_duration(target_duration)
        
        # Set audio to video
        final_video = video.set_audio(audio)
        
        # Create a temporary output file
        temp_output = video_path.replace('.mp4', '_temp_audio.mp4')
        
        try:
            # Write video with audio to temp file
            final_video.write_videofile(
                temp_output,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                logger='bar',  # Use progress bar
                preset='ultrafast',
                threads=4
            )
            
            # Close all clips
            video.close()
            audio.close()
            final_video.close()
            
            # Replace original file
            if os.path.exists(video_path):
                os.remove(video_path)
            os.rename(temp_output, video_path)
            
            # Cleanup temp audio
            try:
                os.unlink(temp_audio.name)
            except:
                pass
            
            print("✅ Audio added to video!")
            
        except Exception as e:
            # Cleanup on error
            try:
                video.close()
                audio.close()
                final_video.close()
                if os.path.exists(temp_output):
                    os.remove(temp_output)
            except:
                pass
            raise e
    
    def generate_video(self, user_prompt, output_name=None, use_3d=None):
        """Complete pipeline: Prompt → Elaborate → Code → Execute → Add Audio
        
        Args:
            user_prompt: Topic for animation
            output_name: Output filename (auto-generated if None)
            use_3d: Use 3D scenes if True, 2D if False. If None, auto-detect based on topic.
        """
        
        if output_name is None:
            # Sanitize prompt for filename
            output_name = re.sub(r'[^\w\s-]', '', user_prompt)[:50].strip().replace(' ', '_')
        
        # Auto-detect scene type if not specified
        if use_3d is None:
            use_3d = self.detect_scene_type(user_prompt)
        
        print("\n" + "="*60)
        print(f"🎓 GENERATING VIDEO FOR: {user_prompt}")
        print(f"📐 Scene Type: {'3D (slower)' if use_3d else '2D (faster)'}{'- ⏱️ ~60s rendering' if not use_3d else '- ⏱️ ~90s rendering'}")
        print("="*60 + "\n")
        
        # Step 1: Elaborate
        elaboration = self.elaborate_prompt(user_prompt)
        
        # Step 2: Generate Manim code with 3D support
        manim_code = self.generate_manim_code(elaboration, use_3d=use_3d)
        
        # Step 3: Execute Manim
        video_path = self.execute_manim(manim_code, output_name, use_3d=use_3d)
        
        # Step 4: Extract narration and add audio
        narration = self.extract_narration(manim_code)
        if narration:
            self.add_audio_to_video(video_path, narration)

        print("\n" + "="*60)
        print("✅ COMPLETE!")
        print(f"📹 Video: {video_path}")
        print(f"🗣️ Narration: {narration}")
        print("="*60 + "\n")
        
        return {
            'video_path': video_path,
            'elaboration': elaboration,
            'manim_code': manim_code,
            'narration': narration,
            'use_3d': use_3d
        }


if __name__ == "__main__":
    # Test
    generator = ManimAIGenerator()
    
    result = generator.generate_video(
        "how step by step animated instructions on how to create a circle"
    )
    
    print(f"\n🎉 Done! Video at: {result['video_path']}")
