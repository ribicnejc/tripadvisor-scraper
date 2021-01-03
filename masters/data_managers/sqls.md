# SQL Queries

### 1. Query all attractions containing Cherno word
    select * from locations
    JOIN provinces p on locations.attraction_parent_url = p.province_url
    where p.province_url like '%Cherno%'
    order by province_name
