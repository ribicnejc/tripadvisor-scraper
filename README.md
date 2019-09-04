# Overall

## Prerequisites 
    go to root folder -> /masters

## List spiders
    scrapy list
    
## Start scraper
### 0. Start runner.py
    python3.7 runner.py
    
### 1. Start attraction crawler
    scrapy crawl locations

### 2. Start review crawler
This crawler will fetch reviews from attraction which were 
fetched from previous *location crawler*
 
    scrapy crawl reviews
    
        
### 3. Start review crawler (all languages)
This crawler works with headless browser called gecko.

    python gecko_runner.py        
        
# Deployment (steps)
## 1. Project
    pip install -r requirements.txt
## 2.1. Driver (chrome)
    - LATEST=$(wget -q -O - http://chromedriver.storage.googleapis.com/LATEST_RELEASE)
    - wget http://chromedriver.storage.googleapis.com/$LATEST/chromedriver_linux64.zip
    - unzip chromedriver_linux64.zip && sudo ln -s $PWD/chromedriver /usr/local/bin/chromedriver
## 2.2. Driver(firefox)
    - wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
    - tar -xvzf geckodriver-v0.24.0-linux64.tar.gz
    - chmod +x geckodriver
    - sudo ln -s $PWD/geckodriver /usr/local/bin/geckodriver
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


# Dockerise deployment
## Steps
    pip install scrapy-splash

    docker pull scrapinghub/splash
    
    docker run -p 8050:8050 scrapinghub/splash
    
# SSH Session scraping
Use TMux

Create new session

    tmux new -s scrap-locations

Start new process

    scrapy crawl locations
    
Detach tmux process
    
    press: ctrl + b... then relase and press d after
    
List sessions

    tmux list-sessions
    
Attach to previous session
    
    tmux attach -t scrap-locations
        
    