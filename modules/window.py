import subprocess

def get_window():
    try:
        win_id = subprocess.check_output(["kdotool","getactivewindow"], encoding="utf-8").strip()
        title = subprocess.check_output(["kdotool","getwindowname",win_id], encoding="utf-8").strip()
        return f"💻 {title}" if title else "💻 Рабочий стол"
    except:
        return None
