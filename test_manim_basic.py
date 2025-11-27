"""
Quick test to verify Manim works without LaTeX
"""
from manim import *

class SimpleTest(Scene):
    def construct(self):
        # Test basic shapes and Text (no MathTex)
        circle = Circle(radius=2, color=BLUE)
        text = Text("Hello Circle!", color=WHITE).next_to(circle, UP)
        
        self.play(Create(circle))
        self.play(Write(text))
        self.wait(1)
        
        # Test another shape
        square = Square(side_length=2, color=RED)
        self.play(Transform(circle, square))
        self.wait(1)

if __name__ == "__main__":
    import subprocess
    import os
    
    # Save this file and render
    print("Testing Manim without LaTeX...")
    result = subprocess.run([
        "manim",
        "-ql",
        "--format", "mp4",
        __file__,
        "SimpleTest"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Success! Manim works without LaTeX")
    else:
        print("❌ Error:")
        print(result.stderr)
