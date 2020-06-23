from selenium import webdriver 
from bs4 import BeautifulSoup 
import time 
import datetime
import pandas as pd
import os
import mail

"""
Program to scrape gpus of a website and notify me if 
prices dropped with an email.
Script will probably not work anymore if the site gets an 
update
"""

class Scraper():
    def __init__(self):

        #Define url to scrape from
        url = "https://www.megekko.nl/Computer/Componenten/Videokaarten/Nvidia-Videokaarten?f=f_vrrd-3_s-populair_pp-250_p-1_d-list_cf-"

        #Define path to webdriver for selenium
        PATH = 'E:/win21/chromedriver_win32/chromedriver.exe'

        self.driver = webdriver.Chrome(PATH)

        replacements = {"-":"", " ":"", ":":"", ".":""}

        self.today = str(self.replace(str(datetime.date.today()), replacements))
        self.yesterday = str(int(self.today) - 1)

        self.fname = self.today + "products.csv"
        self.f = open(self.fname, 'a')

        self.fname2 = self.yesterday + "products.csv"
        self.f2 = open(self.fname2, "a")

        self.names = []
        self.prices = []

        #Open chrome tab
        self.driver.get(url)

        self.filter()
        self.get_and_export_data(3)
        
        self.go_to_amd()
        self.filter()
        self.get_and_export_data(1)

        self.compare(self.today + "products.csv", self.yesterday + "products.csv")
       
        self.driver.close()
        self.f.close()
        self.f2.close()

    def filter(self):
        option_menu = self.driver.find_element_by_xpath("html/body/div/main/div[1]/div[5]/div[1]/div[3]/div[1]/select")
        option_menu.click()

        option_3 = self.driver.find_element_by_xpath("html/body/div/main/div[1]/div[5]/div[1]/div[3]/div[1]/select/option[3]")
        option_3.click()
        time.sleep(2)

        delivery_time = self.driver.find_element_by_xpath("html/body/div/main/div[1]/div[4]/div/div[1]/div[2]/div/div[1]/input")
        delivery_time.click()
        time.sleep(2)

    #Combine the get_data and export_data function
    def get_and_export_data(self, scraped_pages):
        #Loop trough each page and get its data
        for i in range(scraped_pages):
            self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            self.get_data()
        self.export_data()   

    def next_page(self): 
        time.sleep(1)
        next_page_element = self.driver.find_element_by_xpath("html/body/div/main/div[1]/div[5]/div[5]/div/div[2]/div[3]/img")
        self.driver.execute_script("arguments[0].click();", next_page_element)
        time.sleep(2)

    def export_data(self):
        #Create columns containing the data
        raw_data = {"name": self.names,
                    "price": self.prices}

        self.df = pd.DataFrame(raw_data, columns = ['name', 'price'])
        self.df.to_csv(self.today + "products.csv", index=False)
        
    def append_data(self):
        self.names.append(self.name)
        self.prices.append(self.price)

    
    #Get all data from the site
    def get_data(self):
        for self.container in self.soup.find_all('div', {'class':'productList'}):
            
            self.name = self.container.a["title"]
        
            price_container = self.container.find_all('div', {'class':'euro'})
            self.price = price_container[0]

            replacements = {",":"", "-":"", '"':""}
            self.price = self.price.text.strip()
            self.price = self.replace(str(self.price), replacements)
            self.price = "€" + self.price + ",-"
            print(self.name)
            print(self.price + "\n")

            self.append_data()
        self.next_page()     

    #Compare files from today and yesterday
    def compare(self, file1, file2):
        #Check if file is empty
        empty = False
        if os.stat(self.yesterday + "products.csv").st_size == 0:
            print("File is empty")
            empty = True

        """
        If the file is not empty, merge the files and drop
        the duplicate rows so we keep the rows with same
        gpu names but different prices. We will export 
        these into a csv file named gpus.csv
        """
        if not empty:
            df1 = pd.read_csv(file1)
            df2 = pd.read_csv(file2)
        
            df_merged = pd.concat([df1, df2])   
            df_merged.drop_duplicates(keep=False, inplace=True)
            
            if not df_merged.empty:
                df_merged.to_csv("gpus.csv")

    #Function to replace some garbage on the price/name of gpu
    def replace(self, text, dictionary):    
        for k, v in dictionary.items():
            text = text.replace(k, v)
        return text

    def go_to_amd(self):
        gpus_elem = self.driver.find_element_by_xpath("html/body/div/main/div[1]/div[1]/ol/li[4]/a/span")
        gpus_elem.click()

        amd_gpus_elem = self.driver.find_element_by_xpath("html/body/div/main/div[1]/div[4]/div[2]/h2/a")
        amd_gpus_elem.click()
        time.sleep(2)

#Create class instances
if __name__ == '__main__':
    scraper = Scraper()
    email = mail.Email()

import os
replacements = {"-":"", " ":"",":":"", ".":""}
today = str(scraper.replace(str(datetime.date.today()), replacements))
day_before_yesterday = str(int(today) - 2)

#Remove file from day before yesterday because we don't need it anymore
try:
    os.remove(day_before_yesterday + "products.csv")

except FileNotFoundError:
    print("File doesn't exist!")
