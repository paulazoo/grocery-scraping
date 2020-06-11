#%%
from webbot import Browser
import pandas as pd
import selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from datetime import date
import time

from kroger_links import links

wait_time = 1

#%%
def get_text_excluding_children(driver, element):
    return driver.execute_script("""
    var parent = arguments[0];
    var child = parent.firstChild;
    var ret = "";
    while(child) {
        if (child.nodeType === Node.TEXT_NODE)
            ret += child.textContent;
        child = child.nextSibling;
    }
    return ret;
    """, element)

#%%
web = Browser()
web.driver.get('https://www.kroger.com/')
time.sleep(wait_time*2)
web.driver.find_element_by_xpath("//button[@class='kds-Button kds-Button--primary DynamicTooltip--Button--Confirm float-right']").click()


#%%
food_dict = {}
i = 1
total = float(0)
for link in links:
    web.driver.get(link)
    time.sleep(wait_time*2)
    price_element = web.driver.find_elements_by_xpath("//data[@class='kds-Price']")[0]
    time.sleep(1)
    price_text = price_element.get_attribute("value")
    price = float(price_text)
    print(price)
    
    name_element = web.driver.find_elements_by_css_selector("span[class='kds-Text--l']")[0]
    name_text = get_text_excluding_children(web, name_element)
    print(name_text)

    location_element = web.driver.find_elements_by_css_selector("span[class='PurchaseOptions--aisleLocation text-default-900 ml-8']")[0]
    location_text = get_text_excluding_children(web, location_element)
    location_text_parsed = location_text[11:]
    location_text_parsed = location_text_parsed[:-14]
    print(location_text_parsed)

    food_dict[i] = {
        'price': price,
        'name': name_text,
        'location': location_text_parsed,
        'link': link
    }

    #step
    i = i+1
    total = total + price

food_dict['Total'] = total
#%%
# print(food_dict)

#%%
import json
json.dump(food_dict, open( r"C:\Users\pkzr3\Coding\grocery-scraping\output_06112020.json", 'w' ) )


#%%
with open(r"C:\Users\pkzr3\Coding\grocery-scraping\output_06112020.json", 'r') as read_file:
    food_dict_data = json.load(read_file)