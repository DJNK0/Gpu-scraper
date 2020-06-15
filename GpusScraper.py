from selenium import webdriver 
from bs4 import BeautifulSoup 
import time 
import datetime
import pandas as pd

class Scraper():
    def __init__(self):
        url = 'https://www.megekko.nl/Computer/Componenten/Videokaarten'
        PATH = 'E:/win21/chromedriver_win32/chromedriver.exe'

        self.driver = webdriver.Chrome(PATH)

        self.today = str(datetime.date.today()).replace('-', '').replace(' ', '').replace(':','').replace('.', '')
        self.yesterday = str(int(self.today) - 1)

        self.fname = self.today + ".csv"
        self.f = open(self.fname, 'a')
        
        self.fname2 = self.yesterday + ".csv"
        self.f = open(self.fname, "a")

        self.names = []
        self.deliverytimes = []
        self.prices = []

        self.driver.get(url)

        self.filter()
        self.main(28)
        self.compare(self.today + "products.csv", self.yesterday + "products.csv")
       
        self.driver.close()

    def main(self, ScrapedPages):
        #Loop trough each page and get its data
        for i in range(ScrapedPages):
            self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            self.get_data()
        self.export_data()   

    #Function to go to the next page
    def next_page(self):
        time.sleep(1)
        next_page_element = self.driver.find_element_by_xpath('html/body/div[1]/main/div[1]/div[5]/div[1]/div[3]/img')
        self.driver.execute_script("arguments[0].click();", next_page_element)
        time.sleep(1)

    def export_data(self):
        raw_data = {"name": self.names,
                    "deliverytime": self.deliverytimes,
                    "price": self.prices}

        self.df = pd.DataFrame(raw_data, columns = ['name', 'deliverytime', 'price'])
        self.df.to_csv(self.today + "products.csv")
        
    
    def append_data(self):
        self.names.append(self.name)
        self.deliverytimes.append(self.delivery_time)
        self.prices.append(self.price)

        print(self.name) 
        print(self.delivery_time)
        print(self.price + "\n") 

    def get_data(self):
        for self.container in self.soup.find_all('div', {'class':'navProductListitem'}):
            self.name = self.container.div.img['title']

            price_container = self.container.find_all('div', {'class':'euro'})
            self.price = price_container[0]
            self.price = self.price.text.strip()
            self.price = self.price.replace(",", "").replace("-", "")
            self.price += ",-"

            delivery_time_container = self.container.find_all('div', {'class':'voorraad'})
            self.delivery_time = delivery_time_container[0].text.strip()
            self.append_data()
        self.next_page()    

    def compare(self, file1, file2):
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
        
    def filter(self):
        amd_checkbox_elem = self.driver.find_element_by_xpath('html/body/div/main/div[1]/div[5]/div[3]/div/div[5]/div/div[2]/label')
        self.driver.execute_script("arguments[0].click();",amd_checkbox_elem)
        time.sleep(2)
         
        nvidia_checkbox_elem = self.driver.find_element_by_xpath('html/body/div/main/div[1]/div[5]/div[3]/div/div[5]/div/div[1]/label')
        self.driver.execute_script("arguments[0].click();",nvidia_checkbox_elem)
        time.sleep(2)

if __name__ == "__main__":
    app = Scraper()
