# Overall

## Prerequisites 
    go to root folder -> /masters

## List spiders
    scrapy list
    
## Start spider
    scrapy crawl reviews
    
    
# Deployment (steps)
## 1. Project
    pip install -r requirements.txt
## 2. Driver
    - LATEST=$(wget -q -O - http://chromedriver.storage.googleapis.com/LATEST_RELEASE)
    - wget http://chromedriver.storage.googleapis.com/$LATEST/chromedriver_linux64.zip
    - unzip chromedriver_linux64.zip && sudo ln -s $PWD/chromedriver /usr/local/bin/chromedriver
    
## 3. Run Scraper    
    python runner.py
    
## 4. Chrome
    - wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    - sudo dpkg -i google-chrome-stable_current_amd64.deb
    
## Closed issues
    driver cannot open display!!!
    reason -> ssh with windows running probably
Fix was in selenium. We created selenium scraper that way, that chrome browser is
never visually shown. `--headless` mode!