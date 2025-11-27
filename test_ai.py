"""
Test the AI Manim pipeline
"""
from manim_ai_generator import ManimAIGenerator

def test_circle():
    print("Testing: How to draw a circle")
    generator = ManimAIGenerator()
    
    result = generator.generate_video(
        "how step by step animated instructions on how to create a circle"
    )
    
    print(f"\n✅ Success!")
    print(f"Video: {result['video_path']}")
    print(f"\nElaboration:\n{result['elaboration']}")
    print(f"\nNarration:\n{result['narration']}")

if __name__ == "__main__":
    test_circle()
