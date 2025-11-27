#!/usr/bin/env python3
"""
Quick test script for 3D animation support
Run this to test both 2D and 3D animations
"""

from manim_ai_generator import ManimAIGenerator
import sys

def test_3d_animation():
    """Test 3D animation generation"""
    print("\n" + "="*60)
    print(" Testing 3D Animation Generation")
    print("="*60 + "\n")
    
    generator = ManimAIGenerator()
    
    # Test topic that benefits from 3D
    topic = "How a cube rotates in 3D space showing all faces"
    
    try:
        print(f"📝 Topic: {topic}\n")
        
        result = generator.generate_video(
            user_prompt=topic,
            output_name="test_3d_cube",
            use_3d=True  # Enable 3D
        )
        
        print("\n✅ 3D Animation Generated Successfully!")
        print(f"📹 Video: {result['video_path']}")
        print(f"🗣️ Narration: {result['narration']}")
        return True
        
    except Exception as e:
        print(f"\n❌ 3D Animation Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_2d_animation():
    """Test 2D animation generation"""
    print("\n" + "="*60)
    print("🧪 Testing 2D Animation Generation")
    print("="*60 + "\n")
    
    generator = ManimAIGenerator()
    
    # Test topic that works well in 2D
    topic = "The basic shapes: circle, square, and triangle"
    
    try:
        print(f"📝 Topic: {topic}\n")
        
        result = generator.generate_video(
            user_prompt=topic,
            output_name="test_2d_shapes",
            use_3d=False  # Use 2D only
        )
        
        print("\n✅ 2D Animation Generated Successfully!")
        print(f"📹 Video: {result['video_path']}")
        print(f"🗣️ Narration: {result['narration']}")
        return True
        
    except Exception as e:
        print(f"\n❌ 2D Animation Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🎬 MANIM AI GENERATOR - 3D SUPPORT TEST SUITE")
    print("="*60)
    
    # Test both
    test_3d = test_3d_animation()
    test_2d = test_2d_animation()
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"3D Animation: {'✅ PASSED' if test_3d else '❌ FAILED'}")
    print(f"2D Animation: {'✅ PASSED' if test_2d else '❌ FAILED'}")
    
    if test_3d and test_2d:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n⚠️ Some tests failed. Check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
