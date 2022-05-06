import aqt


def get_addon_dir():
    for addon_meta in aqt.mw.addonManager.all_addon_meta():
        if addon_meta.human_name() == "word-fellow":
            return aqt.mw.addonManager.addonsFolder(addon_meta.dir_name)
    raise FileNotFoundError("Addon word-fellow not found")
