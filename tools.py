"""
ChatTTS 字幕生成示例
使用 Whisper 自动生成 SRT 字幕文件

安装依赖：
pip install openai-whisper scipy numpy

使用方法：
python generate_subtitles.py
"""

import ChatTTS
import torch
import scipy.io.wavfile as wavfile
import numpy as np
import whisper
import json
import os


def format_timestamp(seconds):
    """
    将秒数转换为 SRT 时间格式 (HH:MM:SS,mmm)
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)

    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def generate_srt(whisper_result, output_file):
    """
    从 Whisper 结果生成 SRT 字幕文件
    """
    with open(output_file, "w", encoding="utf-8") as f:
        for i, segment in enumerate(whisper_result["segments"], 1):
            start_time = format_timestamp(segment["start"])
            end_time = format_timestamp(segment["end"])
            text = segment["text"].strip()

            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n")
            f.write("\n")


def generate_audio_with_subtitles(
    text, output_audio="output.wav", output_srt="output.srt", speed=3, language="en"
):
    """
    生成音频并自动生成字幕

    参数:
        text: 要转换的文本
        output_audio: 输出音频文件
        output_srt: 输出字幕文件
        speed: 语速 (0-9，推荐 2-4)
        language: 语言代码 ("en" 或 "zh")
    """

    print("=" * 70)
    print("ChatTTS 音频 + 字幕生成工具")
    print("=" * 70)

    # ========================================
    # 步骤 1: 使用 ChatTTS 生成音频
    # ========================================
    print("\n🎙️  步骤 1/3: 生成音频...")
    print(f"   速度参数: speed_{speed}")

    chat = ChatTTS.Chat()
    print("   正在加载 ChatTTS 模型...")
    chat.load(compile=False)

    # Audio generation parameters (controls quality and completeness)
    params_infer_code = ChatTTS.Chat.InferCodeParams(
        prompt=f"[speed_{speed}]",  # Speed control belongs here
        temperature=0.3,             # Lower = more stable/clear pronunciation
        top_P=0.7,                   # Nucleus sampling for quality
        top_K=20,                    # Limit token selection
        repetition_penalty=1.05,     # Reduce repetition
        max_new_token=2048,          # Ensure complete audio generation
        ensure_non_empty=True,       # Guarantee non-empty output
    )

    print("   正在生成语音...")
    wavs = chat.infer(
        [text],
        skip_refine_text=True,           # Skip GPT text refinement for raw English text
        params_infer_code=params_infer_code,
        use_decoder=True,
        do_text_normalization=False,      # Disable - may cause issues with English
        do_homophone_replacement=False,   # Disable - mainly for Chinese
        split_text=True,                  # Handle long text properly
        max_split_batch=10,               # Increase from default 4 to handle longer text
    )

    # 保存音频
    audio_data = (wavs[0] * 32767).astype(np.int16)
    wavfile.write(output_audio, 24000, audio_data)

    duration = len(wavs[0]) / 24000
    print(f"   ✅ 音频已保存: {output_audio}")
    print(f"   ⏱️  时长: {duration:.2f} 秒")

    # ========================================
    # 步骤 2: 使用 Whisper 识别并生成时间戳
    # ========================================
    print(f"\n🎯 步骤 2/3: 识别语音并生成时间戳...")
    print(f"   语言: {language}")

    # 检查 Whisper 是否已安装
    try:
        print("   正在加载 Whisper 模型...")
        model = whisper.load_model("base")  # 可选: tiny, base, small, medium, large
    except Exception as e:
        print(f"   ❌ 错误: 无法加载 Whisper 模型")
        print(f"   请确保已安装: pip install openai-whisper")
        return None

    print("   正在识别音频...")
    result = model.transcribe(
        output_audio,
        language=language,
        word_timestamps=True,  # 启用词级时间戳
        verbose=False,
    )

    print(f"   ✅ 识别完成")
    print(f"   📝 识别文本: {result['text'][:100]}...")

    # ========================================
    # 步骤 3: 生成 SRT 字幕文件
    # ========================================
    print(f"\n📄 步骤 3/3: 生成字幕文件...")

    generate_srt(result, output_srt)
    print(f"   ✅ SRT 字幕已保存: {output_srt}")

    # 同时生成 JSON 格式（包含详细信息）
    output_json = output_srt.replace(".srt", ".json")
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"   ✅ JSON 数据已保存: {output_json}")

    # ========================================
    # 输出统计信息
    # ========================================
    print(f"\n📊 统计信息:")
    print(f"   音频时长: {duration:.2f} 秒")
    print(f"   字幕段数: {len(result['segments'])} 段")
    print(f"   总字符数: {len(result['text'])} 字符")
    print(f"   平均语速: {len(result['text']) / duration:.1f} 字符/秒")

    print("\n" + "=" * 70)
    print("🎉 全部完成！")
    print("=" * 70)
    print("\n生成的文件:")
    print(f"   1. {output_audio} - 音频文件")
    print(f"   2. {output_srt} - SRT 字幕文件")
    print(f"   3. {output_json} - JSON 详细信息")
    print("\n💡 提示: 你可以用视频播放器加载字幕文件查看效果")
    print("=" * 70 + "\n")

    return result


# ========================================
# 使用示例
# ========================================
if __name__ == "__main__":
    # 示例 1: 英文文本
    english_text = """
    On a catchup call, I told my friend Nick Wignall how someone had trained an AI model to write blog posts in my style. It was a pure research exercise on their part. The idea was to train the tool on my past work, then give it the headlines and opening paragraphs of my 2025 posts. Could it generate the rest of each piece in a similar fashion?

