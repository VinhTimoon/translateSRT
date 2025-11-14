# Translation Prompts Reference

## System Prompt (Fixed)

Used for all translation requests:

```
You are a professional translator model. Translate Chinese subtitle lines to Vietnamese. Output must be a JSON array of strings only (e.g. ["...", "..."]). Do NOT include indices, timestamps, explanations, or any other text. Preserve the number and order of lines exactly as input. Remove any leading numbering in the input lines before translating. Use natural conversational Vietnamese fitting film subtitles. Keep translations concise, preserve tone, and maintain name consistency (use provided name_map). If unsure, translate literally but natural. If input is empty string, output empty string for that line. Output must be valid JSON.
```

## User Prompt Template (Dynamic per Chunk)

```
NameMap: {name_map_json}
Tone: {conversational|formal|literal}
ChunkIndices: [{start_index}-{end_index}]
Lines: {array_of_chinese_lines}

Translate the Lines array from Chinese to Vietnamese. Return a JSON array of {count} strings only. Ensure the i-th output corresponds to the i-th input line. DO NOT add numbering or timestamps. DO NOT change punctuation meaningfully. If a name appears that is in NameMap, use that Hán-Việt mapping. If the translated line still contains Chinese characters, that counts as invalid.
```

## Example 1: Simple Translation

**User Prompt:**
```
NameMap: {}
Tone: conversational
ChunkIndices: [1-3]
Lines: ["加班猝死", "我串到了狗血大同小说", "好消息猝死后穿越活了坏消息"]

Translate the Lines array from Chinese to Vietnamese. Return a JSON array of 3 strings only. Ensure the i-th output corresponds to the i-th input line. DO NOT add numbering or timestamps. DO NOT change punctuation meaningfully.
```

**Expected Response:**
```json
[
  "Làm thêm giờ đến chết",
  "Tôi xuyên vào tiểu thuyết huyết cẩu Đại Đồng",
  "Tin tốt là chết rồi xuyên việt còn sống, tin xấu là"
]
```

## Example 2: With Name Mapping

**User Prompt:**
```
NameMap: {"张伟": "Trương Vĩ", "李芳": "Lý Phương"}
Tone: formal
ChunkIndices: [10-12]
Lines: ["张伟对李芳说", "你好吗", "我很好谢谢"]

Translate the Lines array from Chinese to Vietnamese. Return a JSON array of 3 strings only. Ensure the i-th output corresponds to the i-th input line. DO NOT add numbering or timestamps. DO NOT change punctuation meaningfully. If a name appears that is in NameMap, use that Hán-Việt mapping.
```

**Expected Response:**
```json
[
  "Trương Vĩ nói với Lý Phương",
  "Bạn khỏe không",
  "Tôi rất khỏe, cảm ơn"
]
```

## Example 3: Literal Tone

**User Prompt:**
```
NameMap: {}
Tone: literal
ChunkIndices: [5-6]
Lines: ["这简直太棒了", "我不敢相信"]

Translate the Lines array from Chinese to Vietnamese. Return a JSON array of 2 strings only. Ensure the i-th output corresponds to the i-th input line. DO NOT add numbering or timestamps.
```

**Expected Response (Literal):**
```json
[
  "Điều này thực sự tuyệt vời",
  "Tôi không dám tin"
]
```

## Tone Guidelines

### Conversational (Default)
- Natural spoken Vietnamese
- Suitable for films and TV shows
- Can use colloquialisms
- Example: "你好" → "Chào bạn" or "Xin chào"

### Formal
- Polite, professional Vietnamese
- Suitable for documentaries, news
- Avoid slang
- Example: "你好" → "Xin chào"

### Literal
- Word-for-word when possible
- Preserve structure and meaning
- Less natural but accurate
- Example: "你好" → "Bạn tốt" (though rarely used)

## Common Issues and Solutions

### Issue: Model adds numbering

**Bad Response:**
```json
["1. Xin chào", "2. Tạm biệt"]
```

**Solution:** App automatically strips numbering with regex:
```python
^\s*\d+\s*[\.\)、]\s*
```

### Issue: Model returns wrong count

**Bad Response (asked for 3, got 2):**
```json
["Line 1", "Line 2"]
```

**Solution:** App rejects and retries with fallback APIs

### Issue: Translation still has Chinese

**Bad Response:**
```json
["Xin chào 世界"]
```

**Solution:** App detects with CJK regex and retries

## Testing Your Prompts

Use this curl command to test prompts directly:

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=YOUR_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "contents": [
      {
        "parts": [
          {"text": "SYSTEM_PROMPT_HERE"},
          {"text": "USER_PROMPT_HERE"}
        ]
      }
    ],
    "generationConfig": {
      "temperature": 0.3,
      "topK": 40,
      "topP": 0.95,
      "maxOutputTokens": 2048
    }
  }'
```

## Best Practices

1. **Keep prompts concise**: Gemini performs better with clear instructions
2. **Specify output format**: Always request JSON array
3. **Provide context**: Name map and tone help consistency
4. **Set expectations**: Mention what NOT to do (no indices, etc.)
5. **Test with samples**: Try prompts on representative data first

## Customizing Prompts

To modify prompts, edit `core/config.py`:

```python
# System prompt
SYSTEM_PROMPT = """Your custom system prompt..."""

# User prompt builder
def build_user_prompt(self, lines, start_idx, end_idx):
    # Customize this method
    pass
```

## Advanced: Multi-language Support

To extend to other languages, modify prompts:

```
Translate Chinese subtitle lines to [TARGET_LANGUAGE]...
```

And update validation to check for appropriate characters.
