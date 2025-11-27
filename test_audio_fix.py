"""
Test the audio fix by trying to load and add audio to the problematic video
"""
from manim_ai_generator import ManimAIGenerator

generator = ManimAIGenerator()

# Test with the problematic video
video_path = r"output\video_bb6e4b17-e3c9-434b-ba54-242a30ff6985.mp4"
narration = "This is a test narration to verify the audio merging works correctly."

print("Testing audio addition to existing video...")
print(f"Video: {video_path}")

try:
    generator.add_audio_to_video(video_path, narration)
    print("✅ SUCCESS! Audio added successfully")
except Exception as e:
    print(f"❌ FAILED: {e}")
