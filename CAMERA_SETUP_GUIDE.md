# 3D Camera Setup Guide - No More Tilted Views

## The Issue
Videos appearing tilted/angled because the camera orientation wasn't set correctly at the start.

## The Solution
**Always call `set_camera_orientation()` FIRST in the `construct()` method before creating any objects.**

## Camera Angle Presets

### 1. **Front View (Straight On)** ✅ Best for most cases
```python
self.set_camera_orientation(phi=0*DEGREES, theta=0*DEGREES)
```
- View from the front
- Objects appear directly facing camera
- Good for cubes, text, simple rotations
- No tilt, very clear

### 2. **Isometric View** ✅ Good for 3D structure
```python
self.set_camera_orientation(phi=45*DEGREES, theta=45*DEGREES)
```
- View from 45-degree angle
- Shows 3D perspective nicely
- Objects look 3D while being clear
- Slightly tilted for visual effect

### 3. **Top View** ✅ For looking down
```python
self.set_camera_orientation(phi=90*DEGREES, theta=0*DEGREES)
```
- Looking straight down
- Good for flattened 3D view
- Like looking at a blueprint from above

### 4. **Side View** ✅ For side profiles
```python
self.set_camera_orientation(phi=0*DEGREES, theta=90*DEGREES)
```
- Looking from the side
- Good for showing height and depth
- 2D-like appearance but in 3D context

### 5. **Back View** ✅ For rear perspective
```python
self.set_camera_orientation(phi=0*DEGREES, theta=180*DEGREES)
```
- Looking from behind
- Opposite of front view

## Code Template - Correct Order

### ❌ WRONG (Will appear tilted):
```python
from manim import *

class EducationScene(ThreeDScene):
    def construct(self):
        # Creating objects BEFORE setting camera
        cube = Cube(side_length=1, color=BLUE)  # WRONG!
        self.play(FadeIn(cube))
        
        # Setting camera after objects created
        self.set_camera_orientation(phi=45*DEGREES, theta=45*DEGREES)  # TOO LATE!
```

### ✅ CORRECT (Will appear properly):
```python
from manim import *

class EducationScene(ThreeDScene):
    def construct(self):
        # Set camera FIRST!
        self.set_camera_orientation(phi=0*DEGREES, theta=0*DEGREES)  # CORRECT!
        
        # Now create objects
        cube = Cube(side_length=1, color=BLUE)
        self.play(FadeIn(cube))
```

## Updated Gemini Prompt Instructions

The AI will now be instructed to:
1. **Always set camera first** in construct()
2. **Use specific camera angles** like phi=0, theta=0 for front view
3. **Avoid default tilted angles** like phi=75, theta=45
4. **Validate camera is called before objects**

## Examples by Use Case

### Addition A+B=C (Your Image)
```python
self.set_camera_orientation(phi=0*DEGREES, theta=0*DEGREES)
# Shows cubes straight on, very clear, no tilt
```

### Molecular Structure
```python
self.set_camera_orientation(phi=45*DEGREES, theta=45*DEGREES)
# Shows 3D bonds clearly, slightly rotated for perspective
```

### Rotating Cube
```python
self.set_camera_orientation(phi=0*DEGREES, theta=0*DEGREES)
# Cube rotates cleanly from front view
```

### Planet/Sphere Orbits
```python
self.set_camera_orientation(phi=30*DEGREES, theta=45*DEGREES)
# Good angle for showing orbits and 3D motion
```

## Parameter Meanings

- **phi** (φ): Vertical angle (0° = horizontal, 90° = top down)
- **theta** (θ): Horizontal angle (0° = front, 90° = right side, 180° = back)

Think of it like:
- `phi=0`: Eye level (horizontal)
- `phi=90`: Bird's eye view (looking down)
- `theta=0`: Looking straight ahead
- `theta=90`: Looking to the right
- `theta=180`: Looking behind

## Common Mistakes to Avoid

❌ **Mistake 1**: Forgetting to set camera
```python
def construct(self):
    cube = Cube()  # Camera defaults to weird angle
    self.play(FadeIn(cube))  # Appears tilted!
```

❌ **Mistake 2**: Setting camera after objects
```python
def construct(self):
    cube = Cube()
    self.play(FadeIn(cube))
    self.set_camera_orientation(...)  # Too late!
```

❌ **Mistake 3**: Using confusing angles like phi=75, theta=45
```python
self.set_camera_orientation(phi=75*DEGREES, theta=45*DEGREES)  # Confusing tilt
```

✅ **Correct**: Clear camera before objects
```python
def construct(self):
    self.set_camera_orientation(phi=0*DEGREES, theta=0*DEGREES)  # FIRST!
    cube = Cube()
    self.play(FadeIn(cube))  # Clean, no tilt!
```

## Testing Your Setup

Run the example script to see proper camera usage:
```bash
python example_3d.py
manim -ql example_3d.py ClearAdditionAnimation
```

This renders the A+B=C scene with proper front-view camera setup.

## Updating Your Prompts

When generating videos, use these phrases in your topic:
- "Show clearly" → Uses front view (phi=0, theta=0)
- "Show from angle" → Uses isometric (phi=45, theta=45)
- "Show from above" → Uses top view (phi=90, theta=0)
- "Show from side" → Uses side view (phi=0, theta=90)

The updated AI generator will now:
1. Recognize these keywords
2. Set appropriate camera angle
3. Ensure camera is set FIRST
4. Display without tilt

## Result

✅ **Before**: Videos appear tilted/angled
❌ 

✅ **After**: Videos display clearly with proper perspective
✅ Objects are properly oriented
✅ No unwanted tilt
✅ Professional appearance

The key is: **Camera First, Objects Second!**
