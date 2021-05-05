# https://services.bgsu.edu/directorySearch/search.htm
import sys
import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# get initial list of all departments
#searchTypeDepartment
#departmentNames
# dept_list = driver.find_element_by_css_selector('#departmentNames')
# dept_list.get_attribute('value')
# Get list of departments
# depts = []
# for i in range(2,1000):
#     try:
#         depts.append(driver.find_element_by_css_selector(f'#departmentNames > option:nth-child({i})').get_property('value'))
        
#     except:
#         break
        
# department list Dr.Lee picked out
dept_list = ['Accounting/MIS', 'American Culture Studies', 'Applied Statistics/Oper Res', 'Biological Science', 'Chemistry Department', 
             'Comm. Sciences & Disorders', 'Computer Science', 'Department of Journalism & PR', 'Dept  Engineering Technologies', 
             'Dept of Communication', 'Dept of Envir. and Sustain.', 'Dept of Telecommunications', 'Economics Dept', 'Engineering', 
             'English Department', 'Ethnic Studies', 'Family & Consumer Sciences', 'Finance', 'Food & Nutrition', 'Forensic Science', 
             'Geography Department', 'Geology Department', 'Gerontology', 'History Department', 'Management', 'Marketing', 'Marketing & Communications', 
             'Math and Statistics Dep', 'Music Education', 'Music Performance Studies', 'Philosophy Department', 'Physics & Astronomy', 
             'Political Science Department', 'Popular Culture', 'Psychology Department', 'Public & Allied Health', 'School of Art', 
             'School of Cultural & Critical', 'School of Earth, Environ & Soc', 'School of HMSLS', 'School of Media and Comm', 
             'School of Teaching & Learning', 'Social Work', 'Sociology Department', 'Theatre and Film', 'VCT-Tech Education', 
             'World Languages and Cultures']

# use firefox to access web
driver= webdriver.Firefox(executable_path=r'G:\Python\geckodriver.exe') # update this executable path for your geckodriver location
driver.maximize_window()
driver.get('https://services.bgsu.edu/directorySearch/search.htm')
time.sleep(2)
driver.find_element_by_css_selector('#searchTypeDepartment').click()

# d = pd.DataFrame(depts,columns=['department'])
# d.to_csv('department_list.csv',index=False)
# get data from results table recursively
def from_table(driver,data):
    table = driver.find_element_by_css_selector('#DataTables_Table_0 > tbody:nth-child(3)')
    next_button = driver.find_element_by_css_selector('#DataTables_Table_0_next')
    for row in table.find_elements_by_xpath(".//tr"):
        row_data = [td.text for td in row.find_elements_by_xpath(".//td")]
        if len(row_data) < 2:
            continue
        if 'Professor' in row_data[2]:
            data.append(row_data)
    # returns when the string "i/j" has i == j
    if len(set(driver.find_element_by_css_selector('.pagedisplay').get_attribute('value').split('/'))) == 1:
        return
    next_button.click()
    time.sleep(2) # give it a sec for the next page to load
    from_table(driver,data)
    

data_table = []
for i in range(0,1000): # end at some i=1000, i is greater than the number of departments
    try:
        current_dept = driver.find_element_by_css_selector(f'#departmentNames > option:nth-child({i})')
        if current_dept.text in dept_list:
            print(current_dept.text)
            time.sleep(1)
            current_dept.click()
            time.sleep(1)
            driver.find_element_by_css_selector('button.btn').click()
            time.sleep(9) # sleep 12 seconds, waiting for data to come back
            from_table(driver,data_table)
            time.sleep(1)
    except:
        break
df = pd.DataFrame(data_table,columns=['name','department','title','email','phone'])

df.to_csv(r'G:\Python File Saves\Capstone Project\lookup_table.csv',index=False)
