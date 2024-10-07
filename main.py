import cv2
import numpy as np
import pyautogui
import time

# Задержка перед началом выполнения (например, чтобы успеть переключиться на нужное окно)
time.sleep(3)

# Перечислите файлы шаблонов, которые вы хотите найти
template_files = ['templates/Food.png', 'templates/Gold.png']

# Установите пороговое значение
threshold = 0.8

# Укажите регион для скриншота (опционально)
# Формат: (левый верхний угол x, y, ширина, высота)
# Если оставить None, будет делаться скриншот всего экрана
region = None  # Например, region = (0, 0, 1920, 1080)

# Основной цикл программы
while True:
    # Сделайте скриншот экрана (или указанного региона)
    screenshot = pyautogui.screenshot(region=region)
    screenshot_rgb = np.array(screenshot)  # PyAutoGUI возвращает изображение в RGB формате

    # Конвертируем в BGR для OpenCV
    screenshot_bgr = cv2.cvtColor(screenshot_rgb, cv2.COLOR_RGB2BGR)

    # Флаг, чтобы определить, найден ли хотя бы один шаблон
    found_any = False

    # Цикл по всем шаблонным изображениям
    for template_path in template_files:
        # Загрузите шаблонное изображение в цвете
        template = cv2.imread(template_path)
        if template is None:
            print(f"Не удалось загрузить шаблонное изображение {template_path}. Проверьте путь к файлу.")
            continue
        w, h = template.shape[1], template.shape[0]

        # Поиск шаблона на снимке экрана
        res = cv2.matchTemplate(screenshot_bgr, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        # Если совпадение найдено, выполните клик и выйдите из вложенного цикла
        if len(loc[0]) > 0:
            # Берём первую найденную точку
            pt = (loc[1][0], loc[0][0])

            # Вычислите координаты центра
            center_x = pt[0] + w / 2
            center_y = pt[1] + h / 2

            # Если используете регион, то добавьте смещение
            if region is not None:
                center_x += region[0]
                center_y += region[1]

            # Выполните нужное действие (например, клик)
            pyautogui.click(center_x, center_y)
            print(f"Клик по координатам: ({center_x}, {center_y}) при обнаружении шаблона {template_path}")

            # (Опционально) Добавьте задержку между действиями или дополнительные действия
            time.sleep(0.5)

            found_any = True
            # Если нужно выполнить клик только по первому найденному шаблону
            break
        else:
            print(f"Шаблон {template_path} не найден на экране.")

    # Если шаблон найден, и вы хотите выйти из основного цикла
    if found_any:
        break

    # (Опционально) Задержка перед следующей проверкой
    time.sleep(1)