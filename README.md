# To myself notes

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
    
## Opened issues
    driver cannot open display!!!
    reason -> ssh with windows running probably