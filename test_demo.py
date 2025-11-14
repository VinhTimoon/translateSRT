"""
Demo script to test core components without GUI.
Useful for debugging and testing API connectivity.
"""

import asyncio
from pathlib import Path

from core.config import ConfigManager
from core.parser import SRTParser, Chunker, export_srt, read_srt_file
from core.translator import TranslationDispatcher
from core.validator import TranslationValidator


async def test_translation():
    """Test translation with sample data."""
    
    print("🔧 SRT Translator - Component Test\n")
    
    # Initialize config
    print("1️⃣ Initializing configuration...")
    config = ConfigManager()
    
    errors = config.validate_config()
    if errors:
        print("❌ Configuration errors:")
        for error in errors:
            print(f"   - {error}")
        return
    
    print(f"✓ Configuration valid")
    print(f"✓ Primary APIs: {len(config.get_primary_apis())}")
    print(f"✓ Fallback APIs: {len(config.get_fallback_apis())}")
    print(f"✓ Model: {config.settings.model}")
    print()
    
    # Load sample SRT
    print("2️⃣ Loading sample SRT file...")
    sample_file = Path(__file__).parent / "resources" / "sample.srt"
    
    if not sample_file.exists():
        print(f"❌ Sample file not found: {sample_file}")
        return
    
    content = read_srt_file(str(sample_file))
    times, subs = SRTParser.parse(content)
    
    if not SRTParser.validate(times, subs):
        print("❌ Invalid SRT format")
        return
    
    count = SRTParser.get_count(subs)
    print(f"✓ Loaded {count} subtitle lines")
    print()
    
    # Show first few lines
    print("📄 Preview (first 3 lines):")
    for i in range(1, min(4, len(subs))):
        print(f"   [{i}] {times[i]}")
        print(f"       {subs[i]}")
        print()
    
    # Create chunks
    print("3️⃣ Creating chunks...")
    chunks = Chunker.chunkify(subs, chunk_size=config.settings.chunk_size)
    print(f"✓ Created {len(chunks)} chunks")
    print()
    
    # Translate
    print("4️⃣ Starting translation...")
    print(f"   (This will take ~{len(chunks) * 2}-{len(chunks) * 5} seconds)")
    print()
    
    async with TranslationDispatcher(config) as dispatcher:
        # Progress callback
        def progress(current, total, message):
            print(f"   [{current}/{total}] {message}")
        
        dispatcher.set_progress_callback(progress)
        
        # Translate all chunks
        results = await dispatcher.translate_chunks(chunks)
        
        # Get stats
        stats = dispatcher.get_stats()
        
        print()
        print("✓ Translation complete!")
        print()
        print(f"📊 Statistics:")
        print(f"   Total chunks: {stats.total_chunks}")
        print(f"   Successful: {stats.success_count}")
        print(f"   Failed: {stats.failed_count}")
        print(f"   Success rate: {stats.success_count / stats.total_chunks * 100:.1f}%")
        print(f"   Duration: {stats.total_duration:.2f}s")
        print(f"   API usage: {stats.api_usage}")
        print()
    
    # Merge results
    print("5️⃣ Merging results...")
    subs_translated = Chunker.merge_results(subs, chunks, results)
    print()
    
    # Validate translations
    print("6️⃣ Validating translations...")
    chinese_count = 0
    for i in range(1, len(subs_translated)):
        if TranslationValidator.contains_chinese(subs_translated[i] or ""):
            chinese_count += 1
    
    if chinese_count > 0:
        print(f"⚠️  {chinese_count} lines still contain Chinese")
    else:
        print("✓ All lines successfully translated to Vietnamese")
    print()
    
    # Show results
    print("📄 Results (first 3 lines):")
    for i in range(1, min(4, len(subs_translated))):
        print(f"   [{i}] Original: {subs[i]}")
        print(f"       Translated: {subs_translated[i]}")
        print()
    
    # Export
    print("7️⃣ Exporting SRT...")
    output_file = Path(__file__).parent / "output_test.srt"
    
    output_content = export_srt(times, subs_translated)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_content)
    
    print(f"✓ Exported to: {output_file}")
    print()
    
    print("✅ Test complete!")


def main():
    """Main entry point."""
    print("=" * 60)
    print("  SRT Translator - Component Test")
    print("=" * 60)
    print()
    
    try:
        asyncio.run(test_translation())
    except KeyboardInterrupt:
        print("\n⏹ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
