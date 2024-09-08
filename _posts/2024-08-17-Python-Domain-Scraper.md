---
title:  "Scraping Domain.com.au with Python to CSV"
date:   2023-10-24 5:34:00
tags: "Python"
layout: post
toc: true
comments: true
categories: [coding]
tags: [python]
---

I'm been looking for a block of land on domain.com.au lately, instead of clicking through listings I'd rather dump them out into a CSV file, I'd also like to add and calculate some additional fields in the csv file. The fields I've added are calculating the price per square metre for the property and also the distance from my home. I've also added a suburb review URL for the suburb to learn more about what people have to say about living at that location. I also find the altitude is important to know, the higher up you are the colder it gets.

## Features

1. Web scraping of Domain.com.au real estate listings
3. Calculation of custom metrics (price per square meter, distance from a reference point)
4. Altitude retrieval (optional)
5. Output to CSV file

## Usage

Run the script from the command line with optional arguments:

- `--refresh-json`: Fetches fresh data from the website instead of using cached data.
- `--altitude`: Retrieves altitude data for each property (requires additional setup).

## Example Output

```
PS D:\src\python-domain-scraper> python .\app.py --refresh-json --altitude

Distance: 1315.5101556559905 km
JSON data fetched and saved to data.json.
Listing ID: 2019301981
Price: 385000.0
Suburb: WADEVILLE
Address: 33/1157 Stony Chute Road
Latitude: -28.579002
Longitude: 153.12932
Features: {'beds': 2, 'baths': 1, 'parking': 2, 'propertyType': 'AcreageSemiRural', 'propertyTypeFormatted': 'Acreage / Semi-Rural', 'isRural': True, 'landSize': 1.34, 'landUnit': 'ha', 'isRetirement': False}
Altitude: 195.0
Landsize: 13400.0
price_per_sqm: 28.73
url: https://www.domain.com.au/33-1157-stony-chute-road-wadeville-nsw-2474-2019301981
distance: 614.4108863262564
suburb_review_url: https://www.homely.com.au/suburb-profile/wadeville-nsw-2474
.......
```

## Output

The script generates a CSV file named with the current date (e.g., `20240817.csv`) containing the following information for each listing:

- Price
- Suburb
- Address
- Latitude
- Longitude
- Number of bedrooms
- Land size
- Altitude (if `--altitude` flag is used)
- Price per square meter
- Listing URL
- Distance from reference point
- Link to suburb review

## Key Calculations

### Price per Square Meter

Calculated as: `total_price / land_size_in_sqm`

This metric allows for standardized comparison between properties of different sizes.

### Distance Calculation

Uses the Haversine formula to calculate the distance between two points on Earth given their latitude and longitude coordinates. This is so I can sort the properties by distance to my home and I can browse the closest properties first.

## Notes

- The script uses rotating user agents to mimic different browsers and avoid detection as a bot.
- Altitude data retrieval is optional and requires additional setup (not detailed in this documentation).
- The script is set to search for properties within a specific price range and land size, which can be modified in the `url` variable.

![alt text](/images/2024-08-17/csv.png)

