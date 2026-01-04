# TTS CLI Tool - Usage Guide

Command-line tool for generating high-quality speech audio and SRT subtitles using ChatTTS and Whisper.

## Quick Start

### Basic Usage
```bash
# Simple text-to-speech
python tts_cli.py --text "Hello, world!"

# From file
python tts_cli.py --input article.txt
```

## Key Features

### 1. Auto Text Splitting (NEW!)
For long texts (>800 chars), automatically splits into chunks for better audio quality:

```bash
# Automatically split long text for better quality
python tts_cli.py --input long_article.txt --max-length 800
```

**Benefits:**
- Each chunk generates higher quality audio
- Natural pacing and pronunciation
- Better subtitle recognition accuracy
- Chunks are merged automatically with smooth transitions

**Recommended max-length values:**
- 800 characters: Best quality (default recommendation)
- 1000 characters: Good balance
- 1200+ characters: May see quality degradation

### 2. Speaker Voice Management
Save and reuse speaker voices for consistency across multiple files:

```bash
# Save the voice for later use
python tts_cli.py --input chapter1.txt --save-speaker my_voice.pt

# Reuse the same voice
python tts_cli.py --input chapter2.txt --speaker my_voice.pt
python tts_cli.py --input chapter3.txt --speaker my_voice.pt
```

### 3. Speech Speed Control
Adjust speaking rate (0-9, higher = faster):

```bash
python tts_cli.py --input text.txt --speed 2  # Slower, clearer
python tts_cli.py --input text.txt --speed 5  # Faster
```

### 4. Language Support
```bash
# English (default)
python tts_cli.py --input english.txt --language en

# Chinese
python tts_cli.py --input chinese.txt --language zh
```

### 5. Subtitle Customization
```bash
# Use higher quality Whisper model
python tts_cli.py --input text.txt --whisper-model medium

# Skip subtitles (audio only)
python tts_cli.py --input text.txt --skip-subtitles

# Skip JSON output (SRT only)
python tts_cli.py --input text.txt --no-json
```

## Complete Example Workflow

### Scenario: Creating an audiobook with consistent voice

```bash
# Chapter 1: Generate and save voice
python tts_cli.py \
  --input chapter1.txt \
  --output-audio audiobook_ch1.wav \
  --max-length 800 \
  --save-speaker audiobook_voice.pt \
  --speed 3

# Chapter 2-N: Reuse the same voice
python tts_cli.py \
  --input chapter2.txt \
  --output-audio audiobook_ch2.wav \
  --speaker audiobook_voice.pt \
  --max-length 800 \
  --speed 3
```

## Performance Tips

### Text Length Guidelines

| Text Length | Recommended Approach | Expected Quality |
|------------|---------------------|------------------|
| < 200 chars | Direct generation | Excellent |
| 200-800 chars | Direct generation | Very Good |
| 800-3000 chars | Use `--max-length 800` | Good |
| 3000+ chars | Use `--max-length 800` + split manually | Good |

### Quality vs Speed

**Best Quality:**
```bash
python tts_cli.py --input text.txt --max-length 800 --speed 2 --whisper-model medium
```

**Fastest:**
```bash
python tts_cli.py --input text.txt --skip-subtitles --whisper-model tiny
```

**Balanced (Recommended):**
```bash
python tts_cli.py --input text.txt --max-length 800 --speed 3 --whisper-model base
```

## Output Files

For: `python tts_cli.py --input example.txt`

Generates:
- `output.wav` - Audio file (24000 Hz WAV format)
- `output.srt` - SRT subtitle file (compatible with all video players)
- `output.json` - Detailed Whisper transcription data

## Automation / Scripting

### Quiet Mode
Only outputs file paths (no progress messages):

```bash
python tts_cli.py --input data.txt --quiet > files.txt
```

### Batch Processing
```bash
for file in *.txt; do
  python tts_cli.py \
    --input "$file" \
    --output-audio "${file%.txt}.wav" \
    --speaker shared_voice.pt \
    --max-length 800 \
    --quiet
done
```

## Troubleshooting

### Poor Audio Quality
- Use `--max-length 800` for long texts
- Lower `--speed` value for clearer pronunciation
- Ensure text doesn't have encoding issues

### Inaccurate Subtitles
- Use larger Whisper model: `--whisper-model medium` or `large`
- Use `--max-length 800` for better audio quality first
- Lower speech speed: `--speed 2`

### Inconsistent Voice Across Files
- Always use `--speaker voice.pt` with the same voice file
- Generate the voice once with `--save-speaker` and reuse

### Out of Memory
- Use smaller chunks: `--max-length 600`
- Use smaller Whisper model: `--whisper-model tiny` or `base`

## Advanced Examples

### Multi-language Document
```bash
# English section
python tts_cli.py --input intro_en.txt --language en --save-speaker voice_en.pt

# Chinese section
python tts_cli.py --input content_zh.txt --language zh --save-speaker voice_zh.pt
```

### High-Quality Production
```bash
python tts_cli.py \
  --input script.txt \
  --output-audio final.wav \
  --output-srt final.srt \
  --max-length 800 \
  --speed 3 \
  --whisper-model large \
  --save-speaker production_voice.pt
```

## Dependencies

Required:
- Python 3.8+
- ChatTTS
- PyTorch
- scipy
- numpy
- openai-whisper (optional, only for subtitle generation)

Install:
```bash
pip install torch torchaudio scipy numpy openai-whisper
```

## FAQ

**Q: How long does it take to process 1000 characters?**
A: Approximately 30-60 seconds for audio generation + 10-30 seconds for subtitles (depends on hardware).

**Q: Can I use GPU acceleration?**
A: Yes! ChatTTS automatically uses CUDA if available. Whisper also benefits from GPU.

**Q: What's the maximum text length?**
A: No hard limit, but use `--max-length 800` for texts over 800 characters for best quality.

**Q: Are subtitles always accurate?**
A: Subtitle accuracy depends on audio quality and Whisper model size. Use `--whisper-model medium` or `large` for better accuracy.

**Q: Can I change the voice?**
A: Each run samples a random voice unless you specify `--speaker`. Save voices you like with `--save-speaker`.
