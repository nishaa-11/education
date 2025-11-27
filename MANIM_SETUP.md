# Manim Prerequisites for Windows

## What You Need to Install:

### 1. **FFmpeg** (Required)
FFmpeg is needed for video encoding.

**Installation:**
```cmd
# Option 1: Using Chocolatey (easiest)
choco install ffmpeg

# Option 2: Manual Install
1. Download from: https://github.com/BtbN/FFmpeg-Builds/releases
2. Extract to C:\ffmpeg
3. Add C:\ffmpeg\bin to your PATH environment variable
```

**Verify:**
```cmd
ffmpeg -version
```

### 2. **LaTeX** (Optional but recommended for math equations)
Needed for MathTex (mathematical equations).

**Installation:**
```cmd
# Option 1: MiKTeX (lighter, recommended)
Download from: https://miktex.org/download
Install with default settings

# Option 2: TeX Live (full)
Download from: https://www.tug.org/texlive/windows.html
```

**Verify:**
```cmd
latex --version
```

### 3. **Cairo + Pango** (For text rendering)
Already included in Manim 0.19.0 for Python 3.13!

---

## Quick Setup (Recommended):

```cmd
# 1. Install Chocolatey (if not already installed)
# Open PowerShell as Administrator and run:
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 2. Install FFmpeg
choco install ffmpeg -y

# 3. Install MiKTeX (optional, for math)
choco install miktex -y

# 4. Verify installations
ffmpeg -version
latex --version
```

---

## If You Skip LaTeX:
You can still use Manim! Just avoid `MathTex` and use `Text` instead (which we already did in the code).

---

## Alternative: Use the Optimized Generator (No Manim needed!)
The `optimized_generator.py` we just created requires **ZERO external dependencies** beyond Python packages:
- No FFmpeg needed (MoviePy handles it)
- No LaTeX needed
- No Cairo/Pango needed
- Just: `pip install -r requirements.txt`

**This is the recommended approach for reliability!**

---

## Current Setup Status:
✅ Python 3.13 installed
✅ MoviePy installed
✅ PIL/Pillow installed
❓ FFmpeg (check with: `ffmpeg -version`)
❓ LaTeX (optional)

---

## Test Your Setup:
```cmd
# Test optimized generator (works now!)
python optimized_generator.py

# Test Manim (only if FFmpeg + LaTeX installed)
python manim_generator.py
```
