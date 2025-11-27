"""
Manual test - Generate a simple circle animation to verify Manim works
This bypasses Gemini to test if the Manim pipeline itself works correctly
"""
from pathlib import Path
import os

# Simple Manim code that should work
SIMPLE_CODE = """from manim import *

class EducationScene(Scene):
    def construct(self):
        # NARRATION: "Let's draw a circle step by step."
        
        # Step 1: Show center point
        # NARRATION: "First, we start with a center point."
        center_dot = Dot(ORIGIN, color=RED, radius=0.2)
        center_label = Text("Center", font_size=36).next_to(center_dot, DOWN)
        self.play(FadeIn(center_dot, center_label))
        self.wait(2)
        
        # Step 2: Show radius line
        # NARRATION: "Next, we draw a radius line from the center."
        radius_line = Line(ORIGIN, RIGHT * 2, color=YELLOW, stroke_width=4)
        radius_label = Text("Radius", font_size=36).next_to(radius_line, UP)
        self.play(Create(radius_line), Write(radius_label))
        self.wait(2)
        
        # Step 3: Draw the circle
        # NARRATION: "Now, we rotate the radius to trace a perfect circle."
        circle = Circle(radius=2, color=BLUE, stroke_width=8)
        circle.move_to(ORIGIN)
        self.play(Create(circle, run_time=4))
        self.wait(2)
        
        # Step 4: Label the circle
        # NARRATION: "And there we have it, a perfect circle!"
        self.play(FadeOut(radius_line, radius_label))
        circle_label = Text("Circle", font_size=36).next_to(circle, DOWN, buff=0.5)
        self.play(Write(circle_label))
        self.wait(3)
"""

def test_manual_pipeline():
    """Test the complete pipeline without Gemini"""
    from manim_ai_generator import ManimAIGenerator
    import tempfile
    import sys
    
    # Fix console encoding for Windows
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("Testing manual Manim pipeline (no AI)...")
    
    generator = ManimAIGenerator()
    
    # Save test code
    temp_dir = Path(tempfile.gettempdir()) / "manim_test"
    temp_dir.mkdir(exist_ok=True)
    
    code_file = temp_dir / "scene.py"
    code_file.write_text(SIMPLE_CODE, encoding='utf-8')
    
    print(f"Code saved to: {code_file}")
    
    # Execute Manim directly
    print("\nExecuting Manim...")
    try:
        video_path = generator.execute_manim(SIMPLE_CODE, "manual_test")
        print(f"\nSUCCESS! Video at: {video_path}")
        
        # Add audio
        narration = "Let's draw a circle step by step. First, we start with a center point. Next, we draw a radius line from the center. Now, we rotate the radius to trace a perfect circle. And there we have it, a perfect circle!"
        generator.add_audio_to_video(video_path, narration)
        
        print(f"\nComplete pipeline successful!")
        print(f"Final video with audio: {video_path}")
        return True
        
    except Exception as e:
        print(f"\nFailed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_manual_pipeline()
    
    if success:
        print("\n" + "="*60)
        print("MANUAL TEST PASSED")
        print("The Manim pipeline works correctly.")
        print("If AI-generated videos still fail, the issue is with Gemini's code generation.")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("MANUAL TEST FAILED")
        print("The issue is with the Manim pipeline itself, not Gemini.")
        print("="*60)
