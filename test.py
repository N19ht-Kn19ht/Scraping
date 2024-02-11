import requests
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from datetime import datetime

from db import insert_data


def start_connect(page, s):
    if page == 1:
        r = s.get("https://auto.ria.com/car/used/")
    else:
        r = s.get("https://auto.ria.com/car/used/" + "?page=" + str(page))

    html = BS(r.content, 'html.parser')

    return html


def get_phone(link):
    driver = webdriver.Chrome()

    driver.implicitly_wait(10)  # Set implicit wait timeout
    driver.set_page_load_timeout(10)  # Set page load timeout

    driver.get(link)
    el = driver.find_element("xpath", "//*[@id='phonesBlock']/div/span/a")
    driver.execute_script("arguments[0].click();", el)

    phone_number = driver.find_element("xpath", "//*[@id='show-phone']/div[2]/div[2]/div[2]")
    if phone_number:
        phone_string = phone_number.text.replace(" ", "").replace("(", "").replace(")", "")
        phone = int('38' + phone_string)
    else:
        phone = None

    print(phone)

    return phone


def data():
    s = requests.Session()

    # Increase the redirect
    s.max_redirects = 1000000

    print("Data is started parcing!")

    page = 1

    # Get data from each page
    while True:
        html = start_connect(page, s)

        # Get links from page
        links = html.select("a[class='address']")

        if len(links):
            for link in links:
                link = link.get('href')
                print(link)

                # Get data from each link
                car_req = requests.get(link)
                car_html = BS(car_req.content, 'html.parser')

                # skip sold cars
                sold_cars = car_html.find_all("div", class_="notice_head")
                if sold_cars:
                    continue

                # Get titles
                title = None
                for title in car_html.select_one('h1', class_='head'):
                    title = title.text.lstrip()
                    print(title)

                # Get price_usd
                usd = None
                for price_usd in car_html.select("div.price_value > strong"):
                    price = price_usd.text[:-1].replace(" ", "")
                    usd = int(price)
                    print(usd)

                # Get odometer
                mileage = None
                for odometer in car_html.select("div.base-information > span.size18"):
                    mileage = int(odometer.text + '000')
                    print(mileage)

                # Get username or company name
                name = None
                for username in car_html.select("div.seller_info_name", limit=1):
                    name = username.text.lstrip()
                    print(name)

                for company_name in car_html.select("h4.seller_info_name", limit=1):
                    name = company_name.text.lstrip()
                    print(name)

                # Get phone number
                phone = get_phone(link)

                # Get image url
                im_url = None
                for image_url in car_html.find_all('img', class_="outline m-auto", limit=1):
                    im_url = image_url.get('src')
                    print(im_url)

                # Get images count
                res = None
                for count_images in car_html.find_all('div', class_="action_disp_all_block"):
                    count = count_images.text.replace(" Дивитися всі ", "").replace(" фотографій", "")
                    res = int(count)
                    print(res)

                # Get car number
                number = '  '
                for car_number in car_html.find_all('span', class_="state-num ua"):
                    number = car_number.text.strip().replace(
                        " Ми розпізнали держномер авто на фото та перевірили його за реєстрами МВС.", "")
                    print(number)

                # Get car vin
                vin_number = None
                for car_vin in car_html.select("span[class='label-vin']"):
                    vin_number = car_vin.text
                    print(vin_number)

                for car_vin in car_html.select("span[class='vin-code']"):
                    vin_number = car_vin.text
                    print(vin_number)

                # Set timestamp
                dt = datetime.today()
                tm = dt.timestamp()
                print(tm)

                insert_data(link=link, title=title, price_usd=usd, mileage=mileage, name=name, phone=phone,
                            image_url=im_url, count_images=res, car_number=number, car_vin=vin_number, datetime=dt)

                print('\n')

            page =+ 1
        else:
            print("Data is successfully parced!!")
            break

    return
