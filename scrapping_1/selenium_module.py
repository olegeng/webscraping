from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
driver = webdriver.Chrome()
driver.get("https://www.adamchoi.co.uk/overs/detailed")
print(driver.title)
all_matches_button = driver.find_element(By.XPATH , "//label[@analytics-event='All matches']")
driver.execute_script("arguments[0].click();", all_matches_button)

#dropdown
dropdown = Select(driver.find_element(By.ID, 'country'))
dropdown.select_by_visible_text('Ukraine')
time.sleep(3)



all_records = driver.find_elements(By.TAG_NAME, 'tr')
date = []
home_team = []
score = []
away_team = []
results = {'Date': date,
           'Home Team': home_team,
           'Score': score,
           'Away Team': away_team}
for match in all_records:
    date.append(match.find_element(By.XPATH, './td[1]').text)
    home_team.append(match.find_element(By.XPATH, './td[2]').text)
    score.append(match.find_element(By.XPATH, './td[3]').text)
    away_team.append(match.find_element(By.XPATH, './td[4]').text)
print(results)
driver.quit()
df = pd.DataFrame(results)
df.to_csv('table.csv', index=False)
print(df)
