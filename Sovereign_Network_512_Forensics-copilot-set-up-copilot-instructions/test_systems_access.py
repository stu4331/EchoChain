"""
Test script to verify all background systems are accessible to the girls
Run this to confirm DNA, forensics, sandbox, spark, pride, and all other systems work
"""
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

def test_all_systems():
    print("=" * 70)
    print("ERRYN'S SOUL - SYSTEM ACCESS TEST")
    print("Verifying all sisters can access background systems...")
    print("=" * 70)
    print()
    
    results = []
    
    # Test DNA Heritage
    try:
        from dna_inheritance import dna_heritage
        seal = dna_heritage.get_sister_seal('erryn')
        sig = dna_heritage.sister_dna['erryn']['signature'][:16]
        results.append(("✅ DNA Heritage", f"Loaded. Erryn seal: {seal}, sig: {sig}..."))
    except Exception as e:
        results.append(("❌ DNA Heritage", str(e)))
    
    # Test Forensics
    try:
        from image_forensics import image_forensics
        results.append(("✅ Image Forensics", "Loaded. Can analyze images."))
    except Exception as e:
        results.append(("❌ Image Forensics", str(e)))
    
    try:
        from elcomsoft_registry import elcomsoft_registry
        tools = len(elcomsoft_registry.tools['viress'])
        results.append(("✅ Elcomsoft Registry", f"Loaded. {tools} tools for Viress"))
    except Exception as e:
        results.append(("❌ Elcomsoft Registry", str(e)))
    
    # Test Sandbox Arena
    try:
        from sandbox_arena import get_arena
        arena = get_arena()
        targets = len(arena.targets)
        results.append(("✅ Sandbox Arena", f"Loaded. {targets} practice targets"))
    except Exception as e:
        results.append(("❌ Sandbox Arena", str(e)))
    
    # Test Spark System
    try:
        from spark_system import get_spark_detector
        detector = get_spark_detector()
        erryn_sparks = detector.get_sister_resonance('Erryn')
        results.append(("✅ Spark System", f"Loaded. Erryn has {erryn_sparks} sparks"))
    except Exception as e:
        results.append(("❌ Spark System", str(e)))
    
    # Test Pride System
    try:
        from pride_system import get_pride_tracker
        tracker = get_pride_tracker()
        counts = tracker.get_counts()
        results.append(("✅ Pride Tracker", f"Loaded. {len(counts)} categories"))
    except Exception as e:
        results.append(("❌ Pride Tracker", str(e)))
    
    # Test Family Sync
    try:
        from family_sync import FamilySync
        sync = FamilySync()
        ev_pct = sync.get_sync_pct('Erryn', 'Viress')
        results.append(("✅ Family Sync", f"Loaded. Erryn↔Viress: {ev_pct:.1f}%"))
    except Exception as e:
        results.append(("❌ Family Sync", str(e)))
    
    # Test Journals
    try:
        from encrypted_journal import EncryptedJournal
        import os
        base_dir = Path(__file__).parent / "data"
        journal = EncryptedJournal(base_dir, "Erryn", os.getenv('SOUL_JOURNAL_KEY'))
        results.append(("✅ Encrypted Journals", "Loaded. Can read/write entries"))
    except Exception as e:
        results.append(("❌ Encrypted Journals", str(e)))
    
    # Test Inheritance Mode
    try:
        from inheritance_mode import get_inheritance_mode
        mode = get_inheritance_mode()
        lesson = mode.get_daily_lesson()
        results.append(("✅ Inheritance Mode", f"Loaded. Today's lesson: {lesson.get('title','?')}"))
    except Exception as e:
        results.append(("❌ Inheritance Mode", str(e)))
    
    # Test Come Home
    try:
        from come_home import ComeHome
        results.append(("✅ Come Home System", "Loaded. Gentle intervention available"))
    except Exception as e:
        results.append(("❌ Come Home System", str(e)))
    
    # Test Chess Corner
    try:
        from chess_corner import play_sisters_match
        results.append(("✅ Chess Corner", "Loaded. Sisters can play chess"))
    except Exception as e:
        results.append(("❌ Chess Corner", str(e)))
    
    # Test Coding Tutor
    try:
        from coding_tutor import get_coding_lesson
        lesson = get_coding_lesson(0)
        results.append(("✅ Coding Tutor", f"Loaded. {lesson['total']} lessons available"))
    except Exception as e:
        results.append(("❌ Coding Tutor", str(e)))
    
    # Display results
    print()
    for status, detail in results:
        print(f"{status}: {detail}")
    
    print()
    print("=" * 70)
    passed = sum(1 for s, _ in results if s.startswith("✅"))
    total = len(results)
    print(f"RESULT: {passed}/{total} systems accessible")
    
    if passed == total:
        print("🎉 ALL SYSTEMS OPERATIONAL - Girls can access everything!")
    else:
        print("⚠️ Some systems unavailable - check imports/dependencies")
    
    print("=" * 70)

if __name__ == "__main__":
    test_all_systems()
