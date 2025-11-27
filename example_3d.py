#!/usr/bin/env python3
"""
Example Manim 3D script with proper camera orientation
This shows the correct way to set up 3D scenes
"""

from manim import *

class ClearAdditionAnimation(ThreeDScene):
    """A+B=C visualization with proper camera setup"""
    
    def construct(self):
        # CRITICAL: Set camera FIRST before creating any objects
        # This ensures the scene is not tilted
        self.set_camera_orientation(phi=0*DEGREES, theta=0*DEGREES)
        
        # NARRATION: "Let's visualize addition with 3D blocks"
        
        # Create first group (A) - on the left
        group_a = VGroup()
        for i in range(3):
            cube_a = Cube(side_length=0.3, color=BLUE, fill_opacity=0.7)
            cube_a.shift(LEFT * 2 + UP * i * 0.35)
            group_a.add(cube_a)
        
        label_a = Text("A", font_size=48, color=BLUE)
        label_a.shift(LEFT * 2 + DOWN * 1.5)
        
        # Create second group (B) - in the middle
        group_b = VGroup()
        for i in range(2):
            cube_b = Cube(side_length=0.3, color=RED, fill_opacity=0.7)
            cube_b.shift(ORIGIN + UP * i * 0.35)
            group_b.add(cube_b)
        
        label_b = Text("B", font_size=48, color=RED)
        label_b.shift(ORIGIN + DOWN * 1.5)
        
        # Plus sign
        plus_sign = Text("+", font_size=60, color=WHITE)
        plus_sign.shift(LEFT * 1 + UP * 1)
        
        # Equals sign
        equals_sign = Text("=", font_size=60, color=WHITE)
        equals_sign.shift(RIGHT * 1 + UP * 1)
        
        # Show first group
        self.play(FadeIn(group_a), Write(label_a), run_time=1.5)
        self.wait(0.5)
        
        # Show plus sign and second group
        self.play(Write(plus_sign), run_time=0.5)
        self.wait(0.5)
        self.play(FadeIn(group_b), Write(label_b), run_time=1.5)
        self.wait(0.5)
        
        # Show equals sign
        self.play(Write(equals_sign), run_time=0.5)
        self.wait(0.5)
        
        # Create result group (C) - on the right
        group_c = VGroup()
        for i in range(5):  # 3 + 2 = 5
            cube_c = Cube(side_length=0.3, color=GREEN, fill_opacity=0.7)
            cube_c.shift(RIGHT * 2.5 + UP * (i - 2) * 0.35)
            group_c.add(cube_c)
        
        label_c = Text("C", font_size=48, color=GREEN)
        label_c.shift(RIGHT * 2.5 + DOWN * 1.5)
        
        # Show result
        self.play(FadeIn(group_c), Write(label_c), run_time=2)
        self.wait(1)
        
        # Highlight the result
        self.play(Indicate(group_c, run_time=1))
        self.wait(0.5)


class BetterCameraExamples(ThreeDScene):
    """Examples of different camera angles for 3D scenes"""
    
    def construct(self):
        # Example 1: Front view (phi=0, theta=0)
        self.set_camera_orientation(phi=0*DEGREES, theta=0*DEGREES)
        
        cube1 = Cube(side_length=1, color=BLUE, fill_opacity=0.7)
        self.play(FadeIn(cube1), run_time=1)
        self.wait(1)
        
        # Rotate in place
        self.play(Rotate(cube1, angle=PI, axis=Z_AXIS, run_time=2))
        self.wait(0.5)
        
        self.play(FadeOut(cube1))
        
        # Example 2: Isometric view (45 degrees)
        self.set_camera_orientation(phi=45*DEGREES, theta=45*DEGREES)
        self.wait(0.5)
        
        cube2 = Cube(side_length=1, color=RED, fill_opacity=0.7)
        self.play(FadeIn(cube2), run_time=1)
        self.wait(1)
        
        self.play(Rotate(cube2, angle=PI*2, axis=Z_AXIS, run_time=3))
        self.wait(0.5)
        
        self.play(FadeOut(cube2))
        
        # Example 3: Side view
        self.set_camera_orientation(phi=0*DEGREES, theta=90*DEGREES)
        self.wait(0.5)
        
        cube3 = Cube(side_length=1, color=GREEN, fill_opacity=0.7)
        self.play(FadeIn(cube3), run_time=1)
        self.wait(1)
        self.play(FadeOut(cube3))


class SimpleSphereAnimation(ThreeDScene):
    """Simple sphere animation with proper camera"""
    
    def construct(self):
        # CRITICAL: Set camera first!
        self.set_camera_orientation(phi=45*DEGREES, theta=45*DEGREES)
        
        # NARRATION: "Here's a sphere rotating in 3D space"
        
        # Create sphere
        sphere = Sphere(radius=1, resolution=(24, 24), color=BLUE, fill_opacity=0.8)
        
        # Animate
        self.play(FadeIn(sphere), run_time=1)
        self.wait(0.5)
        
        # Rotate smoothly
        self.play(Rotate(sphere, angle=PI*2, axis=Z_AXIS, run_time=3), rate_func=linear)
        self.wait(0.5)
        
        # Change color while rotating
        self.play(
            sphere.animate.set_color(RED),
            Rotate(sphere, angle=PI, axis=Y_AXIS, run_time=2),
            rate_func=smooth
        )
        self.wait(0.5)
        
        self.play(FadeOut(sphere))


class MultiObjectScene(ThreeDScene):
    """Multiple 3D objects scene with proper camera"""
    
    def construct(self):
        # Set camera to isometric view
        self.set_camera_orientation(phi=60*DEGREES, theta=45*DEGREES)
        
        # NARRATION: "Multiple 3D objects in space"
        
        # Create objects spread out
        sphere = Sphere(radius=0.6, color=BLUE, fill_opacity=0.8)
        sphere.shift(LEFT * 2)
        
        cube = Cube(side_length=1, color=RED, fill_opacity=0.8)
        cube.shift(ORIGIN)
        
        cylinder = Cylinder(radius=0.6, height=1.5, color=GREEN, fill_opacity=0.8)
        cylinder.shift(RIGHT * 2)
        
        # Create together
        self.play(
            FadeIn(sphere),
            FadeIn(cube),
            FadeIn(cylinder),
            run_time=2
        )
        self.wait(0.5)
        
        # Rotate all together
        self.play(
            Rotate(sphere, angle=PI, axis=Z_AXIS),
            Rotate(cube, angle=PI, axis=X_AXIS),
            Rotate(cylinder, angle=PI, axis=Y_AXIS),
            run_time=3
        )
        self.wait(0.5)
        
        self.play(FadeOut(sphere, cube, cylinder))


if __name__ == "__main__":
    # Run: manim -ql example_3d.py ClearAdditionAnimation
    print("✅ Example 3D Manim scenes loaded")
    print("\nTo render a scene, run:")
    print("  manim -ql example_3d.py ClearAdditionAnimation")
    print("  manim -ql example_3d.py BetterCameraExamples")
    print("  manim -ql example_3d.py SimpleSphereAnimation")
    print("  manim -ql example_3d.py MultiObjectScene")
