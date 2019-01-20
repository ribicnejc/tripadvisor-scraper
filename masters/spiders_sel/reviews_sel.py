from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def get_coordinates(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(5)

    coord_url = driver.find_element_by_css_selector("div.staticMap img").get_attribute("src")
    print(coord_url)
    # elem = driver.find_element_by_name("q")
    # elem.clear()
    driver.close()
    return coord_url
