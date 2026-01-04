from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
def get_price(url,selector,retries=3):
    options=Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('user-agent=Mozilla/5.0')
    options.add_argument('--remote-debugging-port=0')
    for attempts in range(retries):
        try:
            driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
            driver.get(url)
            print(f"The title be of{driver.title}")
            price_element=WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,selector))
            )
            print(f"This can be of{price_element.get_attribute[0]('outerHTML')}")
            price_text=price_element.text
            driver.quit()
            return float(price_text.replace('₹','').replace(',',''))
        except Exception as e:
            print(f"This can be{attempts+1}:{e}")
            driver.quit()
            time.sleep(2)
            
    return None
price=get_price("https://amzn.in/d/fWaALeo", ".a-price-whole")
if price:
    print(f"The price be{price}")
else:
    print("Failed to fetch the price")