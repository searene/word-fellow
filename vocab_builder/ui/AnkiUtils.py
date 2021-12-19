from aqt import mw


def get_addon_dir():
    for addon_meta in mw.addonManager.all_addon_meta():
        if addon_meta.human_name() == "vocab_builder":
            return mw.addonManager.addonsFolder(addon_meta.dir_name)
    raise FileNotFoundError("Addon vocab_builder not found")
