from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_coordinates(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # chrome_options.binary_location = '/opt/google/chrome/google-chrome'
    # service_log_path = "{}/chromedriver.log".format("/home/nejc/Desktop/scrapers/trip/")
    service_args = ['--verbose']

    driver = webdriver.Chrome(
        chrome_options=chrome_options,
        service_args=service_args,
        # service_log_path=service_log_path
    )
    driver.get(url)
    driver.implicitly_wait(5)

    coord_url = driver.find_element_by_css_selector("div.staticMap img").get_attribute("src")
    print(coord_url)
    driver.close()
    return coord_url
