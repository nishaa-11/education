# 3D Animation Support - Updated Manim AI Generator

## Overview

The Manim AI Generator now supports **both 2D and 3D animations** with improved Gemini output formatting for better Manim compatibility.

## Key Improvements

### 1. **3D Scene Support**
- Supports both `Scene` (2D) and `ThreeDScene` (3D) classes
- Includes 3D shapes: Sphere, Cube, Cone, Cylinder, Prism, Torus
- Camera control with `set_camera_orientation(phi, theta)`
- Proper 3D rotations with axis parameters

### 2. **Better Structured Output**
- Gemini now generates code wrapped in triple backticks for clean extraction
- Clear separation of 2D and 3D capabilities
- Validated parameters to prevent errors like `uv_resolution` issues

### 3. **Proper 3D Parameters**
- **Sphere**: `Sphere(radius=1, resolution=(24, 24))`
- **Cube**: `Cube(side_length=1)`
- **Cone**: `Cone(base_radius=1, height=2, direction=UP)`
- **Cylinder**: `Cylinder(radius=1, height=2)`
- **Rotations**: `.rotate(PI/4, axis=Z_AXIS)`

### 4. **Improved Error Handling**
- Blacklisted invalid parameters: `uv_resolution`, `dash_length`, `angle_in_degrees`
- Enforced correct parameter formats
- Better validation messages

## Usage

### Python API

```python
from manim_ai_generator import ManimAIGenerator

generator = ManimAIGenerator()

# Generate 3D animation (default)
result = generator.generate_video(
    user_prompt="How does a sphere transform into a cube",
    output_name="3d_animation",
    use_3d=True  # Enable 3D
)

# Generate 2D animation
result = generator.generate_video(
    user_prompt="Explain photosynthesis",
    output_name="2d_animation",
    use_3d=False  # Use 2D only
)
```

### REST API

**Endpoint**: `POST /api/generate`

**With 3D (default)**:
```json
{
    "text": "Show how a sphere rotates in 3D space",
    "use_3d": true
}
```

**With 2D only**:
```json
{
    "text": "Explain the water cycle",
    "use_3d": false
}
```

## 3D Animation Examples

### Example 1: Sphere Transformation
```python
from manim import *

class EducationScene(ThreeDScene):
    def construct(self):
        # NARRATION: "Let's create a sphere"
        self.set_camera_orientation(phi=75*DEGREES, theta=45*DEGREES)
        
        sphere = Sphere(radius=1.5, resolution=(32, 32), color=BLUE, fill_opacity=0.8)
        self.play(FadeIn(sphere), run_time=1.5)
        self.wait(1)
        
        # NARRATION: "Now let's rotate it"
        self.play(Rotate(sphere, angle=PI, axis=Z_AXIS, run_time=2))
        self.wait(1)
        
        # NARRATION: "And transform to a cube"
        cube = Cube(side_length=2, color=RED, fill_opacity=0.8)
        self.play(ReplacementTransform(sphere, cube), run_time=2)
        self.wait(1)
        
        self.play(FadeOut(cube))
```

### Example 2: Complex 3D Scene
```python
from manim import *

class EducationScene(ThreeDScene):
    def construct(self):
        # NARRATION: "Here's a 3D visualization"
        self.set_camera_orientation(phi=70*DEGREES, theta=30*DEGREES)
        
        # Create objects
        sphere = Sphere(radius=1, resolution=(24, 24), color=BLUE)
        cube = Cube(side_length=1.5, color=RED).shift(RIGHT*2)
        cylinder = Cylinder(radius=0.8, height=2, color=GREEN).shift(LEFT*2)
        
        # Animate
        self.play(FadeIn(sphere), FadeIn(cube), FadeIn(cylinder), run_time=1.5)
        self.wait(1)
        
        # NARRATION: "All three objects rotating"
        self.play(
            Rotate(sphere, angle=PI*2, axis=Z_AXIS),
            Rotate(cube, angle=PI, axis=Y_AXIS),
            Rotate(cylinder, angle=PI/2, axis=X_AXIS),
            run_time=3
        )
        self.wait(1)
```

## Gemini Prompt Structure

The updated prompt includes:

1. **Scene Type Selection**: Automatically configures for 2D or 3D
2. **Allowed Features**: Lists only valid shapes and animations for the chosen type
3. **Parameter Validation**: Specifies exact parameter formats
4. **Output Format**: Requires code in triple backticks
5. **Safety Checks**: Pre-execution validation rules

## Technical Details

### Scene Classes

**2D Scenes**:
- Class: `EducationScene(Scene)`
- Canvas: 2D coordinate system
- Shapes: Circle, Rectangle, Square, Polygon, Triangle, Line, Arrow

**3D Scenes**:
- Class: `EducationScene(ThreeDScene)`
- Canvas: 3D coordinate system with camera
- Shapes: Sphere, Cube, Cone, Cylinder, Prism, Torus (in addition to 2D shapes)
- Camera: Adjustable with `set_camera_orientation(phi, theta)`

### Rendering Times

- **2D Low Quality**: ~10-30 seconds
- **2D Medium Quality**: ~30-60 seconds
- **3D Low Quality**: ~30-90 seconds
- **3D Medium Quality**: ~90-300 seconds

Timeout settings:
- 2D: 120 seconds
- 3D: 180 seconds

## Troubleshooting

### "Invalid parameter uv_resolution"
**Solution**: Use `resolution=(24, 24)` instead of `uv_resolution=(24, 24)`

### 3D Objects Not Appearing
**Solution**: Set camera orientation first:
```python
self.set_camera_orientation(phi=75*DEGREES, theta=45*DEGREES)
```

### Too Slow
**Solution**: Reduce resolution:
```python
sphere = Sphere(radius=1, resolution=(16, 16))  # Lower resolution = faster
```

### Scene Not Found Error
**Make sure class is named exactly**: `EducationScene`

## Files Modified

1. **manim_ai_generator.py**
   - Updated `generate_manim_code()` with `use_3d` parameter
   - Enhanced prompt with 3D-specific instructions
   - Updated `execute_manim()` with 3D timeout handling
   - Updated `generate_video()` with 3D support

2. **app.py**
   - Updated `/api/generate` endpoint to accept `use_3d` parameter
   - Updated status tracking to include 3D info

## Future Enhancements

- [ ] Mixed 2D/3D scenes
- [ ] Custom camera paths
- [ ] Advanced lighting controls
- [ ] Particle systems
- [ ] More 3D primitive shapes

## Contributing

When adding new 3D features:
1. Test with low resolution first
2. Document parameter restrictions
3. Update the Gemini prompt with clear examples
4. Add timeout adjustments if needed
