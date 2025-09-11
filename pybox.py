import time, psutil, requests, subprocess, random, shutil
from pythonosc.udp_client import SimpleUDPClient
from datetime import datetime

ip = "127.0.0.1"
ip2 = "192.168.1.1"
port = 9000
client = SimpleUDPClient(ip, port)
client2 = SimpleUDPClient(ip2, port)
# - Настройки -
ENABLE_COMMIT = True
ENABLE_RANDOM = True
ENABLE_WEATHER = True
ENABLE_HARDWARE = True
ENABLE_WINDOW = True
ENABLE_MUSIC = True
ENABLE_2CLIENT = True #Для Bторого клиента
def get_git():
    try:
        return subprocess.check_output(["git", "rev-parse", "--short=7", "HEAD"]).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        return "Гит шарманит, рестартай прогу."
git_commit = "⚙️pybox " + get_git()
city = "Москоу"

# - Погода -
#если модуль погодbi не пишет иконку то тогда делайте тоже что и снизу только "инглиш нейм": "иконка"
weather_icons = {
    "солнечно": "☀️",
    "чистое небо": "🌙",
    "малооблачно": "⛅",
    "облачно": "☁️",
    "местами дождь": "🌥",
    "туман": "🌫",
    "местами возможен дождь": "🌦",
    "небольшой дождь": "🌧",
    "сильный дождь": "🌧",
    "снег": "❄️",
    "гроза": "🌩",
    "дождь с грозой": "⛈️",
    "sunny":"☀️",
    "clear":"🌙",
    "partly cloudy":"⛅",
    "cloudy":"☁️",
    "overcast":"🌥",
    "mist":"🌫",
    "patchy rain possible":"🌦",
    "light rain":"🌧",
    "heavy rain":"🌧",
    "snow":"❄️",
    "thunder":"🌩",
    "Rain with thunderstorm": "⛈️",
}
'''
Устарело. Bместо этого теперь ?lang=ru
weather_translate = {
    "sunny":"Солнечно","clear":"Ясно","partly cloudy":"Перем. облачность",
    "cloudy":"Облачно","overcast":"Пасмурно","mist":"Туман",
    "patchy rain possible":"Возможен дождь","light rain":"Небольшой дождь",
    "heavy rain":"Сильный дождь","snow":"Снег","thunder":"Гроза",
    "Rain with thunderstorm":"Дождь с грозой",
}
'''


#чтоб самому текст напечатать сюда делаем так:стаBим запятую перед прошлbiм текстом если не стоит и пишем "текст"
custom_messages = ["Добро пожалоBать B pybox-vrc","Это рандомbiй текст","tinyurl.com/pyboxvrc"]
if shutil.which("playerctl") is None:
    print("[❌] playerctl не найден (информация о музыке будет отключена)")
    ENABLE_MUSIC = False
if shutil.which("kdotool") is None:
    print("[❌] kdotool не найден (информация об активном окне будет отключена)")
    ENABLE_WINDOW = False




# - Модуляки разнbiе
#только для зеленbiх
def get_gpu():
    try:
        out = subprocess.check_output(
            ["nvidia-smi","--query-gpu=utilization.gpu,memory.used,memory.total","--format=csv,noheader,nounits"],
            encoding="utf-8"
        )
        u, used, total = out.strip().split(", ")
        return int(u), int(used), int(total)
    except:
        return None, None, None


def get_weather():
    try:
        data = requests.get(f"https://wttr.in/{city}?format=j1&lang=ru", timeout=5).json()
        t = data["current_condition"][0]["temp_C"]
        f = data["current_condition"][0]["FeelsLikeC"]
        desc = data["current_condition"][0]["lang_ru"][0]["value"].lower()
        #desc = data["current_condition"][0]["weatherDesc"][0]["value"].lower()
        #if you wаnt english replаce lаng=ru w/ lаng=en аnd uncomment this line
        icon = next((e for k,e in weather_icons.items() if k.lower() in desc), "❓")
        return f"{icon} {desc.capitalize()} {t}°C (ощущ. {f}°C)"

    except:
        return "🌐 Упс! wttr.in не ответил вовремя."
