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


### 4. Group by location type
    select attraction_type, count(attraction_type) as sum
    from provinces p
             join locations l on p.province_url = l.attraction_parent_url
             join reviews r on l.attraction_url = r.parent_url
    where country = 'slovenia'
    --   and r.review_date > 20190101
    --   and r.review_date < 20200101
      and r.review_date > 20200101
      and r.review_date < 20210101
    group by attraction_type
    order by sum desc
    limit 15