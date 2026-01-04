# ChatTTS CLI Tool with Auto-Splitting and Subtitles

A powerful command-line tool for generating high-quality speech audio and synchronized SRT subtitles.

## Features

✨ **Core Features:**
- 🎙️ High-quality text-to-speech using ChatTTS
- 📝 Automatic SRT subtitle generation with Whisper
- 🔄 **Auto text splitting** for long documents (NEW!)
- 🎭 Speaker voice saving and reuse
- 🌍 Multi-language support (English, Chinese)
- ⚡ Speed control (0-9)
- 🎨 Text normalization to reduce warnings

## Quick Start

```bash
# Basic usage
python tts_cli.py --text "Hello, world!"

# Long text with auto-splitting (recommended for 800+ characters)
python tts_cli.py --input article.txt --max-length 800

# Save and reuse voice for consistency
python tts_cli.py --input chapter1.txt --max-length 800 --save-speaker voice.pt
python tts_cli.py --input chapter2.txt --speaker voice.pt --max-length 800
```

## Installation

```bash
# Required dependencies
pip install torch torchaudio scipy numpy openai-whisper

# ChatTTS should already be installed in your environment
```

## Command-Line Options

### Input Options
- `--text "..."` - Direct text input
- `--input file.txt` - Read from file

### Output Options
- `--output-audio output.wav` - Audio file path (default: output.wav)
- `--output-srt output.srt` - Subtitle file path (default: auto-derived)

### Quality Options
- `--max-length 800` - **Auto-split long text** (recommended: 800)
- `--speed 3` - Speech speed 0-9 (default: 3)
- `--normalize-text` - Convert numbers and special chars to TTS-friendly text

### Voice Options
- `--speaker voice.pt` - Load saved speaker voice
- `--save-speaker voice.pt` - Save current speaker for reuse
- `--language en` - Language: 'en' or 'zh' (default: en)

### Subtitle Options
- `--whisper-model base` - Whisper model: tiny/base/small/medium/large
- `--skip-subtitles` - Generate audio only
- `--no-json` - Skip JSON output

### Other
- `--quiet` - Suppress progress, show only file paths

## Auto Text Splitting Feature

For texts longer than 800 characters, use `--max-length` to automatically split into chunks:

```bash
python tts_cli.py --input long_article.txt --max-length 800
```

**Benefits:**
- ✅ Each chunk generates higher quality audio
- ✅ Natural pacing and clear pronunciation  
- ✅ Better subtitle recognition accuracy
- ✅ Automatic merging with smooth transitions (0.3s silence)

**Performance Comparison** (3552 character text):

| Mode | Chunks | Duration | Subtitle Accuracy |
|------|--------|----------|-------------------|
| No split | 1 | 39s | Poor ❌ |
| `--max-length 800` | 5 | 155s | Excellent ✅ |

## Complete Examples

### Example 1: Simple Article
```bash
python tts_cli.py \
  --input article.txt \
  --output-audio article.wav \
  --speed 3
```

### Example 2: Long Document with Auto-Splitting
```bash
python tts_cli.py \
  --input long_essay.txt \
  --max-length 800 \
  --whisper-model base \
  --save-speaker essay_voice.pt
```

### Example 3: Multi-Chapter Book with Consistent Voice
```bash
# Chapter 1: Create voice
python tts_cli.py \
  --input chapter1.txt \
  --output-audio book_ch1.wav \
  --max-length 800 \
  --save-speaker book_voice.pt

# Chapters 2-N: Reuse voice
for i in {2..10}; do
  python tts_cli.py \
    --input chapter${i}.txt \
    --output-audio book_ch${i}.wav \
    --speaker book_voice.pt \
    --max-length 800
done
```

### Example 4: Clean Text with Normalization
```bash
python tts_cli.py \
  --input technical_doc.txt \
  --normalize-text \
  --max-length 800
```

## Output Files

Running: `python tts_cli.py --input example.txt`

Generates:
- ✅ `output.wav` - Audio file (24000 Hz, high quality)
- ✅ `output.srt` - SRT subtitle file
- ✅ `output.json` - Detailed transcription data

## Tips for Best Results

### For Long Texts (800+ chars)
```bash
python tts_cli.py --input text.txt --max-length 800 --speed 3
```

### For Maximum Quality
```bash
python tts_cli.py --input text.txt --max-length 800 --speed 2 --whisper-model medium
```

### For Speed
```bash
python tts_cli.py --input text.txt --skip-subtitles --speed 5
```

### For Consistency Across Multiple Files
```bash
# Always use the same speaker file
python tts_cli.py --input file1.txt --save-speaker voice.pt
python tts_cli.py --input file2.txt --speaker voice.pt
python tts_cli.py --input file3.txt --speaker voice.pt
```

## Troubleshooting

### "Invalid characters" warnings?
- **Usually harmless** - audio generates fine
- Use `--normalize-text` to reduce warnings
- See NORMALIZATION_GUIDE.md for details

### Poor audio quality?
- Use `--max-length 800` for long texts
- Lower `--speed` value (2-3)
- Ensure clean UTF-8 text encoding

### Inaccurate subtitles?
- Use larger Whisper model: `--whisper-model medium`
- First improve audio quality with `--max-length 800`
- Lower speech speed: `--speed 2`

## Documentation

- `TTS_CLI_USAGE.md` - Detailed usage guide with examples
- `NORMALIZATION_GUIDE.md` - Text normalization feature explanation

## License

Same as ChatTTS project.
