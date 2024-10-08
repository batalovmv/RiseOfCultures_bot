import time
from selenium.webdriver.common.by import By
#Переходит на сайт и обрабатывает редиректы.
def navigate_and_handle(driver):
    driver.get('https://eu0.riseofcultures.com/')
    time.sleep(5)  # Ждем загрузку страницы

    if "eu0.riseofcultures.com" in driver.current_url:
        print("На нужном сайте.")
        time.sleep(20)  # Ждем 20 секунд
    else:
        print("Перекинуто на другой сайт.")
        try:
            button = driver.find_element(By.ID, 'pop-up_remember-me_n/a_button_login')
            button.click()
            print("Кликнули по кнопке.")
            time.sleep(20)  # Ждем 20 секунд
        except Exception as e:
            print("Кнопка не найдена или ошибка:", e)