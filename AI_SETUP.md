# AI-Powered Video Generator Setup

## Get Your Free Gemini API Key

1. **Go to Google AI Studio:**
   https://makersuite.google.com/app/apikey

2. **Click "Get API Key"**

3. **Create a new API key** (free tier includes generous limits)

4. **Copy your API key**

## Set Up the API Key

### Option 1: Environment Variable (Recommended)

**Windows CMD:**
```cmd
setx GEMINI_API_KEY "your-api-key-here"
```

**Windows PowerShell:**
```powershell
$env:GEMINI_API_KEY = "your-api-key-here"
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "your-api-key-here", "User")
```

**Restart your terminal** after setting the variable!

### Option 2: Create .env file

Create a file named `.env` in the project folder:
```
GEMINI_API_KEY=your-api-key-here
```

## Install Required Package

```cmd
pip install google-generativeai
```

## How It Works

Once configured, just enter **ANY topic** in the web UI:

- "Explain gravity and orbital mechanics"
- "How does DNA replication work?"
- "The process of volcanic eruption"
- "How batteries store energy"
- "The nitrogen cycle in nature"

The AI will:
1. ✨ **Design custom animations** for your topic
2. 🎨 **Choose appropriate colors** (sun=yellow, water=blue, etc)
3. 📍 **Position elements** logically
4. 🎬 **Create smooth animations** (movement, rotation, particles)
5. 🏷️ **Add labels** for key concepts

## Test It

```cmd
# Make sure API key is set
echo %GEMINI_API_KEY%

# Run the test
python ai_generator.py
```

## Without AI (Fallback)

If you don't set an API key, the system automatically uses the optimized generator (works for photosynthesis and a few predefined topics).

## Free Tier Limits

Google Gemini free tier:
- ✅ 60 requests per minute
- ✅ 1500 requests per day
- ✅ More than enough for personal use!

## Example Topics to Try

1. **Science:** "Photosynthesis", "Cell division", "Chemical reactions"
2. **Physics:** "Newton's laws", "Electricity flow", "Sound waves"
3. **Biology:** "Heart pumping blood", "Respiratory system", "Digestion"
4. **Chemistry:** "Atomic bonding", "pH scale", "States of matter"
5. **Geography:** "Rock cycle", "Plate tectonics", "Water cycle"

The AI will create appropriate animations for ANY educational topic! 🚀
