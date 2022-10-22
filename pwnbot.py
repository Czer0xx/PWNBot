import email
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options
import pyfiglet
import random

PATH = "chromedriver.exe"

pwn_text = pyfiglet.figlet_format("PWN\nBOTTER", font = "slant")

def main():
    global description_list
    global delay
    global end_delay
    global email
    global word
    time.sleep(2)
    print(pwn_text)
    word = input("Word: ")
    if word == "":
        word = "Malina"
    else:
        word = word
    description_input = input("Descriptions (separated by comma ','): ")
    if description_input == "":
        description_list = ["Malina - określenie na znajomego", "Określenie na przyjaciela", "Malina - przyjaciel, kolega, znajomy", "Malina - kolega", "Malina - znajomy", "Malina to określenie na znajomego lub przyjaciela", "Malina to określenie na kolege"]
    else:
        description_list = description_input.split(",")
    email = input("E-mail: ")
    if email == "":
        email = "jinnybkol@gmail.com"
    try:
        delay = int(input("Delay (def. 0): "))
    except ValueError:
        delay = 0
    try:
        end_delay = int(input("Request End Delay (def. 5): "))
    except ValueError:
        end_delay = 5

def bot():
    global sequence
    sent = 0
    description = random.choice(description_list)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    driver.minimize_window()
    driver.get("https://sjp.pwn.pl/mlodziezowe-slowo-roku/mlodziezowe-slowo-roku;202298.html")
    try:
        driver.find_element(By.XPATH, '//*[@id="floater-send"]').click()
        print("\nShowed policy")
    except: 
        pass
    time.sleep(delay)
    try:
        driver.find_element(By.XPATH, '//*[@id="consent-modal-yr73k"]/div/div/div[3]/button').click()
        print("Accepted policy")
    except: 
        pass
    try:
        driver.find_element(By.XPATH, '//*[@id="floater-word"]').send_keys(word)
        print(f"Entered word: {word}")
    except: 
        pass
    try:
        driver.find_element(By.XPATH, '//*[@id="floater-definition"]').send_keys(description)
        print(f"Entered description: {description}")
    except: 
        pass
    try:
        driver.find_element(By.XPATH, '//*[@id="floater-email"]').send_keys(email)
        print(f"Entered email: {email}")
    except: 
        pass
    try:
        x = driver.find_element(By.XPATH, '//*[@id="age-range"]')
        drop = Select(x)
        drop.select_by_value("13 - 17")
        print("Selected age: '13 - 17'")
    except: 
        pass
    try:
        driver.find_element(By.XPATH, '//*[@id="floater"]/div[3]/div[1]/div/div/div[6]/label/span[1]').click()
        print("Accepted Eula")
    except: 
        pass
    try:
        driver.find_element(By.XPATH, '//*[@id="floater-send"]').click()
        print(f"\nWord: {word}\nDesc: {description}\nE-mail: {email}\n\nSent!")
        sent = 1
    except: 
        pass
    if sent == 1:
        sequence = sequence + 1
        print(f"\nSequence {sequence} done!\n")
    else:
        print("\nSequence Failed! :(\n")
    time.sleep(end_delay)
    driver.quit()
    bot()

if __name__ == "__main__":
    sent = 0
    sequence = 0
    main()
    bot()

# slowo //*[@id="floater-word"]
# opis //*[@id="floater-definition"]
# email //*[@id="floater-email"]
# wiek //*[@id="age-range"]
# eula //*[@id="floater"]/div[3]/div[1]/div/div/div[6]/label/span[1]
# send //*[@id="floater-send"]