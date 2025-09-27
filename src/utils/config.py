from aqt import mw


def get_config():
    cfg = mw.addonManager.getConfig(__name__) or {}
    # ensure structure
    if "decks" not in cfg:
        cfg["decks"] = {}
    if "tokens_used" not in cfg:
        cfg["tokens_used"] = 0
    return cfg


# def write_config(cfg):
#     try:
#         mw.addonManager.writeConfig(__name__, cfg)
#     except Exception:
#         # fallback: keep in memory; avoid crashing if API differs
#         mw.col.set_config("paradox_config", str(cfg))
