"""
Test different topics to verify AI works for any subject
"""
from manim_ai_generator import ManimAIGenerator

def test_topic(topic):
    """Test a specific topic"""
    print(f"\n{'='*70}")
    print(f"Testing topic: {topic}")
    print('='*70)
    
    try:
        generator = ManimAIGenerator()
        result = generator.generate_video(topic, output_name=f"test_{topic.replace(' ', '_')[:20]}")
        print(f"\n✅ SUCCESS for '{topic}'!")
        print(f"📹 Video: {result['video_path']}")
        return True
    except Exception as e:
        print(f"\n❌ FAILED for '{topic}': {e}")
        return False

if __name__ == "__main__":
    # Test multiple topics
    topics = [
        "how to draw a circle step by step",
        "bubble sort algorithm explained",
        "how photosynthesis works",
        "pythagoras theorem demonstration",
    ]
    
    results = {}
    for topic in topics:
        results[topic] = test_topic(topic)
        input("\nPress Enter to continue to next topic...")
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    for topic, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {topic}")