```python
import requests
from bs4 import BeautifulSoup
import json
import random
import csv
import re
import argparse
from typing import Optional
from altitude import get_altitude
from distance import haversine
from datetime import datetime

my_lat = -33.85682540265101
my_long = 151.21503029598466
today_date = datetime.now().strftime('%Y%m%d')

# List of common user agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
]

# URL of the real estate listings
# url = "https://www.domain.com.au/sale/tamworth-nsw-2340/?excludeunderoffer=1&lastsearchdate=2024-08-04t16:02:33.796z"
url = "https://www.domain.com.au/sale/?price=0-750000&excludeunderoffer=1&landsize=4046-202300&landsizeunit=m2&sort=dateupdated-desc&state=nsw"

# Laguna
#url = "https://www.domain.com.au/sale/laguna-nsw-2325/?price=0-1000000&excludeunderoffer=1&landsize=2000-any&landsizeunit=m2&sort=dateupdated-desc"

headers = {
    'User-Agent': random.choice(user_agents)
}

# Function to parse price
def parse_price(price_str: str) -> Optional[float]:
    # Only process if the price starts with a dollar sign and contains numeric values
    if price_str.startswith('$') and re.match(r'^\$\d+(\,\d{3})*(\.\d{2})?$', price_str):
        # Remove non-numeric characters except decimal point
        price_str = re.sub(r'[^\d.]', '', price_str)
        try:
            return float(price_str)
        except ValueError:
            return None
    return None

def convert_land_size(landsize: float, landunit: str) -> float:
    """
    Convert land size to square meters based on the land unit.

    :param landsize: The size of the land.
    :param landunit: The unit of the land size ('m²', 'sqm', 'ha', etc.).
    :return: Land size in square meters.
    """
    # Convert the land size to square meters based on the unit
    if landunit.lower() in ['ha', 'hectare']:
        return landsize * 10000  # Convert hectares to square meters
    elif landunit.lower() in ['m²', 'sqm', 'square meters']:
        return landsize  # Already in square meters
    else:
        raise ValueError(f"Unknown land unit: {landunit}")


# Function to calculate price per square meter
def calculate_price_per_sqm(price: Optional[float], land_size: Optional[float]) -> Optional[float]:
    if price is not None and land_size is not None and land_size > 0:
        return round(price / land_size, 2)
    return None



# Function to fetch and save JSON data
def fetch_and_save_json():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        script_tag = soup.find('script', id='__NEXT_DATA__', type='application/json')
        json_data = json.loads(script_tag.string)
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        print("JSON data fetched and saved to data.json.")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# Function to read JSON data from file
def read_json():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Main function to process the data and write to CSV
def main(args):
    if args.refresh_json:
        fetch_and_save_json()

    json_data = read_json()

    with open(f'{today_date}.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Price', 'Suburb', 'Address', 'Latitude', 'Longitude', 'Beds', 'Landsize', 'Altitude', 'Price_per_sqm', 'url', 'distance', 'Review'])

        listings_map = json_data['props']['pageProps']['componentProps']['listingsMap']
        for listing_id, listing_info in listings_map.items():
            listing_model = listing_info.get('listingModel', {})
            price_str = listing_model.get('price', 'N/A')
            price = parse_price(price_str)
            address_info = listing_model.get('address', {})
            street = address_info.get('street', 'N/A')
            suburb = address_info.get('suburb', 'N/A')
            state = address_info.get('state', 'N/A')
            postcode = address_info.get('postcode', 'N/A')
            address = f"{street}"
            latitude = address_info.get('lat', 'N/A')
            longitude = address_info.get('lng', 'N/A')
            features = listing_model.get('features', {})
            beds = features.get('beds', 'N/A')
            landsize = features.get('landSize', 'N/A')
            landunit = features.get('landUnit', 'N/A')
            url = listing_model.get('url', 'N/A')
            distance = 'N/A'

            if landsize != 'N/A' and landunit != 'N/A':
                landsize = convert_land_size(landsize, landunit)

            if latitude != 'N/A' and longitude != 'N/A':
                distance = haversine(float(latitude), float(longitude), my_lat, my_long)

            altitude = 'N/A'
            if args.altitude:
                if latitude != 'N/A' and longitude != 'N/A':
                    altitude = get_altitude(float(latitude), float(longitude))

            if url != 'N/A' :
                url = f"https://www.domain.com.au{url}"

            suburb_review_url = f'https://www.homely.com.au/suburb-profile/{suburb.lower().replace(" ","-")}-{state.lower()}-{postcode.lower()}'

            price_per_sqm = calculate_price_per_sqm(price, landsize)

            # Print the extracted information
            print(f"Listing ID: {listing_id}")
            print(f"Price: {price}")
            print(f"Suburb: {suburb}")
            print(f"Address: {address}")
            print(f"Latitude: {latitude}")
            print(f"Longitude: {longitude}")
            print(f"Features: {features}")
            print(f"Altitude: {altitude}")
            print(f"Landsize: {landsize}")
            print(f"price_per_sqm: {price_per_sqm}")
            print(f"url: {url}")
            print(f"distance: {distance}")
            print(f"suburb_review_url: {suburb_review_url}")
            print('-' * 40)

            writer.writerow([price_str, suburb, address, latitude, longitude, beds, landsize, altitude, price_per_sqm, url, distance, suburb_review_url])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Real estate data scraper')
    parser.add_argument('--refresh-json', action='store_true', help='Refresh JSON data from the remote website')
    parser.add_argument('--altitude', action='store_true', help='Retrieve Altitude data')
    args = parser.parse_args()
    main(args)

```

## Ideas for future improvements

* Retrieving more climate data, on google if you search for a placename climate google will give you graphs of annual temperature and rainfall, this is pretty importment information, would be good to be able to see this at a glance :

<img src="images/2024-08-18-08-57-58.png">

## Conclusion

So far I am finding the distance column the most valuable, it's nice to sort by distance and start with reviewing the properties closest to my home. If you want to have a weekend property the drive time is a key factor, luckily I noticed that each domain.com.au property listing in the json code has listed the properties lat and long, from there you can specify your location lat and long and than use a formula to calculate the distance.