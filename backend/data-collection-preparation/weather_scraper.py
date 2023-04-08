from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import ElementClickInterceptedException
import pandas as pd
import time
from csv import writer

#create csv file with relevant headers
headers = ["Location","Year","Date", "Daily Rainfall Total (mm)", "Highest  30-min Rainfall (mm)",
           "Highest  60-min Rainfall (mm)", "Highest 120-min Rainfall (mm)", "Mean Temperature (degree celsius)",
           "Maximum Temperature (degree celsius)", "Minimum Temperature (degree celsius)", "Mean Wind Speed (km/h)",
           "Max Wind Speed (km/h)"]

with open('weather_data.csv',"a", encoding='utf-8') as file:
    writer_object = writer(file)
    writer_object.writerow(headers)
    file.close()


url = 'http://www.weather.gov.sg/climate-historical-daily/'

driver = webdriver.Chrome()
driver.get(url)

all_loc = driver.find_element_by_class_name('world-region') # get all locations
all_loc = driver.find_elements_by_tag_name('span')
# print(list(map(lambda x:x.get_attribute("id"),all_loc[:5])))
all_loc = list(map(lambda x:x.get_attribute("id"),all_loc))[5:]  #first 5 elements useless so just throw


#click on all locations
for place in all_loc:
    try:
        location_button = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{place}"]')))
        location_button.click()
    except ElementClickInterceptedException:
        print(f"Trying to click on the button again for : {place}")
        driver.execute_script("arguments[0].click()", location_button)
    
    #access different year
    interested_years = (1,2,3,4) #2023[1]-2020[4]
    for year in interested_years:
        wait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="year"]'))).click() #click on year dropdown box
        wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="yearDiv"]/ul/li[{year}]/a'))).click() #click on specific year
        wait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="display"]'))).click()  #click on display
        time.sleep(1)  #give time for page to load

        #access different months
        all_months = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="monthDiv"]/ul'))) #get all months available
        all_months = all_months.find_elements_by_tag_name('li')
        all_months = list(map(lambda x:x.find_element_by_tag_name("a").get_attribute("innerHTML"),all_months)) #get list month string
        all_months = list(map(lambda x:x[:3],all_months)) #extract first 3 letters of month

        for i, month in enumerate(all_months):
            wait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="month"]'))).click() #click on month dropdown box
            wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="monthDiv"]/ul/li[{i+1}]/a'))).click() #click on specific month
            wait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="display"]'))).click()  #click on display
            time.sleep(1) #give time for page to load

            curr_month = all_months[i]
            # print(f'curr_month = {curr_month}')
            wait(driver,10).until(EC.text_to_be_present_in_element((By.XPATH,'//*[@id="temp"]/h4[1]'), curr_month)) #ensure that the table we are reading is updated
            
            #access table data
            table = wait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="temp"]/h4[2]/div/div/table'))) #access table
            table_data = pd.read_html(table.get_attribute('outerHTML'))[0] #use pandas to process html table
            table_data['Location'] = place #add new column for location
            table_data['Year'] = driver.find_element_by_xpath('//*[@id="year"]').text #add new column for year
            table_data.insert(0,'Location', table_data.pop('Location')) #rearrange location to 1st column
            table_data.insert(1,'Year', table_data.pop('Year')) #rearrange year to 2nd column
            # print(table_data)
            table_data.to_csv('weather_data.csv', mode='a', index=False, header=False, encoding="utf-8") #append to current CSV
            
driver.quit()