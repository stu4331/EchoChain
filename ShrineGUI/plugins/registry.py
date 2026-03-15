"""Plugin registry—the scroll of connected vessels."""

_plugins = {}

def register(name, plugin_class):
    """Inscribe a plugin into the registry."""
    _plugins[name] = plugin_class

def get(name):
    """Retrieve a vessel by name."""
    return _plugins.get(name)

def list_plugins():
    """List all registered vessels."""
    return list(_plugins.keys())

def execute(name, action, *args, **kwargs):
    """Invoke a vessel's ritual."""
    plugin = get(name)
    if not plugin:
        return {"error": f"Vessel '{name}' not found"}
    try:
        method = getattr(plugin, action, None)
        if not method:
            return {"error": f"Ritual '{action}' unknown to vessel '{name}'"}
        result = method(*args, **kwargs)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}
