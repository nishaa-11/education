# 3D Animation Examples & Best Practices

## Example Prompts That Work Well with 3D

### Geometry & Shapes
✅ **Good for 3D**:
- "How a cube rotates showing all six faces"
- "The properties of a sphere and how it differs from a circle"
- "How to construct a cylinder from a rectangle"
- "Cone volume calculation visualization"

❌ **Better in 2D**:
- "What is a triangle" (too simple for 3D)
- "Parts of a circle explained" (inherently 2D)

### Physics & Motion
✅ **Good for 3D**:
- "How objects rotate in 3D space"
- "Understanding 3D vectors and directions"
- "Showing Earth's rotation and axis"
- "Planet orbits in the solar system"

❌ **Better in 2D**:
- "Newton's laws of motion" (can work in 2D with arrows)
- "Force diagrams" (typically 2D)

### Chemistry & Biology
✅ **Good for 3D**:
- "Molecular structure of water in 3D"
- "DNA double helix structure"
- "Protein folding visualization"
- "Crystal lattice structure"

❌ **Better in 2D**:
- "The periodic table" (inherently 2D)
- "Photosynthesis process" (process diagram better in 2D)

### Mathematics
✅ **Good for 3D**:
- "Rotating a graph around the axis to show volume"
- "3D coordinate system and plotting points"
- "Surface of revolution concept"
- "Parameterized curves in 3D"

❌ **Better in 2D**:
- "Graph of y=x²" (basic function plotting)
- "Area under a curve" (2D concept)

## 3D Generation Examples

### Example 1: Simple 3D Cube Rotation
```bash
# Command line usage
python app.py

# API Call
POST /api/generate
{
    "text": "Show how a cube rotates in 3D space with all faces visible",
    "use_3d": true
}
```

Expected output:
- Cube appears
- Rotates 360 degrees
- Audio narration explains the rotation
- Duration: ~30 seconds

### Example 2: Complex 3D Scene with Multiple Objects
```python
from manim_ai_generator import ManimAIGenerator

generator = ManimAIGenerator()

result = generator.generate_video(
    user_prompt="Show a sphere, cube, and cylinder in 3D space rotating together",
    use_3d=True,
    output_name="3d_multiple_objects"
)
```

### Example 3: Force 2D for Comparison
```python
# Same topic in 2D
result = generator.generate_video(
    user_prompt="Shapes: circle, square, and triangle with labels",
    use_3d=False,  # Explicitly use 2D
    output_name="2d_shapes"
)
```

## Parameter Configuration

### For Performance
```python
# Fast rendering (less detail)
# Gemini will generate with low resolution
result = generator.generate_video(
    "3D visualization",
    use_3d=True
    # Automatically uses -ql (low quality) flag with 180s timeout
)
```

### For Quality
```python
# Better quality (slower rendering)
# Note: Need to manually increase timeout in code
result = generator.generate_video(
    "3D visualization",
    use_3d=True  
    # Current: uses -ql flag, can modify execute_manim() to use -qm
)
```

## Writing Good 3D Prompts

### ✅ DO:
- **Be specific about rotation**: "rotate 360 degrees showing all faces"
- **Mention visual clarity**: "clearly show the 3D structure"
- **Specify objects clearly**: "sphere, cube, and cylinder"
- **Include camera perspective**: "view from multiple angles"
- **Use timing guidance**: "slowly rotate over 10 seconds"

### ❌ DON'T:
- **Be too vague**: "show something 3D" (too generic)
- **Ask for complex physics**: "simulate realistic gravity" (not supported)
- **Request lighting effects**: "with advanced lighting" (limited support)
- **Mix too many shapes**: "show 10 different 3D objects" (performance issues)

## Best Practices

### 1. Prompt Structure
```
Good 3D prompt template:
"[Verb] a [shape/object] in 3D space [doing action]. 
Show [specific detail] and [specific detail]. 
Camera should be at [angle/position]."

Example:
"Rotate a sphere in 3D space with camera view from 45 degrees. 
Show the sphere changing colors as it rotates. 
Camera should zoom in during rotation."
```

### 2. Performance Tuning
- For testing: Keep it simple with 1-2 shapes
- For production: Use pre-rendered videos when possible
- Monitor the output for quality before wide deployment

### 3. Educational Value
- **Caption**: Use narration to explain what's happening
- **Pace**: Keep rotations slow enough to follow
- **Focus**: Highlight important features, hide unnecessary details

## Common 3D Scenes

### Rotating Cube
```
Prompt: "Animate a cube rotating 360 degrees on the Z-axis, 
showing all six faces clearly. Include the cube changing color 
as it completes the rotation."

Expected: Clean 3D rotation, educational, ~30s
```

### Molecular Structure
```
Prompt: "Show the water molecule (H2O) in 3D space. 
Display one oxygen atom in the center with two hydrogen atoms 
bonded to it. Rotate slowly to show the 3D structure clearly."

Expected: 3 spheres arranged with bonds, slow rotation, ~30s
```

### Solar System Preview
```
Prompt: "Visualize the Sun and three planets in 3D space. 
Show the planets orbiting around the Sun in circular paths. 
Use different colors for each planet."

Expected: Multiple objects in orbital motion, ~30s
```

### DNA Double Helix
```
Prompt: "Animate a DNA double helix structure rotating in 3D. 
Show the twisted spiral structure clearly and include labels 
for the major and minor grooves."

Expected: Complex 3D visualization, ~30s
```

## Troubleshooting Tips

### If rendering is too slow:
1. Simplify the prompt: fewer objects, simpler rotations
2. Use 2D as alternative: `use_3d=False`
3. Reduce animation time: ask for "quick rotation" instead of slow

### If objects don't appear:
1. Check Manim installation
2. Verify 3D libraries are installed: `pip install manim`
3. Try simpler shape: "Show a sphere" instead of complex molecule

### If quality is poor:
1. This is expected at low quality (-ql flag)
2. For better quality, would need to modify code to use `-qm`
3. Trade-off: Quality vs rendering time

## Performance Benchmarks

| Complexity | Shapes | Time | Quality |
|-----------|--------|------|---------|
| Very Simple | 1 sphere | 20-30s | Low |
| Simple | 1 cube + rotation | 25-35s | Low |
| Moderate | 2-3 objects | 40-60s | Low |
| Complex | 4+ objects | 60-120s | Low |

## Advanced Tips

### For Developers
1. Set camera early in animation
2. Group related objects for synchronized animation
3. Use VGroup for compound objects
4. Add narration comments at key moments

### For Educators
1. Test prompts on simple examples first
2. Use 3D for objects that are inherently 3D
3. Fall back to 2D for 2D concepts
4. Keep videos under 30 seconds for engagement

### For Content Creators
1. Mix 2D and 3D for variety
2. Use 3D for "wow factor" moments
3. Use 2D for detailed explanations
4. Combine multiple short videos for longer content
