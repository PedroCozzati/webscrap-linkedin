import re
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import requests
from controllers.web_connection import WebConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import time

option = webdriver.ChromeOptions()
option.add_argument("--start-maximized")
driver = webdriver.Chrome(options=option)

# option = webdriver.EdgeOptions()
# option.add_argument("--start-maximized")
# driver = webdriver.Edge(options=option)

estado = "São Paulo,"
cidade = "São Paulo,"
pais = "Brazil"
trabalho = "Desenvolvedor"
distance = "40"

max_pages = 1

connection = WebConnection(
    driver=driver,
    url="https://www.linkedin.com/jobs/",
    keyword=trabalho,
    estado=estado,
    cidade=cidade,
    pais=pais,
    distance=distance,
)

data = connection.start_connection()
soup = BeautifulSoup(data)

title_list = []
company_list = []
location_list = []
time_opened_list = []
link_list = []
description_list = []
application_list = []
cleaned_jobs_infos = []
experience_level_list = []
job_type_list = []
role_list = []
sector_list = []

def cleaning_job_info(input, output):
    job_infos_aux = str(input).split("\n")
    for info in job_infos_aux:
        if info.strip():
            output.append(info.strip())

def get_info():
    pagina = 0
    have_more_jobs_button = driver.find_element(
        By.CSS_SELECTOR, "button.infinite-scroller__show-more-button"
    )

    while have_more_jobs_button and pagina <= max_pages:
        jobs = driver.find_elements(By.CSS_SELECTOR, "div[data-row]")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        pagina = pagina + 1
        print("Atualmente na página: " + str(pagina))

        if driver.find_element(
            By.CSS_SELECTOR, "button.infinite-scroller__show-more-button"
        ):
            try:
                ActionChains(driver).move_to_element(have_more_jobs_button).click(
                    have_more_jobs_button
                ).perform()
            except:
                print("Loader automático...")

        time.sleep(2)

    for job in jobs:
        title = job.find_element(By.TAG_NAME, "h3").text.strip()
        company = job.find_element(By.TAG_NAME, "h4").text.strip()
        location = job.find_element(
            By.CSS_SELECTOR, "span.job-search-card__location"
        ).text.strip()
        time_opened = job.find_element(By.CSS_SELECTOR, "time").text.strip()
        link = job.find_element(By.TAG_NAME, "a").get_attribute("href")

        # Entrando na pagina de detalhes
        job_details = requests.get(link)
        job_details_soup = BeautifulSoup(job_details.text, "html.parser")
        # Timer necessário para carregar a nova pagina a tempo da informação aparecer
        time.sleep(3)

        # Descrição da vaga
        if job_details_soup.select_one("div.description__text.description__text--rich"):
            job_details_description = (
                job_details_soup.select_one(
                    "div.description__text.description__text--rich"
                )
                .select_one("section")
                .select_one("div")
                .get_text()
                .strip()
            )
        else:
            job_details_description = "NA"

        # Pegando informação de numero de aplicações da vaga
        if job_details_soup.find("figcaption", class_="num-applicants__caption"):
            job_applications = (
                job_details_soup.find("figcaption", class_="num-applicants__caption")
                .get_text()
                .strip()
            )
        else:
            job_applications="NA"

        # Informações gerais da vaga (nivel de experiencia, tipo de emprego, função, etc)
        if job_details_soup.find("ul", class_="description__job-criteria-list"):
            job_infos = (
                job_details_soup.find("ul", class_="description__job-criteria-list")
                .get_text()
                .strip()
            )
        else:
            job_infos ="NA"

        cleaning_job_info(job_infos, cleaned_jobs_infos)

        print(cleaned_jobs_infos)

        title_list.append(title)
        company_list.append(company)
        location_list.append(location)
        time_opened_list.append(time_opened)
        link_list.append(link)
        description_list.append(job_details_description)
        application_list.append(job_applications)

        try:
            experience_level_list.append(cleaned_jobs_infos[1])
        except:
            experience_level_list.append("NA")
            
        try:
            job_type_list.append(cleaned_jobs_infos[3])
        except:
            job_type_list.append("NA")
            
        try:
            role_list.append(cleaned_jobs_infos[5])
        except:
            role_list.append("NA")

        try:
            sector_list.append(cleaned_jobs_infos[7])
        except:
            sector_list.append("NA")
            
        cleaned_jobs_infos.clear()

    driver.close()


get_info()

df = pd.DataFrame.from_dict(
    {
        "title": title_list,
        "company": company_list,
        "location": location_list,
        "time_opened": time_opened_list,
        "link": link_list,
        "applications": application_list,
        "experience_level": experience_level_list,
        "job_type": job_type_list,
        "role": role_list,
        "sectors": sector_list,
        "description": description_list,
    }
)

df.to_csv("results/linkedin_jobs.csv", sep=",", index=False)