# - очень privacy invasive модуль, не рекомендую открbiBать браузер и/или открbiBать чтото что нежелательно для показа на публику
def get_window():

    try:
        win_id = subprocess.check_output(
            ["kdotool", "getactivewindow"], encoding="utf-8"
        ).strip()
        title = subprocess.check_output(
            ["kdotool", "getwindowname", win_id], encoding="utf-8"
        ).strip()
        return f"💻 {title}" if title else "💻Рабочий стол"
    except:
        return "Рабочий стол"


# - очень privacy invasive модуль, не рекомендую смотреть/cлушать нежелательнbiй для показа на публику контент пока это Bключено
def get_music():
    try:
        status = subprocess.check_output(["playerctl", "status"],encoding="utf-8",stderr=subprocess.DEVNULL).strip()
        if status.lower() in ("playing", "paused"):
            artist = subprocess.check_output(["playerctl", "metadata", "artist"],encoding="utf-8",stderr=subprocess.DEVNULL).strip()
            title = subprocess.check_output(["playerctl", "metadata", "title"],encoding="utf-8",stderr=subprocess.DEVNULL).strip()
            return f"🎵 {artist} - {title}"
        else:
            return None
    except subprocess.CalledProcessError:
        return None


weather_info = get_weather()
last_weather_update = time.time()
cpu = psutil.cpu_percent()
ram = psutil.virtual_memory().percent
temp = psutil.sensors_temperatures()
gpu_util, vram_used, vram_total = get_gpu()
cpu_temp = temp["coretemp"][0].current if "coretemp" in temp else "?"
while True:
    if time.time() - last_weather_update > 120:
        weather_info = get_weather()
        last_weather_update = time.time()
    parts = []
    #ломает winDowz саппорт, а кому он нужен? идите жрите магикчатбокс
    if ENABLE_HARDWARE:
        hw_msg = f"CPU {cpu}% 🌡{cpu_temp}°C RAM {ram}%"
        if gpu_util is not None:
            hw_msg += f"🎮GPU {gpu_util}% VRAM {vram_used}/{vram_total}MB"
        parts.append(hw_msg)
    if ENABLE_WEATHER: parts.append(weather_info)
    if ENABLE_RANDOM: parts.append(f"💬 {random.choice(custom_messages)}")
    if ENABLE_COMMIT: parts.append(git_commit)
    if ENABLE_WINDOW: parts.append(get_window())
    if ENABLE_MUSIC:
        m = get_music()
        if m: parts.append(m)
    parts.append(f"🕒 {datetime.now().strftime('%H:%M')}")

    # - крутой fix для лимита текста -
    drop_order = ["COMMIT", "TIME", "WINDOW", "MUSIC", "WEATHER", "HARDWARE"]
    while drop_order:
        total_len = sum(len(p) for p in parts) + len(parts) - 1
        if total_len <= 144:
            break
        drop = drop_order.pop(0)
        if drop == "COMMIT" and ENABLE_COMMIT:
            parts = [p for p in parts if p != git_commit]
        elif drop == "TIME":
            parts = [p for p in parts if not p.startswith("🕒")]
        elif drop == "WINDOW":
            parts = [p for p in parts if not p.startswith("🪟")]
        elif drop == "MUSIC":
            parts = [p for p in parts if not (p and p.startswith("🎵"))]
        elif drop == "WEATHER" and ENABLE_WEATHER:
            parts = [p for p in parts if p != weather_info]
        elif drop == "HARDWARE" and ENABLE_HARDWARE:
            parts = [p for p in parts if not ("CPU" in p or "GPU" in p)]
    final_msg = "\n".join(parts)
    client.send_message("/chatbox/input", [final_msg, True])
    if ENABLE_2CLIENT:
      client2.send_message("/chatbox/input", [final_msg, True])
    time.sleep(10)
