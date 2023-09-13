# Русское GUI для silero TTS
Русскоязычный интерфейс для edge tts 
Код взят у https://github.com/GhostNaN/silero-webui и локализован мной.

Есть 2 типа интерфейса. Скрины ниже.
1. С видео. В конце выходит видео-водопад звука.
![Скрин интерфейса с видео(делает видео водопад звука)](https://github.com/hinaichigo-fox/rus-silero-webui/blob/main/vid.jpg)
2. Аудио. В конце только аудио формата .wav
![Скрин интерфейса с аудио(тут только аудио формата .wav)](https://github.com/hinaichigo-fox/rus-silero-webui/blob/main/aud.jpg)

# Установка
```
Скачайте ffmpeg (гайдов в тырнете полно)
Добавьте его в пач (path)
git clone https://github.com/hinaichigo-fox/rus-silero-webui.git
cd rus-silero-webui
#тут выбор будет. либо делаете python -m venv venv а потом venv\Scripts\activate либо пропускаете это, но потом возможно будет ошибка(ниже покажу как пофиксить
pip install -r requirements.txt
python app_aud.py (если хотите получать в конце аудио)
python app_vid.py (если хотите получать видео-водопад аудио файла в конце)
```
# Ошибки
если вы пропустили этап создания виртуального окружения( python -m venv venv) то у вас будет ошибка
```
 File "C:\Users\Admin/.cache\torch\hub\snakers4_silero-models_master\hubconf.py", line 4, in <module>
 from src.silero import (
ModuleNotFoundError: No module named 'src.silero'
```
или
```
    from silero import (
ModuleNotFoundError: No module named 'silero'
```
# Фикс данной ошибки
1. Перейдите к папке `.cache\torch\hub\snakers4_silero-models_master` (полный путь см. в выводе об ошибке)
2. Скопируйте папку silero из каталога src и разместите их в папке проекта
3. Откройте и отредактируйте файл hubconf.py(этот файл был в папке в пункте 1 НЕ В ПАПКЕ SILERO) следующим образом:
```
import os
import sys

from silero import (
    silero_stt,
    silero_tts,
    silero_te,
)

__all__ = [
    "silero_stt",
    "silero_tts",
    "silero_te",
]

sys.path.append(os.path.dirname(__file__))
```
Ошибка должна исчезнуть!

# Голоса 
Доступные голоса для tts v4_ru:
1. aidar
2. baya
3. kseniya
4. xenia
5. eugene
