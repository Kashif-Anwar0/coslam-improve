import yaml


def load_config(path, default_path=None):
    """Load configuration from ``path`` and optionally inherit from ``default_path``."""
    with open(path, 'r') as f:
        cfg_special = yaml.full_load(f)

    inherit_from = cfg_special.get('inherit_from')
    if inherit_from is not None:
        cfg = load_config(inherit_from, default_path)
    elif default_path is not None:
        with open(default_path, 'r') as f:
            cfg = yaml.full_load(f)
    else:
        cfg = {}

    update_recursive(cfg, cfg_special)
    return cfg


def update_recursive(dict1, dict2):
    """Recursively update ``dict1`` using values from ``dict2``."""
    for k, v in dict2.items():
        if k not in dict1:
            dict1[k] = {} if isinstance(v, dict) else v
            if isinstance(v, dict):
                update_recursive(dict1[k], v)
        else:
            if isinstance(v, dict) and isinstance(dict1[k], dict):
                update_recursive(dict1[k], v)
            else:
                dict1[k] = v

__all__ = ["load_config", "update_recursive"]

