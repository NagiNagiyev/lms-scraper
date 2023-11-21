from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

def scrape_data(username:str, password:str, semester:str):
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    robot = webdriver.Firefox(executable_path='./geckodriver', options=firefox_options)

    # Link of the website for scraping 
    link = "http://lms.adnsu.az/adnsuEducation/login.jsp"
    robot.get(link)
    wait = WebDriverWait(robot, 10)

    # This code find username and password fields to write user's username and password then click enter for logging in account
    username_field = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    username_field.send_keys(username)
    password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    password_field.send_keys(password + Keys.ENTER)

    # Finds "Sistemlər" and click it 
    sistemler = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="header"]/div/div[1]/ul/li/a/span')))
    sistemler.click()

    # Finds "Tədris prosesi" and click it 
    tedris_prosesi = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="header"]/div/div[1]/ul/li/ul/div/div[2]/a/small')))
    tedris_prosesi.click()

    # Finds "Fənn üzrə qruplar" and click it
    fenn_uzre_qruplar = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, 'Fənn üzrə qruplar')))
    fenn_uzre_qruplar.click()

    # Click an empty place in the window to close pop-up
    script = "document.getElementById('accordionDiv').click();"
    robot.execute_script(script)

    # Click dropdown button and select year 
    dropdown_year = wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@data-id="subject_edu_year"]')))
    dropdown_year.click()
    year = wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="operationDiv"]/div[2]/div/div/div/div[1]/div/div/ul/li[14]/a')))
    year.click()

    # Click dropdown button and select semester according your choice
    dropdown_semester = wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@data-id="subject_semester"]')))
    dropdown_semester.click()
    if semester == "Spring":
        semester = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="operationDiv"]/div[2]/div/div/div/div[2]/div/div/ul/li[2]')))
        semester.click()
    elif semester == "Autumn":
        semester = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="operationDiv"]/div[2]/div/div/div/div[2]/div/div/ul/li[1]')))
        semester.click()

    # Finds how many subjects are there and create a for loop for each subject
    number_of_subjects = len(wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'state-link'))))

    data = {}
    # For loop to print data of each subject 
    for i in range(0, number_of_subjects):

        # Finds subject by its index and click it 
        subject = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'state-link')))[i]
        subject.click()

        # Finds subject's name to show it in the application as a label
        subject_name = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/h1')))

        # Finds "Elektron jurnal" and click it. Finds "Yekun jurnal" and click it. Finds "Göstər" and click it. To get table 
        # where our data is located
        elektron_jurnal = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, 'Elektron jurnal')))
        elektron_jurnal.click()
        yekun_jurnal = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, 'Yekun jurnal')))
        yekun_jurnal.click() 
        goster = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, 'Göstər')))
        goster.click()

        # Finds all keys in the table
        keys_table = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="resultJournal"]/thead/tr')))
        keys = keys_table.find_elements(By.TAG_NAME, 'th')

        # Finds all values in the table
        values_table = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="resultJournal"]/tbody')))
        values = values_table.find_elements(By.TAG_NAME, 'td')

        # 1. Print all key and value pairs
        # 2. Add label called info to labels list 
        # 3. Change the position of next label for a look from left to right as in program
        
        subject_data = {}
        for key, value in zip(keys[2:], values[2:]):
            subject_data[key.text] = value.text

        data[subject_name.text] = subject_data

        # Make program go back where all subjects are located
        fennler_siyahisi = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, 'Fənnlər siyahısı')))
        fennler_siyahisi.click()
    print(data)
    return data
scrape_data('nagi.nagiyev', 'Nagi2003', 'Autumn')