# DNA Guardian Web API - Requirements

## Python Dependencies

Add these to your `requirements.txt`:

```
Flask>=2.0.0
```

Or install manually:

```bash
pip install Flask
```

## For ShrineGUI Integration

The ShrineGUI application already has Flask installed, so no additional dependencies are needed.

Just add the import to your `app.py`:

```python
from dna_guardian_api import register_dna_guardian_api

register_dna_guardian_api(app)
```

## Testing Without Flask

If Flask is not available, the DNA Guardian can still be used via:
- Command-line: `python dna_guardian_cli.py`
- Python API: `from dna_guardian_protection import guardian`

The web API is an optional enhancement for website integration.
