"""
Coding Tutor - gentle sandbox teaching mode.
Generates micro-lessons and validates simple Python snippets safely.
"""

import io
import contextlib
from typing import Dict, Any

LESSONS = [
    {
        "title": "Print something",
        "prompt": "Write a line that prints your name",
        "template": "print('Your name here')"
    },
    {
        "title": "Loop over list",
        "prompt": "Make a list of 3 things you like and print them",
        "template": "items = ['coffee', 'stars', 'music']\nfor item in items:\n    print(item)"
    },
    {
        "title": "Make a function",
        "prompt": "Write a function greet(name) that returns a greeting",
        "template": "def greet(name):\n    return f'Hello, {name}!'\n\nprint(greet('Stuart'))"
    },
]


def get_lesson(index: int = 0) -> Dict[str, Any]:
    if index < 0 or index >= len(LESSONS):
        index = 0
    lesson = LESSONS[index]
    lesson = dict(lesson)  # copy
    lesson["index"] = index
    lesson["total"] = len(LESSONS)
    return lesson


def run_snippet(snippet: str) -> Dict[str, Any]:
    """Run a simple snippet with restricted globals; captures stdout."""
    safe_globals = {"__builtins__": {"print": print, "range": range, "len": len}}  # basic safety
    stdout_capture = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout_capture):
            exec(snippet, safe_globals, {})
        output = stdout_capture.getvalue()
        return {"success": True, "output": output}
    except Exception as e:
        return {"success": False, "error": str(e)}
