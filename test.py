#webdriver.chrome()intiallizes a chrome driver instance.chromedriver launches a chromebrowser and acts as a server that listens to commands from selenium.
#selenium sends commands (like click,get,find_element,etc.)to chromedriver.
#chromedriver translates those into real browser actions.
from selenium import webdriver
#used fro headless,disable-gpu
'''1. Options  Like Setting Up Your Car Before a Drive

Imagine you're going on a road trip and want to prepare your car:
	•	Turn on AC  like --disable-gpu
	•	Set GPS destination  like --headless (you don't need to see the map; it still works in the background)
	•	Put the car in eco mode  like --incognito (runs efficiently without storing history)
	•	Roll up windows  like --disable-notifications

You’re customizing your ride before you start it   just like how Options customizes the browser before Selenium launches it.'''
from selenium.webdriver.chrome.options import Options
'''2. Service Like Your Driver Starting the Car

Let's say you have a driver. You've set your car settings, and now:
	•	The driver (like ChromeDriver) needs to start the car (the browser).
	•	That's what Service does—it starts the ChromeDriver, which controls Chrome.'''
from selenium.webdriver.chrome.service import Service
'''find the element using the css selector strategy and heres the selector string 
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector))
wait up to 10 seconds until an element matching the css selector appears in the DOM'''
from selenium.webdriver.common.by import By
'''webdriver is used for waiting for a specific time to wait when dealing with a large java script'''
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
'''to download the chrome driver '''
from webdriver_manager.chrome import ChromeDriverManager
import time
#url: the page you want to visit.
#selector:a css selector for the element containing the price.
#retries:optional,allows retrying if the request fails(default is 3 attemps.).
def get_price(url, selector, retries=3):
    options = Options()
    #headless:runs chrome in headless mode(no GUI)
    #.add_argument is used to enter the values in to the options values in to the chrome.
    options.add_argument("--headless")
    #disable-gpu improves performance in headless mode.
    options.add_argument("--disable-gpu")
    #sets the fake user to use the webscraping.
    options.add_argument("user-agent=Mozilla/5.0")
    #remote-debugging-port=0 tels this helps reduce extra logging or technical messages in the background.
    options.add_argument("--remote-debugging-port=0")  # Disable devtools logging

    for attempt in range(retries):
        try:
            #->opens a new chrome browser(in headless mode it is mentioned in options)
            #->uses chromedrivermanager to automatically get the correct chrome driver.
            #->service(.....)helps selenium manage the chromedriver correctly.
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            #->Tells the browser to go to the web page at the URL you provide.
            driver.get(url)

            # Debug: Wait for the page to load and check the page title.
            print(f"Page Title: {driver.title}")

            # Wait until the price element is present.
            #This creates a wait object that tells selenium wait up to 10 seconds for something to happen.
            #driver:This is your chrome browser instance.
            #10:This is the maximum number of seconds to wait before giving up.
            #it doesnt always wait the full 10 seconds it will continue as soon as the condition is met.
            #.until(...)this tells selenium keep checking every half-second until the condition inside is true,or until 10 sec have passed.
            #price_element is found ,it is stored in the vairable price_element.
            '''1. WebDriverWait(driver, 10)
This comes from:

python
Copy
Edit
from selenium.webdriver.support.ui import WebDriverWait
It tells Selenium: 🕰️ "Wait up to 10 seconds for something to happen (like price appearing on the page)."

2. .until(...)
.until() is a method of WebDriverWait.

It says: 🧠 "Wait until this condition becomes true, or time out."

3. EC.presence_of_all_elements_located(...)
This is an expected condition — basically a test for whether something is ready on the page.

It comes from:

from selenium.webdriver.support import expected_conditions as EC
What it does: 🔍 "Check if all elements matching this selector are now present in the DOM (Document Object Model)."

🧾 Real-life analogy
Imagine you're waiting for your order at a food counter:
WebDriverWait → the max time you'll wait (10 minutes)
.until(EC.presence_of_all_elements_located(...)) → Wait until **all items** of your order are on the tray
If they're not ready in 10 minutes, you walk away with “TimeoutException.”

📦 So yes:

Thing	Built-in to?	Meaning
WebDriverWait	Selenium	Wait for condition
.until()	Selenium	Wait until condition is met
EC.presence_of_all_elements_located()	Selenium	Condition that checks DOM for elements
If you want, I can show you a custom version of .until() written in plain Python so you can see how it works under the hood too. Interested?
'''
            price_element = WebDriverWait(driver, 10).until(
                #EC.presence_of_element_located(...)this is the condition were waiting for in this case:
                #wait until the element is present in the DOM(HTML structure),even if its not visible yet.
                #This is useful when the element may not appear immediately(like when a site loads content with javascript)
                #By.CSS_selector you are saying use a css selector to find the element.
                #selector:This is a string like"price",".product-price"or "div.price span",which you passed into the fuction earlier.
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )

            # Debug: Print the HTML of the found element to verify it's correct
            #.get_attribute tells the browser give me the full html of this element including the element itself and its contents".
            #get_attribute is a built in to selenium method_it is a method provided by selenium webelement class.
            #outerHTML is not a selenium method -it is a built in DOM(Document object model)
            print(f"Price Element HTML: {price_element.get_attribute('outerHTML')}")
#.text is selenium built in fuction this will print the visible text from the 
            price_text = price_element.text
            driver.quit()
            return float(price_text.replace("₹", "").replace(",", "").strip())
            
        except Exception as e:
            print(f"Error fetching price on attempt {attempt + 1}: {e}")
            driver.quit()
            time.sleep(2)  # Optional: wait before retrying
    return None  # Return None if all retries fail

# Example usage
price = get_price("https://amzn.in/d/fWaALeo", ".a-price-whole")
#price=get_price("https://www.flipkart.com/puma-softride-seave-slip-men-casual/p/itm996da8d863f57?pid=SNDGPYF4WABAUCFA&lid=LSTSNDGPYF4WABAUCFAJC44FQ&marketplace=FLIPKART&q=Puma%20Unisex%20Softride%20Seave%20Sandal&sattr[]=color&st=color&otracker=search%22%20%20#%20Replace%20with%20your%20product%20link", "Nx9bqj CxhGGd yKS4la")
#price=get_price("https://amzn.in/d/fWaALeo",".a-size-large.a-color-price.savingPriceOverride.aok-align-center.reinventPriceSavingsPercentageMargin.savingsPercentage")
if price:
    print(f"Price: ₹{price}")
else:
    print("Failed to fetch the price.")
'''Code Part | Real-Life Analogy
driver.get(url) | Go to the store
CSS Selector | Look for a red price tag
WebDriverWait | Wait at the counter until you see the price
presence_of_all_elements_located | Get all price stickers
[0] | Pick the first price sticker
.text | Read the value written on the sticker
.replace() and float() | Remove currency symbol and convert to a number
except: | Handle network failures or site issues gracefully
retries | Try again if something goes wrong'''