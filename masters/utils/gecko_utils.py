def get_gecko_driver():
    gecko_options = Options()
    if settings.HEADLESS_MODE:
        gecko_options.add_argument("--headless")
    service_args = ['--verbose']

    profile

    # driver = webdriver.PhantomJS(service_args=['--load-images=no'])
    driver = webdriver.Firefox(firefox_profile=profile, options=gecko_options, capabilities=capabilities)
    driver = webdriver.Chrome(
        chrome_options=chrome_options,
        service_args=service_args)
    # driver.add_cookie({'name': 'TALanguage', 'value': 'ALL'})
    driver.get(url)
    driver.implicitly_wait(2)
