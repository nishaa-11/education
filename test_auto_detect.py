#!/usr/bin/env python3
"""
Test auto-detection of 2D vs 3D scenes
Demonstrates intelligent scene type selection based on topic
"""
import sys
sys.path.insert(0, '.')

from manim_ai_generator import ManimAIGenerator

def test_scene_detection():
    generator = ManimAIGenerator()
    
    test_topics = [
        # 2D topics
        ("Explain how fractions work", False),
        ("Graph the function y = x^2", False),
        ("Show percentage calculation: 20% of 100", False),
        ("Demonstrate algebraic equation solving step by step", False),
        
        # 3D topics  
        ("Show 3D cube rotation and transformation", True),
        ("Explain how sphere surface area relates to radius", True),
        ("Demonstrate cone volume visualization in 3D space", True),
        ("Show 3D polyhedron geometry concepts", True),
    ]
    
    print("=" * 80)
    print("🧪 AUTO-DETECTION TEST")
    print("=" * 80)
    
    for prompt, expected_3d in test_topics:
        detected_3d = generator.detect_scene_type(prompt)
        status = "✅" if detected_3d == expected_3d else "❌"
        print(f"\n{status} {prompt}")
        print(f"   Expected: {'3D' if expected_3d else '2D'} | Detected: {'3D' if detected_3d else '2D'}")
    
    print("\n" + "=" * 80)
    print("BENEFITS:")
    print("✓ 2D topics render FAST (~60 seconds)")
    print("✓ 3D topics render slower (~90 seconds) but with proper visualization")
    print("✓ System automatically chooses optimal approach")
    print("✓ You can override with use_3d parameter if needed")
    print("=" * 80)

if __name__ == "__main__":
    test_scene_detection()
