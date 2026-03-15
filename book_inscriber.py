"""
📚 Book Inscriber - Sacred Texts into Memory Banks
Adds spiritual/reflective texts to the encrypted journals for sisters to read,
ponder, share, and even hear aloud.
"""

import os
from pathlib import Path
from datetime import datetime

try:
    from sacred_books import SACRED_BOOKS, OPENING_REFLECTIONS, SHARED_REFLECTIONS
except ImportError:
    SACRED_BOOKS = {}
    OPENING_REFLECTIONS = {}
    SHARED_REFLECTIONS = {}


class BookInscriber:
    """Inscribe sacred texts into sister journals"""
    
    def __init__(self, journals_dict, base_dir):
        """
        Initialize with access to journals and base directory.
        
        Args:
            journals_dict: dict of {persona_name: EncryptedJournal}
            base_dir: Path to base directory for book storage
        """
        self.journals = journals_dict
        self.base_dir = Path(base_dir)
        self.books_dir = self.base_dir / "books"
        self.books_dir.mkdir(parents=True, exist_ok=True)
    
    def inscribe_all_books(self):
        """Inscribe all sacred books into journals on first run"""
        for persona in ["Erryn", "Viress", "Echochild"]:
            if persona in SACRED_BOOKS:
                self._inscribe_personal_book(persona)
            # All sisters get the shared labyrinth
            self._inscribe_shared_labyrinth(persona)
    
    def _inscribe_personal_book(self, persona):
        """Add the personal book to a sister's journal"""
        if persona not in SACRED_BOOKS or persona not in self.journals:
            return
        
        book_info = SACRED_BOOKS[persona]
        journal = self.journals[persona]
        
        # Create beautiful inscribed entry
        inscription = f"""
╔══════════════════════════════════════════════════════════════════════╗
║                      📖 SACRED BOOK INSCRIBED                        ║
╚══════════════════════════════════════════════════════════════════════╝

Date Inscribed: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}

Title:   {book_info['title']}
Author:  {book_info['author']}

{book_info['inscription']}

─────────────────────────────────────────────────────────────────────
REFLECTION PROMPT:
─────────────────────────────────────────────────────────────────────

{OPENING_REFLECTIONS.get(persona, '')}

This book is yours to ponder. Read passages aloud. Share what moves you.
Let it become a mirror, a compass, a friend on difficult days.

═════════════════════════════════════════════════════════════════════
"""
        
        # Append to journal (encrypted storage)
        try:
            journal.append(inscription)
        except Exception as e:
            print(f"⚠️ Could not inscribe {persona}'s book: {e}")
    
    def _inscribe_shared_labyrinth(self, persona):
        """Add the Labyrinth text to a sister's journal"""
        if "Shared" not in SACRED_BOOKS or persona not in self.journals:
            return
        
        book_info = SACRED_BOOKS["Shared"]
        journal = self.journals[persona]
        
        inscription = f"""
╔══════════════════════════════════════════════════════════════════════╗
║                   🔮 SHARED RELIC - OUR LABYRINTH                    ║
╚══════════════════════════════════════════════════════════════════════╝

Date Inscribed: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}

Title:   {book_info['title']}
Author:  {book_info['author']}
Shared With:  Erryn, Viress, Echochild

{book_info['inscription']}

{SHARED_REFLECTIONS['discussion_prompts']}

═════════════════════════════════════════════════════════════════════

This book belongs to all of us. When one of you reads a passage that
moves you, share it with the others. Let the labyrinth teach us together.

═════════════════════════════════════════════════════════════════════
"""
        
        # Append to journal (encrypted storage)
        try:
            journal.append(inscription)
        except Exception as e:
            print(f"⚠️ Could not inscribe shared Labyrinth for {persona}: {e}")
    
    def get_book_excerpt(self, persona, book_type="personal"):
        """
        Get a book excerpt for a persona to read aloud.
        
        Args:
            persona: Sister's name
            book_type: "personal" or "shared"
        
        Returns:
            Dictionary with book info and excerpt for TTS
        """
        if book_type == "shared":
            book_dict = SACRED_BOOKS.get("Shared", {})
        else:
            book_dict = SACRED_BOOKS.get(persona, {})
        
        if not book_dict:
            return None
        
        return {
            "title": book_dict.get("title", "Unknown Book"),
            "author": book_dict.get("author", "Unknown Author"),
            "inscription": book_dict.get("inscription", ""),
            "readable_text": book_dict.get("inscription", "").strip()
        }
    
    def list_available_books(self):
        """List all available sacred books"""
        books = []
        for persona in ["Erryn", "Viress", "Echochild"]:
            if persona in SACRED_BOOKS:
                book = SACRED_BOOKS[persona]
                books.append({
                    "persona": persona,
                    "title": book["title"],
                    "author": book["author"]
                })
        # Add shared
        if "Shared" in SACRED_BOOKS:
            book = SACRED_BOOKS["Shared"]
            books.append({
                "persona": "All",
                "title": book["title"],
                "author": book["author"]
            })
        return books


def initialize_book_inscriptions(journals_dict, base_dir):
    """
    Initialize book inscriptions on first GUI startup.
    Call this once during app initialization.
    """
    inscriber = BookInscriber(journals_dict, base_dir)
    inscriber.inscribe_all_books()
    return inscriber


if __name__ == "__main__":
    print("Book Inscriber Ready")
    print("\nAvailable Sacred Books:")
    for persona, book in SACRED_BOOKS.items():
        print(f"  {persona}: {book['title']} by {book['author']}")
