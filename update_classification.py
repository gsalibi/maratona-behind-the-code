import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import csv

option = Options()
option.headless = True

urls = ["https://maratona.dev/pt/ranking?c=1", "https://maratona.dev/pt/ranking?c=2", 
        "https://maratona.dev/pt/ranking?c=3", "https://maratona.dev/pt/ranking?c=4"]
challenges = [dict(), dict(), dict(), dict()]
        
participants = dict()



for i in range(len(urls)):
    driver = webdriver.Firefox(options=option)
    driver.get(urls[i])
    time.sleep(10)

    element = driver.find_element_by_xpath("//*[@id='__next']/main/div/div[3]")
    html_content = element.get_attribute('outerHTML')

    soup = BeautifulSoup(html_content, 'html.parser')

    table = soup.findAll(class_='styles_participant__YQRLp')

    points = 100
    for participant in table:
        name = participant.p.text.split(' ',1 )[1]
        position = participant.p.text.split(' ',1 )[0][:-1]
        
        challenges[i][name] = position
        
        if name in participants:            
            participants[name] = participants[name] + points
        else:
            participants[name] = points
            
        points -= 1
        
    driver.quit()



data = sorted(participants.items(), key=lambda x: x[1], reverse=True)

for i in range(len(data)):
    for challenge in challenges:
        if data[i][0] in challenge:
            data[i] = data[i] + (challenge[data[i][0]],)
        else:
             data[i] = data[i] + tuple("-",)


# opening the csv file in 'w+' mode 
file = open('classificados.csv', 'w+', newline ='') 
  
# writing the data into the file 
with file:     
    write = csv.writer(file) 
    write.writerow(['participante','pontos (101 - posição)', 'desafio 1', 'desafio 2', 'desafio 3', 'desafio 4'])
    write.writerows(data) 