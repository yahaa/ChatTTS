# Text Normalization Feature

## What it does

The `--normalize-text` option converts problematic characters to TTS-friendly text:

### Conversions Applied

1. **Years**: `2025` → `twenty twenty-five`
2. **Time**: `5:30` → `five thirty`
3. **Single digits**: `3` → `three`
4. **Numbers 1-20**: `15` → `fifteen`
5. **Dashes**: `—` → `, ` (comma + space)
6. **Colons**: `:` → `, `
7. **Smart quotes**: `"text"` → `text`
8. **Newlines**: Multiple newlines → single space

## Usage

```bash
# With normalization
python tts_cli.py --input text.txt --normalize-text

# Without normalization (default)
python tts_cli.py --input text.txt
```

## Example

**Original text:**
```
In 2025, I wrote this: Hello world! What's the time—5:30?
```

**Normalized text:**
```
In twenty twenty-five, I wrote this, Hello world! What's the time, five thirty?
```

## When to use

✅ **Use `--normalize-text` if:**
- Text contains many numbers or special punctuation
- You want to minimize warning messages
- Text has dates, times, or measurements

❌ **Don't use if:**
- Text is already clean (only letters and basic punctuation)
- You want numbers spoken as digits
- Processing poetry or creative text where formatting matters

## Note

Even without normalization, ChatTTS handles most text well. The warnings are informational and rarely affect output quality.