I only compared a handful of posts from their AI versions to their originals, but I quickly concluded the writing suffered from the same uncanny valley effect as many AI-generated images: It all looks fine enough at first glance, but pay attention just a little longer, and something feels off. The AI would veer off in a different direction or end up making the opposite argument. It sounded confident where I would have been doubtful and vice versa. And so on.

The creator wanted to know if such a model—once it worked properly, of course—could be useful to me. I told him even if it worked perfectly it wouldn’t. Why? Because I don’t write a daily blog to crank out a post every day. If that was the point, I’d have switched to AI long ago already. I write a daily blog to make sure I remember how to think. It’s a daily practice for my brain. A creative ritual to strengthen my writing muscles. And a commitment to my readers. A promise that I’ll show up for them once a day. AI can generate output, but it can’t give me any of these benefits. The output is secondary. If it happens to attract new readers, all the better. And if not? That’s fine too.

Nick said my story reminded him of an interview with writer and Vox-founder Ezra Klein. Klein explained that, so far, AI hasn’t been all that useful to him. He uses it for light research or to structure some data, but that’s about it. Why? Because the writer doing the research is what makes the writing unique.

When you’re using AI as a writer, you’re “outsourcing the part of the work [you] need to do the most,” Klein believes. “Having AI summarize a book or a paper for me is a disaster. It has no idea what I really wanted to know. It would not have made the connections I would have made.” This is why reading actual books in full might now be more valuable than it ever has been: Only if you’ve seen every word will you discover insights and links an AI would never include in its average-driven summary.

Nick pointed out the same applies to a writer struggling when creating a piece. “When you’re stuck and sit there, thinking, trying to come up with what’s next, that’s the valuable part of writing. It’s tempting to use AI to remove that stuck-ness, but it’s basically cheating—and leads to a very different result.” AI is great at giving you a list of ideas. You’ll almost always find one you can plug in and keep writing. But is it the idea that needs to slot into this gap? Or just a bad piece of filler that’ll make for a fragile mental bridge most readers won’t dare to cross?

The more I think about it, the happier I am that AI is transforming the world of writing. In a way, I think it’ll make it even easier to stand out—because the more people take shortcuts, the less quality will remain for readers to flock to, even if the overall quantity of options is much larger.

Whenever technology makes it feel like you can avoid the suck, it’s most likely a mirage. The path behind easy only leads to the lowest common denominator. The real artists, fighters, makers—they stick with a truth as old as time itself: The suck is why we’re here, and only those who overcome it themselves will reap all the rewards of their hard labor.
    """

    print("\n📌 示例 1: 英文字幕生成")
    result1 = generate_audio_with_subtitles(
        text=english_text,
        output_audio="demo_english.wav",
        output_srt="demo_english.srt",
        speed=2,
        language="en",
    )

    print("\n" + "=" * 70)
    print("✨ 所有示例已完成！")
    print("=" * 70)
    print("\n生成的所有文件:")
    print("   英文:")
    print("     - demo_english.wav")
    print("     - demo_english.srt")
    print("     - demo_english.json")
