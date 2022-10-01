from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

FILENAME = 'Affiliate515 - Sheet1.csv'
COLUMNS = ['No',
            'ID',
            'Title',
            'Campaign-Tagged URL']
START_ROW_NUM = 5
HEADER = {
    'authority': 'www.dickssportinggoods.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9',
}

url = "https://www.gramedia.com/products/almond?utm_medium=MBSAffiliate&utm_source=Affiliate515&utm_campaign=Hackathon"


def get_browser():
    options = Options()
    #options.add_argument(f"user-data-dir={os.getcwd()}cookies")
    options.add_argument("start-maximize")
    try:options.add_experimental_option("excludeSwitches", ["enable-logging"])    
    except: print("Exception: excludeSwitches - enable-logging")
    mybrowser = webdriver.Chrome(options=options)
    return mybrowser

def get_book_data(url):
    mybrowser = get_browser()
    mybrowser.maximize_window()
    mybrowser.get(url)
    time.sleep(10)
    book_title = mybrowser.find_element(by=By.XPATH,value="//div[@class='book-title']").text
    time.sleep(5)
    author = mybrowser.find_element(by=By.XPATH, value="//span/a").text
    time.sleep(5)
    desc = mybrowser.find_element(by=By.XPATH, value="//div[@class='product-desc']").text
    time.sleep(5)
    detail = mybrowser.find_element(by=By.XPATH, value="//div[@class='detail-section']").text
    time.sleep(5)
    price_promo = mybrowser.find_element(by=By.XPATH, value="//div[@class='price-promo']").text
    time.sleep(5)   
    badge_discount = mybrowser.find_element(by=By.XPATH, value="//div[@class='badge-discount']").text
    time.sleep(5)  
    discounted_price = mybrowser.find_element(by=By.XPATH, value="//div[@class='price-from']").text
    time.sleep(5)
    img_url = mybrowser.find_element(by=By.XPATH, value="//div[@class='image']/img").get_attribute('src')
    return book_title,author,url, desc, detail,price_promo,badge_discount,discounted_price,img_url

def get_dataframe(filename=FILENAME,columns=COLUMNS, start_row_num = START_ROW_NUM):
    orig_df = pd.read_csv(f'{filename}')
    df = orig_df[start_row_num-1:]
    df.columns = columns
    return df

if __name__=='__main__':
    import pandas as pd
    import csv

    
    with open('data.csv', 'a+', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        col_names = ['Book Title',
                    'Author',
                    'URL',
                    'Description',
                    'Detail',
                    'Price',
                    'Discount',
                    'Disc. Price',
                    'Img URL']
        writer.writerow(COLUMNS)
        data = []
        df = get_dataframe()
        for index,row in df.iterrows():
            url = row[-1]
            try:
                data.append(get_book_data(url))
                print(data[-1])
                writer.writerow(data[-1])
            except:
                pass
