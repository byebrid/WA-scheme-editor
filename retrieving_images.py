import os
import requests
from bs4 import BeautifulSoup as BS

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
WEAPONS_DIR = os.path.join(BASE_DIR, 'weapons_images')


# r = requests.get(url="https://worms2d.info/Weapons")
# print(r.status_code)
# soup = BS(r.content, "html.parser")

with open('bs.html', 'r') as f:
    soup = BS('\n'.join(f.readlines()), 'html.parser')

table = soup.find('table')
table_rows = table.find_all('tr')[2:]

WORMS_URL = "https://worms2d.info"
for row in table_rows:
    row_urls = row.find_all('a')
    for row_url in row_urls:
        weapon_url = WORMS_URL + row_url['href']
        r = requests.get(url=weapon_url)
        if not r.ok:
            print("BAD RESPONSE!")
        else:
            weapon_soup = BS(r.content, 'html.parser')
            img = weapon_soup.find('img')
            imgname = img['alt']
            print(f"Found {imgname}")
            img_url = WORMS_URL + img['src']
            img_r = requests.get(img_url)
            if img_r.ok:
                with open(os.path.join(WEAPONS_DIR, imgname), 'wb') as f:
                    f.write(img_r.content)
                print(f"Downloaded {imgname}")
