# API Configuration Guide

## Getting Gemini API Keys

1. **Go to Google AI Studio**: https://makersuite.google.com/app/apikey
2. **Create API Key**: Click "Create API Key"
3. **Copy the key**: Save it securely

## Setting up API Keys

### Method 1: Environment Variables (Recommended)

Create a `.env` file in the project root:

```bash
# Copy from .env.example
cp .env.example .env
```

Edit `.env` and add your keys:

```
GEMINI_PRIMARY_API1_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXX
GEMINI_PRIMARY_API2_KEY=AIzaSyYYYYYYYYYYYYYYYYYYYYYYYY
GEMINI_FALLBACK_API1_KEY=AIzaSyZZZZZZZZZZZZZZZZZZZZZZZZ
GEMINI_FALLBACK_API2_KEY=AIzaSyWWWWWWWWWWWWWWWWWWWWWWWW
```

### Method 2: Windows Environment Variables

```powershell
# Set permanently
[System.Environment]::SetEnvironmentVariable('GEMINI_PRIMARY_API1_KEY', 'your_key_here', 'User')

# Set for current session only
$env:GEMINI_PRIMARY_API1_KEY = "your_key_here"
```

## API Endpoint

Default endpoint (automatically configured):
```
https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent
```

The `{model}` placeholder is replaced with your selected model:
- `gemini-2.5-flash`
- `gemini-2.5-flash-lite`
- `gemini-2.0-flash`
- `gemini-2.0-flash-lite`

## Security Best Practices

1. **Never commit `.env` to Git**: Already in `.gitignore`
2. **Rotate keys regularly**: Especially if sharing code
3. **Use separate keys for development/production**
4. **Monitor usage**: Check Google Cloud Console for quota
5. **Restrict API key permissions**: Enable only necessary APIs

## Rate Limits

- **Free tier**: 60 requests/minute per API key
- **Paid tier**: Higher limits available
- **App behavior**: Automatically throttles to avoid limits

## Troubleshooting

### "API key not valid"
- Check if key is correctly copied (no spaces)
- Verify API is enabled in Google Cloud Console
- Try regenerating the key

### "Quota exceeded"
- Wait a minute and try again
- Use multiple API keys (already supported)
- Upgrade to paid tier

### "Model not found"
- Ensure model name is correct in dropdown
- Some models require allowlist access

## Multiple Keys Strategy

This app uses 4 keys by design:

1. **Primary API 1 & 2**: Main workhorses (5 threads each = 10 parallel)
2. **Fallback API 1 & 2**: Backup when primary fails (parallel retry)

You can use:
- Same key for all (simplest but may hit rate limits)
- Different keys for better throughput (recommended)
- Mix of free/paid keys

## Example Configuration

```env
# All different keys (best performance)
GEMINI_PRIMARY_API1_KEY=AIza...key1
GEMINI_PRIMARY_API2_KEY=AIza...key2
GEMINI_FALLBACK_API1_KEY=AIza...key3
GEMINI_FALLBACK_API2_KEY=AIza...key4

# Same key for all (simplest)
GEMINI_PRIMARY_API1_KEY=AIza...mykey
GEMINI_PRIMARY_API2_KEY=AIza...mykey
GEMINI_FALLBACK_API1_KEY=AIza...mykey
GEMINI_FALLBACK_API2_KEY=AIza...mykey
```

## Getting Help

If you encounter API issues:
1. Check https://ai.google.dev/gemini-api/docs
2. Review error logs in the app
3. Test API key with curl:

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=YOUR_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}'
```
