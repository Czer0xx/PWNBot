from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options
import pyfiglet
import random
import re
import requests
import json

PATH = "chromedriver.exe"

pwn_text = pyfiglet.figlet_format("PWN\nBOTTER", font = "slant")

def main():
    global visible
    global description_list
    global delay
    global end_delay
    global email
    global word
    time.sleep(2)
    print(pwn_text)
    while True:
        word = input("Word: ")
        if word == "":
            print("\nCannot be empty!\n")
            continue
        description_input = input("Descriptions (separated by comma ','): ")
        if description_input == "":
            print("\nCannot be empty!\n")
            continue
        description_list = description_input.split(",")
        try:
            delay = int(input("Delay (def. 3): "))
        except ValueError:
            delay = 3
        visible = input("Visible? Y/N: ")
        visible = visible.lower()
        if visible == "":
            visible = "n"
        break

def generate():
    global login
    global domain
    global email
    r = requests.post("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
    email = r.text
    email = email.replace('["',"")
    email = email.replace('"]',"")
    splitted_email = email.split("@")
    domain = splitted_email[1]
    login = splitted_email[0]

def verify():
    url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
    while True:
        r = requests.get(url)
        parsed = json.loads(r.text)
        try:
            if 'id' in parsed[0]:
                for url in parsed:
                    id = url["id"]
                url2 = f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={id}"
                response = requests.get(url2)
                response.raise_for_status()
                jsonResponse = response.json()
                for key, value in jsonResponse.items():
                    c = re.findall("<a href=\".*?(?=\")", jsonResponse["body"])
                    c = "".join(c)
                    link = c.replace('<a href="', "")
                    options = Options()
                    if visible == "n":
                        options.add_argument('--headless')
                        options.add_argument('--disable-gpu')
                    options.add_argument("--log-level=3")
                    options.add_experimental_option('excludeSwitches', ['enable-logging'])
                    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
                    driver.get(link)
                    time.sleep(2)
                    print("Email sucessfully verified!")
                    driver.quit()
                    break
                break
                
        except:
            pass

def bot():
    global sequence
    sent = 0
    generate()
    print(f"\nGenerated email: {email}")
    description = random.choice(description_list)
    options = Options()
    if visible == "n":
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
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
        verify()
    else:
        print("\nSequence Failed! :(\n")
    driver.quit()
    bot()

if __name__ == "__main__":
    sent = 0
    sequence = 0
    main()
    bot()
