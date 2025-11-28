"""
Test the enhanced Gemini prompt and code generation
"""
import os
from manim_ai_generator import ManimAIGenerator

def test_simple_topics():
    """Test with simple educational topics"""
    generator = ManimAIGenerator()
    
    test_topics = [
        "Explain what is a circle and show its parts",
        "Show how a square transforms into a circle",
        "Demonstrate the Pythagorean theorem visually"
    ]
    
    print("=" * 80)
    print("TESTING ENHANCED PROMPT GENERATION")
    print("=" * 80)
    
    for i, topic in enumerate(test_topics, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}: {topic}")
        print(f"{'='*80}\n")
        
        try:
            # Generate video
            video_path = generator.generate_video(topic)
            
            if video_path and os.path.exists(video_path):
                print(f"\n✅ SUCCESS: Video generated at {video_path}")
                size = os.path.getsize(video_path) / 1024 / 1024
                print(f"   File size: {size:.2f} MB")
            else:
                print(f"\n❌ FAILED: No video file created")
                
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "="*80)
        if i < len(test_topics):
            input("\nPress Enter to continue to next test...")

if __name__ == "__main__":
    test_simple_topics()
