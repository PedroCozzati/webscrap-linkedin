from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

from controllers.web_connection import WebConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import time

driver = webdriver.Edge()

estado = 'São Paulo,'
cidade = 'São Paulo,'
pais = 'Brazil'
trabalho = 'Desenvolvedor'
distance = '40'

max_pages = 8

connection = WebConnection(
    driver=driver,
    url='https://www.linkedin.com/jobs/',
    keyword=trabalho,
    estado=estado,
    cidade=cidade,
    pais=pais,
    distance=distance
)

data = connection.start_connection()
soup = BeautifulSoup(data)

job_list=[]
title_list=[]
company_list=[]
location_list=[]
time_opened_list=[]
link_list=[]
test_list=[]

def get_info():
    pagina = 0
    have_more_jobs = driver.find_element(By.CSS_SELECTOR, "button.infinite-scroller__show-more-button")
    
    while have_more_jobs and pagina <= max_pages:
        jobs=driver.find_elements(By.CSS_SELECTOR,"div[data-row]")
        button = driver.find_element(By.CSS_SELECTOR, "button.infinite-scroller__show-more-button")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        pagina = pagina+1
        
        print(pagina)
        
        if driver.find_element(By.CSS_SELECTOR, "button.infinite-scroller__show-more-button"):
            try:
                button = driver.find_element(By.CSS_SELECTOR, "button.infinite-scroller__show-more-button")
                ActionChains(driver).move_to_element(button).click(button).perform()
            except:
                print('nada')
                
        time.sleep(2)
    
    for job in jobs:
        title = job.find_element(By.TAG_NAME,'h3').text.strip()
        company = job.find_element(By.TAG_NAME,'h4').text.strip()
        location = job.find_element(By.CSS_SELECTOR,'span.job-search-card__location').text.strip()
        time_opened = job.find_element(By.CSS_SELECTOR,'time').text.strip()
        link = job.find_element(By.TAG_NAME,'a').get_attribute('href') if job.find_element(By.TAG_NAME,'a')  else 'NA'
        
        title_list.append(title)
        company_list.append(company)
        location_list.append(location)
        time_opened_list.append(time_opened)
        link_list.append(link)
    
    driver.close()
    
        
get_info()
len(test_list)

print(len(title_list))
print(len(company_list))
print(len(location_list))
print(len(time_opened_list))

df = pd.DataFrame.from_dict({
    'title': title_list,
    'company':company_list,
    'location':location_list,
    'time_opened':time_opened_list,
    'link':link_list
})

df.to_csv("results/linkedin_jobs.csv", sep=',', index=False)
