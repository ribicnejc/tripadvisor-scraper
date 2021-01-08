# SQL Queries

### 1. Query all attractions containing Cherno word
    select * from locations
    JOIN provinces p on locations.attraction_parent_url = p.province_url
    where p.province_url like '%Cherno%'
    order by province_name

### 2. Query Odessa locations
    select * from provinces p
    join locations l on p.province_url = l.attraction_parent_url
    where country = 'ukraine'
    and region_name = 'Odessa Oblast'

### 3. Query Slovenian locations