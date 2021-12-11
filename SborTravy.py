from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json

username = "login"
password = "password"

def acp_api_send_request(driver, message_type, data={}):
    message = {
        # всегда указывается именно этот получатель API сообщения
        'receiver': 'antiCaptchaPlugin',
        # тип запроса, например setOptions
        'type': message_type,
        # мерджим с дополнительными данными
        **data
    }
    # выполняем JS код на странице
    # а именно отправляем сообщение стандартным методом window.postMessage
    return driver.execute_script("""
    return window.postMessage({});
    """.format(json.dumps(message)))


options = Options()
#options.binary_location = "C:\\Users\\Admin\\AppData\\Local\\Programs\\Opera\\launcher.exe"
options.add_extension('anticaptcha-plugin_v0.60.crx')
driver = webdriver.Chrome(executable_path='/home/andrey/Рабочий стол/python_script/selenium_test/operadriver', options=options)
#driver.set_window_size(140, 900)
driver.get("http://www.wmod.ru")
sleep(3)

acp_api_send_request(
    driver,
    'setOptions',
    {'options': {'antiCaptchaApiKey': 'KEY'}}
)

driver.find_element_by_id("email").send_keys(username)
# найти поле ввода пароля и также вставить пароль
driver.find_element_by_id("password").send_keys(password)
# нажмите кнопку входа в систему
driver.find_element_by_name("submit").click()

a = 0
c = 0
b = 0
step = driver.find_element_by_xpath("//input[@name='move'][@type='submit'][@value='N']")
location = 0
while True:
    c += 1
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    list_1 = soup.text
    list_1 = ' '.join(list_1.split())
    res = list_1.split()
    del res[40:]
    trava = "Аир" in list_1
    aura = "Подкрадывание" in res
    box = "Ящик" in list_1
    attack = "атакованы" in res
    games_map = "игровой" in list_1
    print(res)
    driver.implicitly_wait(2)

    if box == True:
        driver.find_element_by_link_text("пройти мимо").click()
        aura = True

    if aura == False:
        button = driver.find_element_by_xpath("//input[@class='battle'][@type='submit'][@value='колдовать']").click()
        sleep(8)
        
    if attack == True:
        attack_but = driver.find_element_by_xpath("//input[@type='submit'][@name='fight'][@value='атака']").click()
        sleep(8)

    if trava == True:
        driver.implicitly_wait(2)
        b += 1
        driver.find_element_by_link_text("Аир болотный").click()
        page = driver.page_source
        pars = BeautifulSoup(page, 'html.parser')
        captcha = pars.find("div", class_="captcha")
        list_2 = pars.text
        list_2 = ' '.join(list_2.split())
        not_el = "позже!" in list_2
        put_in = "нашли" in list_2

        if not_el == True:
            button_W = driver.find_element_by_xpath("//input[@name='move'][@type='submit'][@value='N']").click()
            a += 1
            location += 1
        if captcha != None:
            # Самая важная чаcть: ждем не более 120 секунд пока индикатор антикаптчи с классом antigate_solver
            # не получит класс solved, что означает что рекапча решена
            WebDriverWait(driver, 120).until(lambda x: x.find_element_by_css_selector('.antigate_solver.solved'))
            button = driver.find_element_by_xpath("//input[@name='submit'][@type='submit'][@value='Желаете положить в рюкзак?']").click()
            put_in = False
        if put_in == True:
            #driver.implicitly_wait(2)
            button = driver.find_element_by_xpath("//input[@name='submit'][@type='submit'][@value='Желаете положить в рюкзак?']").click()
    if games_map == True:
        break
    """
    if (location % 2 == 0 and trava == False):
        while True:
            page = driver.page_source
            soup = BeautifulSoup(page, 'html.parser')
            list_1 = soup.text
            list_1 = ' '.join(list_1.split())
            res = list_1.split()
            del res[25:]
            trava = "Аир" in list_1
            lok = "невозможно" in res
            print(res)
            if trava == True:
                break
            else:
                print("Здесь должна расти трава")
                driver.find_element_by_link_text("инвентарь").click()
                driver.find_element_by_id('item-0').click()
                driver.find_element_by_xpath("//select[@name='action']/option[@value='plant']").click()
                driver.find_element_by_xpath("//input[@type='submit'][@name='submit'][@value='Применить']").click()
                sleep(62)
    """
    #print(location % 2, trava)
    driver.implicitly_wait(2)
    button_W = driver.find_element_by_xpath("//input[@name='move'][@type='submit'][@value='N']").click()
    location += 1
print(b, c, a)
