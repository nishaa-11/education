#!/usr/bin/env python3
"""
Quick test to show the difference between proper and improper camera setup
"""

from manim import *

class ProperCameraSetup(ThreeDScene):
    """Shows CORRECT camera setup - clear view, no tilt"""
    
    def construct(self):
        # ✅ CORRECT: Camera set FIRST
        self.set_camera_orientation(phi=0*DEGREES, theta=0*DEGREES)
        
        # Title
        title = Text("Proper Camera Setup", font_size=48, color=GREEN)
        title.shift(UP * 3)
        self.add_fixed_in_frame_mobjects(title)
        
        # Create and show cubes with clear view
        cube1 = Cube(side_length=0.8, color=BLUE, fill_opacity=0.7)
        cube1.shift(LEFT * 2)
        
        cube2 = Cube(side_length=0.8, color=RED, fill_opacity=0.7)
        cube2.shift(ORIGIN)
        
        cube3 = Cube(side_length=0.8, color=GREEN, fill_opacity=0.7)
        cube3.shift(RIGHT * 2)
        
        # Show cubes
        self.play(FadeIn(cube1), FadeIn(cube2), FadeIn(cube3), run_time=1.5)
        self.wait(0.5)
        
        # Rotate - notice NO TILT, clean rotation
        self.play(
            Rotate(cube1, angle=PI/2, axis=Z_AXIS),
            Rotate(cube2, angle=PI/2, axis=Y_AXIS),
            Rotate(cube3, angle=PI/2, axis=X_AXIS),
            run_time=2
        )
        self.wait(1)


class ImproperCameraSetup(ThreeDScene):
    """Shows INCORRECT camera setup - appears tilted"""
    
    def construct(self):
        # ❌ WRONG: Using weird angle like default
        self.set_camera_orientation(phi=75*DEGREES, theta=45*DEGREES)
        
        # Title
        title = Text("Improper Camera Setup (Tilted)", font_size=48, color=RED)
        title.shift(UP * 3)
        self.add_fixed_in_frame_mobjects(title)
        
        # Create same cubes
        cube1 = Cube(side_length=0.8, color=BLUE, fill_opacity=0.7)
        cube1.shift(LEFT * 2)
        
        cube2 = Cube(side_length=0.8, color=RED, fill_opacity=0.7)
        cube2.shift(ORIGIN)
        
        cube3 = Cube(side_length=0.8, color=GREEN, fill_opacity=0.7)
        cube3.shift(RIGHT * 2)
        
        # Show cubes - notice they appear TILTED
        self.play(FadeIn(cube1), FadeIn(cube2), FadeIn(cube3), run_time=1.5)
        self.wait(0.5)
        
        # Rotate - the tilt is still there
        self.play(
            Rotate(cube1, angle=PI/2, axis=Z_AXIS),
            Rotate(cube2, angle=PI/2, axis=Y_AXIS),
            Rotate(cube3, angle=PI/2, axis=X_AXIS),
            run_time=2
        )
        self.wait(1)


class AllCameraAngles(ThreeDScene):
    """Show all important camera angles"""
    
    def construct(self):
        # Each angle gets shown with a label
        angles = [
            ("Front (0°, 0°)", 0, 0, BLUE),
            ("Isometric (45°, 45°)", 45, 45, GREEN),
            ("Top (90°, 0°)", 90, 0, RED),
            ("Side (0°, 90°)", 0, 90, YELLOW),
        ]
        
        for name, phi_deg, theta_deg, color in angles:
            # Set camera
            self.set_camera_orientation(phi=phi_deg*DEGREES, theta=theta_deg*DEGREES)
            
            # Label
            label = Text(name, font_size=36, color=color)
            label.shift(UP * 3.5)
            self.add_fixed_in_frame_mobjects(label)
            
            # Create cube
            cube = Cube(side_length=1, color=color, fill_opacity=0.7)
            
            # Show it
            self.play(FadeIn(cube), run_time=0.8)
            self.wait(1.5)
            self.play(FadeOut(cube), run_time=0.5)
            
            # Remove label for next iteration
            self.remove_fixed_in_frame_mobjects(label)


class CorrectedAdditionScene(ThreeDScene):
    """Your A+B=C scene with PROPER camera setup"""
    
    def construct(self):
        # ✅ IMPORTANT: Set camera FIRST and to FRONT VIEW for clarity
        self.set_camera_orientation(phi=0*DEGREES, theta=0*DEGREES)
        
        # Title
        title = Text("A + B = C", font_size=60, color=WHITE)
        title.shift(UP * 3.5)
        self.add_fixed_in_frame_mobjects(title)
        
        # Group A (3 cubes) - Left side
        group_a = VGroup()
        for i in range(3):
            cube = Cube(side_length=0.4, color=BLUE, fill_opacity=0.8)
            cube.shift(LEFT * 3 + UP * (i - 1) * 0.5)
            group_a.add(cube)
        
        label_a = Text("A", font_size=48, color=BLUE)
        label_a.shift(LEFT * 3 + DOWN * 2)
        self.add_fixed_in_frame_mobjects(label_a)
        
        # Plus sign
        plus = Text("+", font_size=60, color=WHITE)
        plus.shift(UP * 0.5)
        self.add_fixed_in_frame_mobjects(plus)
        
        # Group B (2 cubes) - Middle
        group_b = VGroup()
        for i in range(2):
            cube = Cube(side_length=0.4, color=RED, fill_opacity=0.8)
            cube.shift(ORIGIN + UP * (i - 0.5) * 0.5)
            group_b.add(cube)
        
        label_b = Text("B", font_size=48, color=RED)
        label_b.shift(ORIGIN + DOWN * 2)
        self.add_fixed_in_frame_mobjects(label_b)
        
        # Equals sign
        equals = Text("=", font_size=60, color=WHITE)
        equals.shift(RIGHT * 1.5 + UP * 0.5)
        self.add_fixed_in_frame_mobjects(equals)
        
        # Group C (5 cubes) - Right side
        group_c = VGroup()
        for i in range(5):
            cube = Cube(side_length=0.4, color=GREEN, fill_opacity=0.8)
            cube.shift(RIGHT * 3 + UP * (i - 2) * 0.5)
            group_c.add(cube)
        
        label_c = Text("C", font_size=48, color=GREEN)
        label_c.shift(RIGHT * 3 + DOWN * 2)
        self.add_fixed_in_frame_mobjects(label_c)
        
        # Animate in order
        self.play(FadeIn(group_a), run_time=1)
        self.wait(0.5)
        
        self.play(FadeIn(group_b), run_time=1)
        self.wait(0.5)
        
        self.play(FadeIn(group_c), run_time=1.5)
        self.wait(1)
        
        # Highlight result
        self.play(Indicate(group_c, run_time=1))
        self.wait(0.5)


if __name__ == "__main__":
    print("✅ Camera Setup Examples Loaded")
    print("\nTo test proper vs improper camera setup, run:")
    print("  manim -ql camera_setup_test.py ProperCameraSetup")
    print("  manim -ql camera_setup_test.py ImproperCameraSetup")
    print("\nTo see all camera angles:")
    print("  manim -ql camera_setup_test.py AllCameraAngles")
    print("\nTo see corrected A+B=C scene:")
    print("  manim -ql camera_setup_test.py CorrectedAdditionScene")
