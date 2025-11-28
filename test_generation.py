"""
Test script to verify video generation works properly
"""
from manim_ai_generator import ManimAIGenerator
import os

def test_simple_generation():
    """Test a simple video generation"""
    print("\n" + "="*60)
    print("Testing Video Generation")
    print("="*60)
    
    # Initialize generator
    try:
        generator = ManimAIGenerator()
        print("✅ Generator initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize generator: {e}")
        return False
    
    # Test prompt
    test_prompt = "Explain what is a circle"
    
    try:
        print(f"\n📝 Testing with prompt: '{test_prompt}'")
        print("⏳ Generating video (this may take 30-60 seconds)...")
        
        result = generator.generate_video(
            test_prompt, 
            output_name="test_circle",
            use_3d=False  # Force 2D for faster testing
        )
        
        print("\n✅ Video generated successfully!")
        print(f"📹 Video path: {result['video_path']}")
        print(f"📊 File size: {os.path.getsize(result['video_path']) / 1024:.1f} KB")
        print(f"🗣️ Narration: {result['narration'][:100]}...")
        print(f"📐 Scene type: {'3D' if result['use_3d'] else '2D'}")
        
        # Verify file exists and is readable
        if os.path.exists(result['video_path']):
            print("✅ Video file exists and is accessible")
            return True
        else:
            print("❌ Video file not found")
            return False
            
    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_simple_generation()
    
    if success:
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("❌ TESTS FAILED")
        print("="*60)
        exit(1)
