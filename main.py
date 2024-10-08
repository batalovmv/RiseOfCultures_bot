from chrome_utils import open_chrome_with_profile
from navigation import navigate_and_handle
import json

# Загружает конфигурацию из файла.
def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        print("Файл конфигурации не найден.")
        return None

# Выводит доступные профили
def display_profiles(profiles):
    for index, profile in enumerate(profiles):
        print(f"{index}: {profile['name']}")

# Запрашивает выбор профиля у пользователя.
def get_user_choice(num_profiles):
    choice = input("Выберите номер профиля: ")
    try:
        choice = int(choice)
        if 0 <= choice < num_profiles:
            return choice
        else:
            print("Некорректный выбор профиля.")
            return None
    except ValueError:
        print("Пожалуйста, введите число.")
        return None

# Основная функция
def main():
    config = load_config()
    
    if config is None or 'profiles' not in config or 'user_data_dir' not in config:
        print("Нет доступных профилей или не указан user_data_dir.")
        return

    profiles = config['profiles']
    user_data_dir = config['user_data_dir']
    display_profiles(profiles)

    choice = get_user_choice(len(profiles))
    if choice is not None:
        selected_profile = profiles[choice]
        profile_directory = selected_profile['directory']

        driver = open_chrome_with_profile(user_data_dir, profile_directory)

        try:
            navigate_and_handle(driver)
        finally:
            driver.quit()  # Закрываем браузер

if __name__ == "__main__":
    main()