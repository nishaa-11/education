"""
Example usage of the Video Generator
Run this script to see how the video generator works
"""
from video_generator import VideoGenerator

# Create a video generator instance
generator = VideoGenerator(output_dir="output")

# Example 1: Simple educational video
print("=" * 50)
print("Example 1: Photosynthesis")
print("=" * 50)

text1 = """
Welcome to this lesson on photosynthesis. 
Photosynthesis is the process by which plants convert sunlight into energy. 
This process occurs in the chloroplasts of plant cells. 
Plants absorb carbon dioxide from the air and water from the soil. 
Using sunlight as energy, they combine these to produce glucose and oxygen.
"""

video1 = generator.generate_video(text1.strip(), "photosynthesis.mp4")
print(f"\n✅ Video saved to: {video1}\n")


# Example 2: Math concept
print("=" * 50)
print("Example 2: The Pythagorean Theorem")
print("=" * 50)

text2 = """
Let's learn about the Pythagorean Theorem. 
This theorem applies to right triangles. 
It states that the square of the hypotenuse equals the sum of the squares of the other two sides. 
In formula form, a squared plus b squared equals c squared. 
This theorem has countless applications in mathematics and engineering.
"""

video2 = generator.generate_video(text2.strip(), "pythagorean_theorem.mp4")
print(f"\n✅ Video saved to: {video2}\n")


# Example 3: Short concept
print("=" * 50)
print("Example 3: Gravity")
print("=" * 50)

text3 = """
Gravity is a fundamental force of nature. 
It attracts objects with mass toward each other. 
On Earth, gravity gives weight to objects and causes them to fall when dropped. 
The greater the mass of an object, the stronger its gravitational pull.
"""

video3 = generator.generate_video(text3.strip(), "gravity.mp4")
print(f"\n✅ Video saved to: {video3}\n")

print("=" * 50)
print("All example videos generated successfully!")
print("Check the 'output' folder to view them.")
print("=" * 50)
