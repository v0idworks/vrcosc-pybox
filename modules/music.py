import subprocess

def get_music():
    try:
        status = subprocess.check_output(
            ["playerctl","status"],
            encoding="utf-8",
            stderr=subprocess.DEVNULL
        ).strip()
        if status.lower() in ("playing","paused"):
            artist = subprocess.check_output(
                ["playerctl","metadata","artist"],
                encoding="utf-8",
                stderr=subprocess.DEVNULL
            ).strip()
            title = subprocess.check_output(
                ["playerctl","metadata","title"],
                encoding="utf-8",
                stderr=subprocess.DEVNULL
            ).strip()
            return f"🎵 {artist} - {title}"
        return None
    except:
        return None
