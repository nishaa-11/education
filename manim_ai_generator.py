"""
AI-Powered Manim Video Generator
Pipeline: User Prompt → Gemini Elaborates → Gemini Generates Manim Code → Execute → Video
"""
import os
import json
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
            shape_options = """
1. **2D Shapes**: Circle, Rectangle, Square, Polygon, Triangle, Line, Arrow, Dot
2. **3D Shapes**: Sphere, Cube, Cone, Cylinder, Prism, Torus
   - **IMPORTANT 3D PARAMETERS**:
     - Sphere: Sphere(radius=1, resolution=(24, 24)) - resolution is tuple (latitude, longitude)
     - Cube: Cube(side_length=1)
     - Cone: Cone(base_radius=1, height=2, direction=UP)
     - Cylinder: Cylinder(radius=1, height=2)
   - **3D Positioning**: .shift(UP*2), .rotate(PI/4, axis=Z_AXIS), .set_color(BLUE)
   - **3D Camera - MUST SET FIRST IN construct()**: 
     * **DEFAULT (BEST for educational content)**: self.set_camera_orientation(phi=0*DEGREES, theta=0*DEGREES) - STRAIGHT FRONT VIEW, NO TILT
     * For 45-degree isometric view: self.set_camera_orientation(phi=45*DEGREES, theta=45*DEGREES)
     * For top view: self.set_camera_orientation(phi=90*DEGREES, theta=0*DEGREES)
     * For side view: self.set_camera_orientation(phi=0*DEGREES, theta=90*DEGREES)
     * **NEVER use phi=75, theta=30 or similar - those create unwanted tilt**
"""
            camera_setup = """
# **CRITICAL FOR 3D - SET CAMERA FIRST**:
# Call set_camera_orientation() IMMEDIATELY FIRST in construct() before creating objects
# DEFAULT: self.set_camera_orientation(phi=0*DEGREES, theta=0*DEGREES)  # Front view - no tilt
# This gives clear, professional educational view - ALWAYS USE THIS UNLESS INSTRUCTED OTHERWISE
"""
            forbidden = "**ABSOLUTELY FORBIDDEN**: Matrix, Tex, MathTex, SVGMobject, ImageMobject, Integer, DecimalNumber"
        else:
            scene_type = "Scene"
            shape_options = """
1. **Shapes ONLY**: Circle, Rectangle, Square, Polygon, Triangle, Line, Arrow, Dot
   - DO NOT use: Arc, Ellipse, Sphere, Cube, Cone, Cylinder, Prism (3D objects)
"""
            camera_setup = ""
            forbidden = "**ABSOLUTELY FORBIDDEN**: Matrix, Tex, MathTex, SVGMobject, ImageMobject, Integer, DecimalNumber, Arc, Ellipse"
        
        prompt = f"""
You are an ADVANCED Manim animator creating PROFESSIONAL educational animations.

SCENE TYPE: {scene_type}
USE 3D: {'Yes - Maximize 3D effects' if use_3d else 'No - Use 2D only'}

EDUCATIONAL CONTENT TO ANIMATE:
{elaboration}

YOUR TASK: Generate perfectly formatted Python code that Manim can execute without errors.

OUTPUT FORMAT REQUIREMENTS:
1. Return ONLY clean Python code - NO markdown, NO explanations, NO comments outside code
2. Wrap entire code in triple backticks: ```python ... ```
3. Code MUST be directly executable with: manim -ql script.py EducationScene
4. ALL code must be within the construct() method
5. Include # NARRATION: "text" comments for each major animation step

ALLOWED MANIM FEATURES (NOTHING ELSE):
{shape_options}

2. **Text ONLY**: Text() - NEVER Matrix, Tex, MathTex, or anything requiring LaTeX
3. **Advanced Animations**: 
   - ReplacementTransform (morphing between shapes)
   - Indicate (highlight/pulse effect)
   - Circumscribe (draw box around)
   - Flash (flash effect)
   - Rotate (rotation)
   - FadeIn, FadeOut, Create, Write, GrowFromCenter
   - For 3D: Rotate with axis parameter, set_camera_orientation()
4. **Colors & Styles**: 
   - ONLY use these exact Manim colors: RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE, PINK, TEAL, GOLD, WHITE, BLACK, GRAY
   - set_color(), set_fill(), set_opacity()
   - stroke_width=2 to 10
5. **Text Formatting**:
   - Text("content", font_size=48, color=BLUE)
   - Use Unicode for symbols: "x²", "∑", "π", "≈", "×", "÷"
6. **Grouping**: VGroup, Group
7. **Positioning**: 
   - .shift(UP*2 + RIGHT*3), .move_to(ORIGIN)
   - .next_to(obj, UP, buff=0.5)
8. **Timing**: Total EXACTLY 25-30 seconds (all run_times + waits)

CRITICAL RULES (VIOLATION = FAILURE):
- from manim import *
- class EducationScene({0}):
- def construct(self):
- {1}
- **ABSOLUTELY NO invalid parameters** like uv_resolution, dash_length, angle_in_degrees
- **MINIMUM wait duration is 0.5 seconds** - NEVER use self.wait(0)
- Total duration: 25-30 seconds exactly
- Each animation step must have a # NARRATION: "..." comment
- Match educational content - no generic code
{camera_setup}
- **FOR 3D SCENES**: IMMEDIATELY in construct(), ADD THIS FIRST LINE BEFORE ALL OBJECTS:
  self.set_camera_orientation(phi=0*DEGREES, theta=0*DEGREES)
  This creates a professional front-view educational perspective. NEVER use phi > 70 or theta < 10 (causes unwanted tilt).

SAFETY CHECKS BEFORE RETURNING CODE:
✓ from manim import * is the first import
✓ class EducationScene({0}): is defined correctly
✓ def construct(self): is indented inside the class
✓ For 3D: self.set_camera_orientation(phi=0*DEGREES, theta=0*DEGREES) is the FIRST line in construct()
✓ All animations have run_time and MINIMUM 0.5s wait
✓ NO invalid parameters (especially uv_resolution, angle_in_degrees, dash_length)
✓ Total duration is 25-30 seconds
✓ Code is executable Python
✓ NO markdown formatting - only code

Return ONLY the code wrapped in ```python ... ```, nothing else.""".format(scene_type, forbidden)
        
        print("🎨 Step 2: Generating Manim code with AI...")
        response = self._call_gemini_with_retry(prompt)
        
        # Extract code from markdown
        code = response.strip()
        if '```python' in code:
            code = code.split('```python')[1].split('```')[0].strip()
        elif '```' in code:
            code = code.split('```')[1].split('```')[0].strip()
        
        print("✅ Manim code generated!")
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
        
        print(f"🚀 Running FFmpeg merge...")
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
        
        print(f"✅ Audio merged successfully with FFmpeg!")
    
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
        
        code_file = temp_dir / "scene.py"
        code_file.write_text(code, encoding='utf-8')
        
        print(f"📄 Code saved to: {code_file}")
        print("\n--- GENERATED CODE ---")
        print(code)
        print("--- END CODE ---\n")
        
        # Run Manim
        output_path = self.output_dir / f"{output_name}.mp4"
        
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
                print(f"⏳ Waiting for file to be fully written...")
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
                print(f"Searched in:")
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
            print(f"\n💡 This might be an issue with the AI-generated code.")
            print(f"📝 Check the generated code above for errors.")
            raise
    
    def add_audio_to_video(self, video_path, narration):
        """Add narration audio to video using gTTS"""
        from gtts import gTTS
        from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
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
                    return self._add_audio_with_ffmpeg(video_path, narration, temp_audio.name if 'temp_audio' in locals() else None)
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
        
        # Force both to 30 seconds - trim if longer, extend if shorter
        target_duration = 30.0
        
        if video.duration > target_duration:
            print(f"✂️ Trimming video from {video.duration:.1f}s to {target_duration:.1f}s")
            video = video.subclip(0, target_duration)
        elif video.duration < target_duration:
            print(f"⚠️ Video is shorter ({video.duration:.1f}s), using as-is")
            target_duration = video.duration  # Use actual video duration
        
        if audio.duration > target_duration:
            print(f"✂️ Trimming audio from {audio.duration:.1f}s to {target_duration:.1f}s")
            audio = audio.subclip(0, target_duration)
        elif audio.duration < target_duration:
            print(f"⚠️ Extending audio to {target_duration:.1f}s")
            from moviepy.audio.AudioClip import CompositeAudioClip
            from moviepy.audio.AudioClip import AudioClip
            silence = AudioClip(lambda t: [0, 0], duration=target_duration - audio.duration, fps=audio.fps)
            audio = CompositeAudioClip([audio, silence.set_start(audio.duration)])
        
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
            
            print(f"✅ Audio added to video!")
            
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
        
        print(f"\n{'='*60}")
        print(f"🎓 GENERATING VIDEO FOR: {user_prompt}")
        print(f"📐 Scene Type: {'3D (slower)' if use_3d else '2D (faster)'}{'- ⏱️ ~60s rendering' if not use_3d else '- ⏱️ ~90s rendering'}")
        print(f"{'='*60}\n")
        
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
        
        print(f"\n{'='*60}")
        print(f"✅ COMPLETE!")
        print(f"📹 Video: {video_path}")
        print(f"🗣️ Narration: {narration}")
        print(f"{'='*60}\n")
        
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
