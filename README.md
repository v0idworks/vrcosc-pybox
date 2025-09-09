# vrcosc-pybox

Скрипт для автоматического набора текста в чатбокс VRChat.
Сделан под Linux, потому что MagicChatBox отстой и на linux'е не работает

---

## Что умеет
- писать в чат железо (CPU, RAM, температура, GPU если есть nvidia-smi(и не Bсегда работает :( ))
- показывать погоду через wttr.in(спасибо Bам народ обожаю Bас )
- выводить музыку из playerctl (Spotify, VLC и т.п.)
- показывать активное окно через kdotool
- кидать рандомные фразы
- время
- сам подрезает текст под лимит VRChat
- и много чего еще чего я не залил на гитхаб
- Bозможно работает на термуксе
- а также на айосоBском аналоге (не уBерен, не юзал, и VRChat под айос еще не Bbiшел)

---
## Что НЕ умеет
- Работать на win
- работать на макос
- работать на гноме,i3,сBей,cinnаmon,баджи,unity,и на том что не кде.

---
## как Bbiглядит
<img width="331" height="735" alt="изображение" src="https://github.com/user-attachments/assets/da872c9d-061b-4c03-880d-d6b92d0da588"/>

## Что нужно
- Python 3
- пакеты: `psutil`, `requests`, `python-osc`
- утилиты: `git`, `kdotool` (для окон), `playerctl` (для музыки)

Установка питон-зависимостей:
```bash
pip install psutil requests python-osc
```
Установка опциональных зависимостей:
Arch Linux: 
```bash
    sudo pacman -S git kdotool playerctl
```
Debian / Ubuntu(не тестил)
```bash
    sudo apt update
    sudo apt install git kdotool playerctl
```

Fedora(не тестил)
```bash
    sudo dnf install git kdotool playerctl
```
openSUSE(не тестил)
```bash
    sudo zypper install git kdotool playerctl
```
Alpine Linux(не тестил)
```bash
    sudo apk add git kdotool playerctl
```

---
## как юзать?
```bash
    python pybox.py
```
или 
```bash
    python3 pybox.py
```
### поддержать меня
[криптобот](https://t.me/send?start=IVzATgwSpMLM)
monero: 86bvVgxwMxYJghTFF6TCTyXntDVbftb4Jf9PJxGg64WDjjZZPoHopPZEbAPeKdbEEGP2iKZfWx7EAWaBNPwpBm6EHGZUpJS
[DA](https://www.donationalerts.com/c/random_tnt)
#### кредитbi
- сделано с <3 командой v0idworks(а именно рандомом_тнт)
- спасибо линусу дройдBардсу за git и линукс 
- спасибо кдешникам за плазму
- и арчойдам за арчлинукс
- а также Graham Gaylor и Jesse Joudrey за VRChat
- и гейбу ньюэллу за vаlve и стим и его команде за протон и за то что он сBоими руками держит коммунити игр на линуксе
- и Bсем-Bсем моим друзьям B VRChat'е за то что помогли добраться до юзера(да-да, именно Bbi, которbiе B друзьях у бургера/мегашаттербомба)
- и нкосимоко, и дебоширу, записке (SL 14), киберхлебу
- микамерике и аператару за поддержку
- и слипе из смптриггера за дружбу
- и моим мозгам за идеи
- и команде Unity за дBижок
- и гному(редхатойдам) за боль и страдания изза прекращения поддержки x11(/сарказм)
- Гитхабу за гитхаб(хотя я на гитлабе сижу уже)
- [pandao](https://pandao.github.io/editor.md/en) за чудесний мд эдитор
- Джесси Даффилду и Стефану Холлеру за [Lazygit](https://github.com/jesseduffield/lazygit)
- Эдриану Фриду и Мэтту Райту за Open Sound Control (иначе этого проекта бbi небbiло)
---
###### *see you next time....*
