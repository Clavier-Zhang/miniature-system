from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pickle

bad_key_words = [
    'writer',
    'desk',
    'service',
    'marketing',
    'support',
    'test',
    'tester',
    'writer',
    'quality',
    'embedded',
    'investment',
    'physics',
    'hardware',
    'sales',
    'design',
    'manager',
    'qa',
    'business',
    'risk',
    'testing'
]
def contains_word(s, w):
    return (' ' + w + ' ') in (' ' + s + ' ')

def contains_bad_key_words(s, bad_words):
    result = False
    for bard_word in bad_words:
        if contains_word(s, bard_word):
            result = True
    return result

class WorksDriver:

    driver = None

    wait = None

    def __init__(self, _username, _password):
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 5)
        self.driver.get('https://waterlooworks.uwaterloo.ca/home.htm')
        self.login(_username, _password)
        self.go_to_hire_page()
        self.loop()
        self.driver.close()


    def login(self, _username, _password):
        student_login_button = self.driver.find_element_by_link_text('Students/Alumni/Staff')
        student_login_button.click()
        username = self.driver.find_element_by_id("username")
        password = self.driver.find_element_by_id("password")
        submit = self.driver.find_element_by_name('submit')
        username.send_keys(_username)
        password.send_keys(_password)
        submit.click()
        time.sleep(2)

    def go_to_hire_page(self):
        hire_waterloo_coop_button = self.driver.find_element_by_link_text("Hire Waterloo Co-op")
        hire_waterloo_coop_button.click()
        for_my_program_button = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'For My Program')))
        for_my_program_button.click()

    def loop(self):
        page_num = self.count_page_num()
        organization_set = set()
        trash = []
        for i in range(0, page_num):
            posting_table = self.driver.find_element_by_id('postingsTable')
            postings = posting_table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
            for posting in postings:
                fields = posting.find_elements_by_tag_name('td')
                id = fields[2].text
                title = fields[3].text.lower()
                organization = fields[4].text
                openings = fields[6].text
                city = fields[8].text
                level = fields[9].text
                applications = fields[10].text

                discard_button = WebDriverWait(fields[12], 5).until(EC.element_to_be_clickable((By.TAG_NAME, "a")))
                # print(id+' '+title+' '+organization+' '+ openings+' '+city+' '+level+' '+applications)
                organization_set.add(organization)

                if contains_bad_key_words(title, bad_key_words):
                    discard_button.click()
                    print('')
                    print('delete ' + title)
                    print('')
                    trash.append(title)
                    trash.append(id)

            self.click_next_page()



    # the following methods are valid only when it's under hire page
    def click_next_page(self):
        next_page_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, "»")))
        next_page_button.click()
        time.sleep(3)

    def count_page_num(self):
        pagination_element = self.driver.find_element_by_class_name('pagination')
        ul_element = pagination_element.find_element_by_tag_name("ul")
        li_elements = ul_element.find_elements_by_tag_name("li")
        page_num = len(li_elements)-4
        return page_num

driver = WorksDriver('', '')

