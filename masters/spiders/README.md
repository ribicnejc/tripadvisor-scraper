# Steps to scrap tripadviser
## 1. Scrap Provinces
### 1.1 
Use tripadvisor.co.uk as main domain. 
Open second page <https://www.tripadvisor.co.uk/Attractions-g274862-Activities-oa20-Slovenia.html>.
Click on Popularity button to sort it in ascending way. 
The page will redirect you to main page and then you have to click back to get back on second page - order should be now 
ascending.

### 1.2
Go to the last page and download the last and second last site. Save it in *.html format - single page. 
Follow the pattern <first|second.html> and save it into the ```missing_data\slo``` folder - following the 
country code pattern.
That way parser will check extra folder (missing_data/<country_code>) and parse custom downloaded sites as well.

### 1.3
In file ```provinces_spider.py``` set main province url example </Attractions-g294473-Activities-oa20-Ukraine.html>

### 1.4
Run command bellow
    
    python scrap_provinces.py

### 1.5
Scraped data is available under ```scraped_data``` folder under country code which is 
set in settings.

## 2. Scrap Locations
### 2.1
Set country code in setting 
    
    COUNTRY = "slo"

### 2.2
Clean file located in ```masters\logs\scraped_locations.log```

### 2.3
Run command bellow

    python scrap_locations.py

### 2.3
Scraped data is available under ```scraped_data``` folder under country code which is 
set in settings.

## 3. Scrap Reviews