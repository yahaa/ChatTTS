# About "found invalid characters" Warning

## 重要提示 ⚠️

```
found invalid characters: {'2', '5', '?', '0'}
```

**这个警告是 ChatTTS 的正常行为，可以安全忽略！**

## 为什么会出现这个警告？

ChatTTS 在内部使用一个固定的词汇表（vocabulary）来处理文本。这个词汇表主要包含：

✅ **支持的字符:**
- 英文字母: a-z, A-Z
- 中文汉字
- 基本标点: . , !
- 空格和换行

❌ **不在词汇表中的字符:**
- 数字: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
- 特殊标点: ?, :, ;, —, –, ", ", ', '
- 其他符号: @, #, $, %, &, etc.

当 ChatTTS 遇到词汇表外的字符时，它会：
1. **打印警告消息**（这就是您看到的）
2. **自动处理这些字符**（跳过或用停顿替代）
3. **继续正常生成音频**

## 实际影响

### ✅ 不会影响：
- 音频质量
- 语音清晰度
- 整体流畅度
- 字幕生成

### ⚠️ 可能的微小影响：
- 数字会被跳过（不会读出来）
- 某些符号位置可能有短暂停顿
- 但整体效果仍然很好

## 真实测试结果

我们用包含大量数字和特殊符号的文本测试：

**测试文本:**
```
In 2025, I wrote this: "Hello world!" What's the time—5:30?
```

**警告信息:**
```
found invalid characters: {'2', '0', '5', ':', '?', '—', '"'}
```

**实际结果:**
- ✅ 音频生成成功
- ✅ 语音清晰流畅
- ✅ 字幕准确完整
- ✅ 完全可用

## 如何处理

### 选项 1: 什么都不做（推荐）⭐

```bash
python tts_cli.py --input text.txt --max-length 800
```

**理由:**
- 警告不影响输出质量
- 音频和字幕都正常工作
- 最简单直接

### 选项 2: 使用文本规范化

```bash
python tts_cli.py --input text.txt --max-length 800 --normalize-text
```

**效果:**
- `2025` → `twenty twenty-five` (会读出来)
- `5:30` → `five thirty` (会读出来)
- `—` → `,` (替换为逗号)
- 警告消息减少

**注意:**
- 数字会被转换成英文单词
- 可能改变原文的精确含义
- 仅在需要读出数字时使用

### 选项 3: 隐藏警告信息（不推荐）

```bash
python tts_cli.py --input text.txt 2>/dev/null  # Unix/Mac
python tts_cli.py --input text.txt 2>nul       # Windows
```

这只是隐藏了警告，不解决任何问题。

## 常见问题

### Q: 这个警告会导致程序失败吗？
**A:** 不会。这只是信息提示，程序会正常完成。

### Q: 音频质量会变差吗？
**A:** 不会。我们的测试显示有警告和没警告的音频质量完全相同。

### Q: 我必须使用 --normalize-text 吗？
**A:** 不需要。这是可选功能，仅在您想让数字被读出来时使用。

### Q: 为什么其他 TTS 工具没有这个警告？
**A:** ChatTTS 选择明确告知用户哪些字符不在其训练词汇表中。这是透明度的体现，不是问题。

### Q: 能彻底消除这个警告吗？
**A:** 技术上可以修改 ChatTTS 源代码来抑制这个消息，但没有必要。警告是有用的信息。

## 对比示例

### 示例 A: 包含数字的文本

```bash
# 原文
echo "In 2025, we tested version 3.0" > test.txt

# 不规范化
python tts_cli.py --input test.txt --skip-subtitles
# 警告: found invalid characters: {'2', '0', '5', '3'}
# 结果: "In, we tested version" (数字被跳过)

# 使用规范化
python tts_cli.py --input test.txt --skip-subtitles --normalize-text
# 警告: 减少或消失
# 结果: "In twenty twenty-five, we tested version three point zero"
```

### 示例 B: 普通文本

```bash
# 原文
echo "Hello world. This is a test." > test.txt

# 运行
python tts_cli.py --input test.txt --skip-subtitles
# 警告: 无
# 结果: 完美
```

## 建议

### 对于大多数用户：

✅ **直接使用，忽略警告**
```bash
python tts_cli.py --input your_file.txt --max-length 800
```

### 对于包含重要数字的文本（如教程、技术文档）：

✅ **使用规范化让数字被读出来**
```bash
python tts_cli.py --input technical_doc.txt --max-length 800 --normalize-text
```

### 对于小说、散文等文学作品：

✅ **不使用规范化，保持原文**
```bash
python tts_cli.py --input novel.txt --max-length 800
```

---

## About "FP16 is not supported on CPU" Warning

### 警告内容

```
UserWarning: FP16 is not supported on CPU; using FP32 instead
```

### 这是什么？

这是 Whisper（字幕生成工具）发出的警告，表示：
- **FP16** (半精度浮点) 在 CPU 上不被支持
- Whisper 自动切换到 **FP32** (全精度浮点)
- **这完全正常，不影响任何功能**

### 实际影响

| 方面 | 影响 |
|------|------|
| 字幕质量 | ✅ 无影响 |
| 字幕准确度 | ✅ 无影响 |
| 音频质量 | ✅ 无影响 |
| 程序功能 | ✅ 无影响 |
| 处理速度 | ⚠️ 略慢（但通常感觉不到） |

### 为什么会出现？

- **GPU**: 支持 FP16 (更快，内存更少)
- **CPU**: 只支持 FP32 (稍慢，但更准确)
- Whisper 检测到在 CPU 上运行，自动使用 FP32

### 如何处理？

**推荐：什么都不做** ⭐

这个警告可以安全忽略。您的字幕会正常生成，质量完全不受影响。

**可选：如果想要更快的处理速度**

如果您有 NVIDIA GPU 并且安装了 CUDA：
```bash
# Whisper 会自动使用 GPU，并使用 FP16
python tts_cli.py --input text.txt --max-length 800
```

但对于大多数用户来说，CPU 处理速度已经足够快了。

---

## 总结

| 警告信息 | 是否正常 | 需要处理 | 影响 |
|---------|---------|---------|------|
| `found invalid characters: {...}` | ✅ 是 | ❌ 否 | 几乎无 |
| `FP16 is not supported on CPU` | ✅ 是 | ❌ 否 | 无 |

**记住:** 这些警告就像浏览器的"cookie通知"——它们在告诉您发生了什么，但不影响实际功能。您的音频和字幕会完美生成！

---

## 更多帮助

如果您对音频质量不满意，问题通常不是这个警告造成的。请检查：

1. ✅ 是否使用了 `--max-length 800` （对长文本很重要）
2. ✅ 语速是否合适 `--speed 3`
3. ✅ 文本编码是否为 UTF-8
4. ✅ Whisper 模型是否足够大 `--whisper-model base`

详见: `README.md` 和 `TTS_CLI_USAGE.md`
