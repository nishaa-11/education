# AI Manim Video Generation Pipeline

## How It Works

### The Complete Pipeline:

```
User Prompt → Gemini Elaborates → Gemini Generates Manim Code → Execute Manim → Final Video
```

### Step-by-Step:

**1. User Input**
- You type: "how step by step animated instructions on how to create a circle"

**2. Gemini Elaborates (AI Step 1)**
- Gemini creates detailed educational content:
  - Title
  - Narration script (4-6 sentences)
  - Key visual elements to animate
  - Animation flow/sequence

**3. Gemini Generates Manim Code (AI Step 2)**
- Gemini writes actual Python/Manim code:
  ```python
  class EducationScene(Scene):
      def construct(self):
          # Create circle
          circle = Circle(radius=2, color=BLUE)
          self.play(Create(circle))
          # ... etc
  ```

**4. Execute Manim**
- The generated code is saved to a temporary `.py` file
- Manim CLI is executed: `manim -ql scene.py EducationScene`
- Manim renders the animation using its professional engine

**5. Final Video**
- High-quality animated video is output
- Includes all Manim effects: smooth curves, LaTeX math, professional animations

## Test It

```cmd
python test_ai.py
```

## Use It via API

```cmd
python app.py
```

Then go to http://localhost:5000 and type any educational prompt!

## Example Prompts to Try

1. "how to draw a circle step by step"
2. "explain pythagoras theorem with animation"
3. "show how addition works with visual objects"
4. "demonstrate the area of a triangle"
5. "animate the concept of prime numbers"
6. "explain how fractions work visually"

## Requirements

- ✅ Manim Community Edition installed
- ✅ FFmpeg installed
- ✅ GEMINI_API_KEY in .env
- ✅ Python packages: google-generativeai, python-dotenv

## What Makes This Different

**Before:** Manual PIL drawings, simple shapes, no professional animations

**Now:** 
- ✨ AI generates custom Manim code for ANY topic
- 🎨 Professional animations with smooth curves, transformations
- 📐 LaTeX math support for formulas
- 🎬 Full Manim feature set (Create, Transform, FadeIn, etc.)
- 🤖 Completely automated from prompt to video

## Troubleshooting

If Manim fails:
1. Check Manim is installed: `manim --version`
2. Check FFmpeg is installed: `ffmpeg -version`
3. Check the generated code in console output
4. Try running manually: `manim scene.py EducationScene`
