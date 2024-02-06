from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import pandas as pd
import time

def log(message):
    now = datetime.now()
    with open ('logs.txt', 'a') as f:
        f.write(f'{now.strftime("%Y-%m-%d %H:%M:%S")} --- {message}\n')
        
log('Program start')

def extract_scrapping():
    '''
    This function gather data from website, make test .csv file with raw data.
    Further than that, redirect data frame to the next step of ETL process.
    '''
    log('Start scrapping')
    options = Options()
    # options.add_argument('--headless=new')
    # options.add_argument('window-size=1920x1080')

    web = 'https://www.audiobooks.com/browse'
    path = './chromedriver.exe'
    driver = webdriver.Chrome(options=options)
    driver.get(web)
    driver.maximize_window() #not effiecient because of headless

    #pagination
    pagination = driver.find_element(By.XPATH, '//ul[contains(@class, "pagination")]')
    pages = pagination.find_elements(By.XPATH, 'li')
    book_title = []
    book_author = []
    book_lenght = []
    book_price = []
    page = 1
    while True:
        if page==2:
            break
        log(f'Scrapping: page {page}')
        try:
            container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'books')))
        except:
            break
        #container = driver.find_element(By.CLASS_NAME, 'books')
        products = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class = "bb-link  "]')))
        #products = container.find_elements(By.XPATH, '//div[@class = "bb-link  "]')
        for product in products:
            print(f'-------------PAGE {page}-----------')
            # title = product.find_element(By.XPATH, './/h6[contains(@class, "book__info__title")]').text
            title = WebDriverWait(product, 5).until(EC.presence_of_element_located((By.XPATH, './/h6[contains(@class, "book__info__title")]'))).text
            book_title.append(title)
            print(title)
            #author = product.find_element(By.XPATH, './/h6[contains(@class, "book__info__author")]').text
            author = WebDriverWait(product, 5).until(EC.presence_of_element_located((By.XPATH, './/h6[contains(@class, "book__info__author")]'))).text
            book_author.append(author)
            print(author)
            #leng = product.find_element(By.XPATH, './/span[contains(@class, "book__info__meta--duration")]').text
            leng = WebDriverWait(product, 5).until(EC.presence_of_element_located((By.XPATH, './/span[contains(@class, "book__info__meta--duration")]'))).text
            book_lenght.append(leng)
            print(leng)
            try:
                price = WebDriverWait(product, 2).until(EC.presence_of_element_located((By.XPATH, ".//span[contains(@class, 'book__info__meta--price')]"))).text
                book_price.append(price)
            except Exception as e:
                print(e)
                book_price.append('Coming soon')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        next_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//li[contains(@class, 'next')]")))
        time.sleep(1)
        next_page.click()
        page+=1
    driver.quit()
    df_books = pd.DataFrame({
        'Book Title': book_title,
        'Author': book_author,
        'Lenght': book_lenght,
        'Price': book_price
    })
    df_books.index.name = 'ID'
    df_books.to_csv('raw_books.csv')
    log('The end of scrapping')
    return df_books

data = extract_scrapping()

def transforming(data, author='Mark Manson'):
    log('Transforming started')
    filter_a = (data['Author'].str.upper() == f'BY {author.upper()}')
    data.loc[filter_a, 'Price'] = data.loc[filter_a, 'Price'].apply(lambda x: f'${float(x[1:])-2}')
    print('----------------------------------------------------')
    print(data)
    log('Transforming ended')

def load_to_csv(to_load=data, filename = 'final_data.csv'):
    log('Loading to .csv started')
    to_load.to_csv(filename)
    log('Loading to .csv is done')

transforming(data)
load_to_csv()