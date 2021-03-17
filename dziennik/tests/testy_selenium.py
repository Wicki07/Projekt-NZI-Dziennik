from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse , resolve
from django.test import TestCase , Client
from dziennik.models import User,UserManager
from dziennik.forms import RegisterForm
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import re

# Ważne!!!!!!!!!!!!!!!!!!!!!
# każdy test musi zaczynać się od słowa kluczowego 'test' inaczej się wysypie :)
# komenda na odpalenie wszystkich testów py manage.py test
# komenda na odpalenie konkretnego testu np. py .\manage.py test dziennik.tests.testy_selenium.TestProject.test_login
# yyyyyyyyyyyYYYYYYYYYYYYYYYYYYYYYYyyyyyyyyyyyyyyyyyyyyyyyyyyyyYYYYYYYYYYYY


class TestProject(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.wait = WebDriverWait(self.browser, 10)

    """ Testy Logowania Uzytkownik"""
    """ T1 Logowanie poprawne"""
    def test_T1(self):
        self.browser.get('http://localhost:8000/login')
        login = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/input')
        password = self.browser.find_element_by_name('password')
        button = self.browser.find_element_by_tag_name('button')      
        password.send_keys('Marik1234')
        login.send_keys('dziennik@mail.com')
        button.submit()
        self.wait.until(EC.url_to_be('http://localhost:8000/'))
        self.browser.close()

    """ T2 Logowanie niepoprawne - brak hasła"""
    def test_T2(self):
        self.browser.get('http://localhost:8000/login')
        login = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/input')
        password = self.browser.find_element_by_name('password')
        button = self.browser.find_element_by_tag_name('button')    
        password.send_keys('')
        login.send_keys('dziennik@mail.com')
        button.submit()
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[4]/p"), "hasło się nie zgadzją."))
        self.browser.close()

    """ T3 Logowanie niepoprawne - błędne hasło"""
    def test_T3(self):
        self.browser.get('http://localhost:8000/login')
        login = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/input')
        password = self.browser.find_element_by_name('password')
        button = self.browser.find_element_by_tag_name('button')      
        password.send_keys('blednehaslo')
        login.send_keys('dziennik@mail.com')
        button.submit()
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[4]/p"), "hasło się nie zgadzją."))
        self.browser.close()

    """ Testy Rejestracja Uzytkownik"""
    """ T4 Rejestracja użytkownika poprawne"""
    def test_T4(self):
        self.browser.get('http://localhost:8000/signup/person')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        surname = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/p/input')     
        name.send_keys('Mateusz')
        surname.send_keys('Wicki')
        email.send_keys('mateuszwicki1@mail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik2')
        number.send_keys('123456789')
        self.browser.find_element_by_tag_name('button').submit()   
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'popup')))
        self.browser.close()

    """ T5 Rejestracja użytkownika niepoprawne - niezgadzające się hasła"""
    def test_T5(self):
        self.browser.get('http://localhost:8000/signup/person')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        surname = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/button')      
        name.send_keys('Mateusz')
        surname.send_keys('Wicki')
        email.send_keys('mateuszwicki1@mail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik2')
        number.send_keys('123456789')
        self.browser.execute_script("validate()")
        time.sleep(2)
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[6]/span/p"), "Podane hasła się nie zgdzają"))
        self.browser.close()

    """ T6 Rejestracja użytkownika niepoprawne - brak podania hasła"""
    def test_T6(self):
        self.browser.get('http://localhost:8000/signup/person')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        surname = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/button')      
        name.send_keys('Mateusz')
        surname.send_keys('Wicki')
        email.send_keys('mateuszwicki1@mail.com')
        password1.send_keys('')
        password2.send_keys('')
        number.send_keys('123456789')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[5]/span/p"), "Nie podano hasła"))
        self.browser.close()  

    """ T7 Rejestracja instytucji poprawne"""
    def test_T7(self):
        self.browser.get('http://localhost:8000/signup/institution')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        category = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/select')
        profil = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[9]/button')   
        name.send_keys('Akademia Pływania')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('')
        category.click()
        all_options = category.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "Klub sportowy":
                option.click()
        profil.send_keys('Pływanie')
        number.send_keys('123456789')
        self.browser.find_element_by_tag_name('button').submit()   
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'popup')))
        self.browser.close()   

    """ T8 Rejestracja instytucji niepoprawne - brak podania nazwy instytucji"""
    def test_T8(self):
        self.browser.get('http://localhost:8000/signup/institution')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        category = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/select')
        profil = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[9]/button')   
        name.send_keys('')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('')
        category.click()
        all_options = category.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "Klub sportowy":
                option.click()
        profil.send_keys('Pływanie')
        number.send_keys('123456789')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[2]/span/p"), "Nie podano nazwy"))
        self.browser.close()  

    """ T9 Rejestracja instytucji niepoprawne - błędnie podane hasła"""
    def test_T9(self):
        self.browser.get('http://localhost:8000/signup/institution')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        category = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/select')
        profil = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[9]/button')   
        name.send_keys('Akademia Pływania')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik2')
        number.send_keys('')
        category.click()
        all_options = category.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "Klub sportowy":
                option.click()
        profil.send_keys('Pływanie')
        number.send_keys('123456789')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[5]/span/p"), "Podane hasła się nie zgdzają"))
        self.browser.close()  

    """ T10 Podgląd planu zajęć pracownika poprawne"""
    def test_T10(self):
        self.browser.get('http://localhost:8000/login')
        login = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/input')
        password = self.browser.find_element_by_name('password')
        button = self.browser.find_element_by_tag_name('button')    
        password.send_keys('IAL0O1DQ')
        login.send_keys('pracownik@mail.com')
        time.sleep(2)
        button.submit()
        time.sleep(2)
        # EC.presence_of_element_located muszą w sodku być nawiasy bo inaczej widzi jako 3 argumenty
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'activity')))
        self.browser.close()

    """ T11 Ustawienie przypomnień pracownika poprawne"""
    def test_T11(self):
        self.browser.get('http://localhost:8000/login')
        login = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/input')
        password = self.browser.find_element_by_name('password')
        button = self.browser.find_element_by_tag_name('button')  
        password.send_keys('IAL0O1DQ')
        login.send_keys('pracownik@mail.com')
        time.sleep(1)
        button.submit()
        time.sleep(1)
        #szukamy activity 
        activity = self.browser.find_element_by_xpath('/html/body/main/div[2]/div/div/div/span[8]')
        #klikamy w activity
        activity.click()  
        time.sleep(1)
        #tutaj szukamy ikonki z włączeniem powiadomień
        set_assignment_button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/div[1]/form/button[1]')
        set_assignment_button.click()
        time.sleep(1)
        #jesli znajdzie message o tym ze poprawnie ustawiono przypomnienie i znajdzie ta wiadomość to przejdzie
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH,'/html/body/div[1]/div/div/div/font'),'Włączono powiadomienie o zajęciach'))
        self.browser.close()

    """T12 Interakcja związana z aktywnością pracownika poprawne"""
    def test_T12(self):
        self.browser.get('http://localhost:8000/login')
        login = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/input')
        password = self.browser.find_element_by_name('password')
        button = self.browser.find_element_by_tag_name('button')  
        password.send_keys('IAL0O1DQ')
        login.send_keys('pracownik@mail.com')
        time.sleep(1)
        button.submit()
        time.sleep(1)
        # szukamy activity 
        activity = self.browser.find_element_by_xpath('/html/body/main/div[2]/div/div/div/span[8]')
        # klikamy w activity
        activity.click()
        time.sleep(1)
        # tutaj szukamy ikonki z wlaczeniem pwoiadomien
        set_assignment_button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/div[1]/form/button[2]')
        set_assignment_button.click()
        time.sleep(1)
        # najpierw nalezy kliknac na textarea zeby sfokusowac element 
        self.browser.find_element_by_xpath('/html/body/div/div/div/div/div[2]/form/textarea').click()
        # teraz przekazujemy wiadomosc
        self.browser.find_element_by_xpath('/html/body/div/div/div/div/div[2]/form/textarea').send_keys('Testowa wiadomość')
        # klikamy 1 potwierdzenie
        self.browser.find_element_by_xpath('/html/body/div/div/div/div/div[2]/form/button[2]').click()
        # klikamy 2 potwierdzenie
        self.browser.find_element_by_xpath('/html/body/div/div/div/div/div[3]/form/button[2]').click()
        time.sleep(1)
        # Teraz szukamy elementu z tekstem
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH,'/html/body/div[1]/div/div/div/font'),'Wysłano powiadomienie o odwołaniu zajęć'))
        self.browser.close()

    """ T13 Rejestracja użytkownika niepoprawne - brak imienia"""
    def test_T13(self):
        self.browser.get('http://localhost:8000/signup/person')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        surname = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/button')      
        name.send_keys('')
        surname.send_keys('Wicki')
        email.send_keys('mateuszwicki1@mail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('123456789')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[2]/span/p"), "Nie podano imienia"))
        self.browser.close()  

    """ T14 Rejestracja użytkownika niepoprawne - błędne imię"""
    def test_T14(self):
        self.browser.get('http://localhost:8000/signup/person')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        surname = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/button')      
        name.send_keys('Mateusz1')
        surname.send_keys('Wicki')
        email.send_keys('mateuszwicki1@mail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('123456789')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[2]/span/p"), "Podano niewłaściwe imie"))
        self.browser.close()  

    """ T15 Rejestracja użytkownika niepoprawne - brak nazwiska"""
    def test_T15(self):
        self.browser.get('http://localhost:8000/signup/person')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        surname = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/button')      
        name.send_keys('Mateusz')
        surname.send_keys('')
        email.send_keys('mateuszwicki1@mail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('123456789')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[3]/span/p"), "Nie podano nazwiska"))
        self.browser.close() 

    """ T16 Rejestracja użytkownika niepoprawne - błędne nazwisko"""
    def test_T16(self):
        self.browser.get('http://localhost:8000/signup/person')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        surname = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/button')      
        name.send_keys('Mateusz')
        surname.send_keys('Wicki1')
        email.send_keys('mateuszwicki1@mail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('123456789')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[3]/span/p"), "Podano niewłaściwe nazwisko"))
        self.browser.close() 

    """ T17 Rejestracja użytkownika niepoprawne - brak maila"""
    def test_T17(self):
        self.browser.get('http://localhost:8000/signup/person')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        surname = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/button')      
        name.send_keys('Mateusz')
        surname.send_keys('Wicki')
        email.send_keys('')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('123456789')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[4]/span/p"), "Nie podano maila"))
        self.browser.close() 

    """ T18 Rejestracja użytkownika niepoprawne - brak maila"""
    def test_T18(self):
        self.browser.get('http://localhost:8000/signup/person')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        surname = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/button')      
        name.send_keys('Mateusz')
        surname.send_keys('Wicki')
        email.send_keys('mateuszwicki1gmail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('123456789')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[4]/span/p"), "Podany mail nie jest prawidłowy"))
        self.browser.close() 

    """ T19 Rejestracja użytkownika niepoprawne - błędny mail bez ."""
    def test_T19(self):
        self.browser.get('http://localhost:8000/signup/person')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        surname = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/button')      
        name.send_keys('Mateusz')
        surname.send_keys('Wicki')
        email.send_keys('mateuszwicki1@gmailcom')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('123456789')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[4]/span/p"), "Podany mail jest nieprawidłowy"))
        self.browser.close() 

    """ T20 Rejestracja użytkownika niepoprawne - błędny mail bez “@….”"""
    def test_T20(self):
        self.browser.get('http://localhost:8000/signup/person')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        surname = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/button')      
        name.send_keys('Mateusz')
        surname.send_keys('Wicki')
        email.send_keys('mateuszwicki1')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('123456789')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[4]/span/p"), "Podany mail nie jest prawidłowy"))
        self.browser.close() 

    """ T21 Rejestracja użytkownika niepoprawne - za krótkie hasło"""
    def test_T21(self):
        self.browser.get('http://localhost:8000/signup/person')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        surname = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/button')      
        name.send_keys('Mateusz')
        surname.send_keys('Wicki')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('Dzie1')
        password2.send_keys('Dzie1')
        number.send_keys('123456789')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[5]/span/p"), "Podane hasło jest nieprawidłowe"))
        self.browser.close() 

    """ T22 Rejestracja użytkownika niepoprawne - hasło bez cyfry"""
    def test_T22(self):
        self.browser.get('http://localhost:8000/signup/person')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        surname = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/button')      
        name.send_keys('Mateusz')
        surname.send_keys('Wicki')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('Dziennik')
        password2.send_keys('Dziennik')
        number.send_keys('123456789')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[5]/span/p"), "Podane hasło jest nieprawidłowe"))
        self.browser.close() 

    """ T23 Rejestracja użytkownika niepoprawne - hasło bez dużej litery"""
    def test_T23(self):
        self.browser.get('http://localhost:8000/signup/person')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        surname = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/button')      
        name.send_keys('Mateusz')
        surname.send_keys('Wicki')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('dziennik1')
        password2.send_keys('dziennik1')
        number.send_keys('123456789')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[5]/span/p"), "Podane hasło jest nieprawidłowe"))
        self.browser.close() 

    """ T24 Rejestracja użytkownika niepoprawne - błędny numer telefonu"""
    def test_T24(self):
        self.browser.get('http://localhost:8000/signup/person')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        surname = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/button')      
        name.send_keys('Mateusz')
        surname.send_keys('Wicki')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('123456abc')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[7]/span/p"), "Podany nr telefonu nie jest prawidłowy"))
        self.browser.close() 

    """ T25 Rejestracja użytkownika niepoprawne - za krótki numer telefonu"""
    def test_T25(self):
        self.browser.get('http://localhost:8000/signup/person')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        surname = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/button')      
        name.send_keys('Mateusz')
        surname.send_keys('Wicki')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('12345678')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[7]/span/p"), "Podany nr telefonu nie jest prawidłowy"))
        self.browser.close() 

    """ T26 Rejestracja użytkownika niepoprawne - za długi numer telefonu"""
    def test_T26(self):
        self.browser.get('http://localhost:8000/signup/person')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        surname = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/button')      
        name.send_keys('Mateusz')
        surname.send_keys('Wicki')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('1234567890123456')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[7]/span/p"), "Podany nr telefonu nie jest prawidłowy"))
        self.browser.close() 

    """ T27 Rejestracja użytkownika poprawne - nazwisko dwuczłonowe"""
    def test_T27(self):
        self.browser.get('http://localhost:8000/signup/person')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        surname = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/button')      
        name.send_keys('Mateusz')
        surname.send_keys('Wicki-Morawski')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('123456789')
        self.browser.find_element_by_tag_name('button').submit()   
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'popup')))
        self.browser.close() 

    """ T28 Rejestracja użytkownika poprawne - bez podania numeru telefonu"""
    def test_T28(self):
        self.browser.get('http://localhost:8000/signup/person')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        surname = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/button')      
        name.send_keys('Mateusz')
        surname.send_keys('Wicki')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('')
        self.browser.find_element_by_tag_name('button').submit()   
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'popup')))
        self.browser.close() 

    """ T29 Rejestracja instytucji niepoprawne - błędne podanie nazwy"""
    def test_T29(self):
        self.browser.get('http://localhost:8000/signup/institution')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        category = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/select')
        profil = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[9]/button')   
        name.send_keys('A')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('123456789')
        category.click()
        all_options = category.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "Klub sportowy":
                option.click()
        profil.send_keys('Pływanie')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[2]/span/p"), "Podano niewłaściwą nazwę"))
        self.browser.close() 

    """ T30 Rejestracja instytucji niepoprawne - brak maila"""
    def test_T30(self):
        self.browser.get('http://localhost:8000/signup/institution')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        category = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/select')
        profil = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[9]/button')   
        name.send_keys('Akademia Pływania')
        email.send_keys('')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('123456789')
        category.click()
        all_options = category.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "Klub sportowy":
                option.click()
        profil.send_keys('Pływanie')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[3]/span/p"), "Nie podano maila"))
        self.browser.close() 

    """ T31 Rejestracja instytucji niepoprawne - błędny mail bez znaku “@”"""
    def test_T31(self):
        self.browser.get('http://localhost:8000/signup/institution')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        category = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/select')
        profil = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[9]/button')   
        name.send_keys('Akademia Pływania')
        email.send_keys('mateuszwicki1gmail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('123456789')
        category.click()
        all_options = category.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "Klub sportowy":
                option.click()
        profil.send_keys('Pływanie')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[3]/span/p"), "Podany mail nie jest prawidłowy"))
        self.browser.close() 

    """ T32 Rejestracja instytucji niepoprawne - błędny mail bez “.”"""
    def test_T32(self):
        self.browser.get('http://localhost:8000/signup/institution')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        category = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/select')
        profil = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[9]/button')   
        name.send_keys('Akademia Pływania')
        email.send_keys('mateuszwicki1@gmailcom')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('123456789')
        category.click()
        all_options = category.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "Klub sportowy":
                option.click()
        profil.send_keys('Pływanie')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[3]/span/p"), "Podany mail jest nieprawidłowy"))
        self.browser.close() 
    
    """ T33 Rejestracja instytucji niepoprawne -błędny mail bez “@….”"""
    def test_T33(self):
        self.browser.get('http://localhost:8000/signup/institution')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        category = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/select')
        profil = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[9]/button')   
        name.send_keys('Akademia Pływania')
        email.send_keys('mateuszwicki1')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('123456789')
        category.click()
        all_options = category.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "Klub sportowy":
                option.click()
        profil.send_keys('Pływanie')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[3]/span/p"), "Podany mail nie jest prawidłowy"))
        self.browser.close() 
              
    """ T34 Rejestracja instytucji niepoprawne - brak podania hasła"""
    def test_T34(self):
        self.browser.get('http://localhost:8000/signup/institution')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        category = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/select')
        profil = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[9]/button')   
        name.send_keys('Akademia Pływania')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('')
        password2.send_keys('Dziennik1')
        number.send_keys('123456789')
        category.click()
        all_options = category.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "Klub sportowy":
                option.click()
        profil.send_keys('Pływanie')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[4]/span/p"), "Nie podano hasła"))
        self.browser.close() 
                     
    """ T35 Rejestracja instytucji niepoprawne - brak podania potwierdzenia hasła"""
    def test_T35(self):
        self.browser.get('http://localhost:8000/signup/institution')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        category = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/select')
        profil = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[9]/button')   
        name.send_keys('Akademia Pływania')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('')
        number.send_keys('123456789')
        category.click()
        all_options = category.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "Klub sportowy":
                option.click()
        profil.send_keys('Pływanie')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[5]/span/p"), "Nie podano hasła ponownie"))
        self.browser.close()  
                             
    """ T36 Rejestracja instytucji niepoprawne - podanie za krótkiego hasła"""
    def test_T36(self):
        self.browser.get('http://localhost:8000/signup/institution')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        category = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/select')
        profil = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[9]/button')   
        name.send_keys('Akademia Pływania')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('Dzien1')
        password2.send_keys('Dzien1')
        number.send_keys('123456789')
        category.click()
        all_options = category.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "Klub sportowy":
                option.click()
        profil.send_keys('Pływanie')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[5]/span/p"), "Podane hasło jest nieprawidłowe"))
        self.browser.close()  
                                     
    """ T37 Rejestracja instytucji niepoprawne - podanie błędnego hasła bez cyfry"""
    def test_T37(self):
        self.browser.get('http://localhost:8000/signup/institution')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        category = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/select')
        profil = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[9]/button')   
        name.send_keys('Akademia Pływania')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('Dziennik')
        password2.send_keys('Dziennik')
        number.send_keys('123456789')
        category.click()
        all_options = category.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "Klub sportowy":
                option.click()
        profil.send_keys('Pływanie')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[4]/span/p"), "Podane hasło jest nieprawidłowe"))
        self.browser.close()  
                                      
    """ T38 Rejestracja instytucji niepoprawne - podanie błędnego hasła bez dużej litery"""
    def test_T38(self):
        self.browser.get('http://localhost:8000/signup/institution')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        category = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/select')
        profil = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[9]/button')   
        name.send_keys('Akademia Pływania')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('dziennik1')
        password2.send_keys('dziennik1')
        number.send_keys('123456789')
        category.click()
        all_options = category.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "Klub sportowy":
                option.click()
        profil.send_keys('Pływanie')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[4]/span/p"), "Podane hasło jest nieprawidłowe"))
        self.browser.close()         
                                       
    """ T39 Rejestracja instytucji niepoprawne - podanie błędnego numeru telefonu"""
    def test_T39(self):
        self.browser.get('http://localhost:8000/signup/institution')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        category = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/select')
        profil = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[9]/button')   
        name.send_keys('Akademia Pływania')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('123456abc')
        category.click()
        all_options = category.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "Klub sportowy":
                option.click()
        profil.send_keys('Pływanie')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[6]/span/p"), "Podany nr telefonu nie jest prawidłowy"))
        self.browser.close()         
                                        
    """ T40 Rejestracja instytucji niepoprawne - podanie za krótkiego numeru telefonu"""
    def test_T40(self):
        self.browser.get('http://localhost:8000/signup/institution')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        category = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/select')
        profil = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[9]/button')   
        name.send_keys('Akademia Pływania')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('12345678')
        category.click()
        all_options = category.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "Klub sportowy":
                option.click()
        profil.send_keys('Pływanie')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[6]/span/p"), "Podany nr telefonu nie jest prawidłowy"))
        self.browser.close()    
                                         
    """ T41 Rejestracja instytucji niepoprawne - podanie za długiego numeru telefonu"""
    def test_T41(self):
        self.browser.get('http://localhost:8000/signup/institution')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        category = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/select')
        profil = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[9]/button')   
        name.send_keys('Akademia Pływania')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('1234567890123456')
        category.click()
        all_options = category.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "Klub sportowy":
                option.click()
        profil.send_keys('Pływanie')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[6]/span/p"), "Podany nr telefonu nie jest prawidłowy"))
        self.browser.close()    

    """ T42 Rejestracja instytucji poprawne - bez podania numeru telefonu"""
    def test_T42(self):
        self.browser.get('http://localhost:8000/signup/institution')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        category = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/select')
        profil = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[9]/button')   
        name.send_keys('Akademia Pływania')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('')
        category.click()
        all_options = category.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "Klub sportowy":
                option.click()
        profil.send_keys('Pływanie')
        self.browser.find_element_by_tag_name('button').submit()   
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'popup')))
        self.browser.close()                   

    """ T43 Rejestracja instytucji niepoprawne - nie wybranie kategorii"""
    def test_T43(self):
        self.browser.get('http://localhost:8000/signup/institution')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        category = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/select')
        profil = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[9]/button')   
        name.send_keys('Akademia Pływania')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('132456789')
        profil.send_keys('Pływanie')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[7]/span/p"), "Nie wybrano kategorii"))
        self.browser.close()    

    """ T44 Rejestracja instytucji niepoprawne - nie wybranie kategorii"""
    def test_T44(self):
        self.browser.get('http://localhost:8000/signup/institution')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        category = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/select')
        profil = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[9]/button')   
        name.send_keys('Akademia Pływania')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('132456789')
        category.click()
        all_options = category.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "Klub sportowy":
                option.click()
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[8]/span/p"), "Nie podano profilu np. klub piłkarski, szkoła j. angielskiego"))
        self.browser.close()   

    """ T45 Rejestracja instytucji niepoprawne - błędne podanie specjalizacji"""
    def test_T45(self):
        self.browser.get('http://localhost:8000/signup/institution')
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/p/input')
        email = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/p/input')
        password1 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[4]/p/input')
        password2 = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[5]/p/input')
        number = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[6]/p/input')
        category = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[7]/select')
        profil = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[8]/p/input')
        button = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[9]/button')   
        name.send_keys('Akademia Pływania')
        email.send_keys('mateuszwicki1@gmail.com')
        password1.send_keys('Dziennik1')
        password2.send_keys('Dziennik1')
        number.send_keys('132456789')
        category.click()
        all_options = category.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "Klub sportowy":
                option.click()
        profil.send_keys('Pływanie1')
        self.browser.execute_script("validate()")
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[8]/span/p"), "Podany profil jest nieprawidłowy"))
        self.browser.close()  

    """ T101 Rejestracja instytucji niepoprawne - błędne podanie specjalizacji"""
    def test_T101(self):
        self.browser.get('http://localhost:8000/login')
        self.browser.maximize_window()
        login = self.browser.find_element_by_xpath('/html/body/div/div/div/div/form/div[2]/input')
        password = self.browser.find_element_by_name('password')
        button = self.browser.find_element_by_tag_name('button')      
        password.send_keys('Dziennik1')
        login.send_keys('mateuszwicki1@gmail.com')
        button.submit()
        time.sleep(1)
        settings = self.browser.find_element_by_xpath('/html/body/nav/div/ul/li[3]')
        settings.click()
        time.sleep(1)
        change = self.browser.find_element_by_xpath('/html/body/main/div[2]/div/div/ul/a[1]')
        change.click()
        email = self.browser.find_element_by_xpath('/html/body/main/div/div/div/div/form/div[1]/p/input')
        email.click()
        time.sleep(1)
        email.send_keys('mateuszwicki1+zmiana@gmail.com')
        time.sleep(1)
        self.browser.execute_script("validate()")
        self.browser.find_element_by_xpath('/html/body/main/div/div/div/div/form/div[2]/button').submit()
        time.sleep(1)
        #self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/div/div/form/div[8]/span/p"), "Podany profil jest nieprawidłowy"))
        self.browser.close()  