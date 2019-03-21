import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
from bs4 import BeautifulSoup
import re

import pandas as pd

class WebConnect():
	def __init__(self, url):
		self.driver = self.connect_driver()
		self.driver.get(url)
		print("Connected")

	def connect_driver(self):
		# driver = webdriver.Firefox() # Uses geckodriver win64

		# working_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)).replace('\\','/'))
		# working_dir = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
		# gecko = os.path.normpath(working_dir + '/drivers/geckodriver')
		# binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
		# driver = webdriver.Firefox(firefox_binary=binary, executable_path=gecko+'.exe') # uses geckodriver win32

		#To connect using custom profile
		# profile = webdriver.FirefoxProfile(os.path.expanduser("path/to/firefox/Mozilla/Firefox/Profiles/52wbvzqb.default"))
		profile = webdriver.FirefoxProfile()
		profile.set_preference('dom.webnotifications.enabled', False)
		profile.set_preference('browser.link.open_newwindow', 	1)
		profile.set_preference('browser.link.open_newwindow.restriction', 0)
		profile.set_preference('browser.link.open_newwindow.override.external', -1)
		driver = webdriver.Firefox(firefox_profile=profile) 
		return driver
		

	def load_element(self, target, by, kind):
		elem = None
		i=0
		delay = 5 if kind=="new" else 2
		while((elem is None) and (i<delay)):
			try:
				if by=="xpath":
					elem = self.driver.find_element_by_xpath(target)
				elif by=="id":
					elem = self.driver.find_element_by_id(target)
				elif by=="link_text":
					elem = self.driver.find_element_by_link_text(target)
				elif by=="name":
					elem = self.driver.find_element_by_name(target)
			except:
				time.sleep(1)
				i +=1
		return(elem)

	def load_elements(self, target, by, kind):
		elem = None
		i=0
		delay = 5 if kind=="new" else 2
		while((elem is None) and (i<delay)):
			try:
				if by=="xpath":
					elem = self.driver.find_elements_by_xpath(target)
				elif by=="id":
					elem = self.driver.find_elements_by_id(target)
				elif by=="link_text":
					elem = self.driver.find_elements_by_link_text(target)
				elif by=="name":
					elem = self.driver.find_elements_by_name(target)
			except:
				time.sleep(1)
				i +=1
		return(elem)


	def login(self, username, password, id_u, id_p, id_sub):
		elem_login = self.driver.find_element_by_id(id_u)
		elem_pw = self.driver.find_element_by_id(id_p)
		elem_submit = self.driver.find_element_by_id(id_sub)

		elem_login.clear()
		elem_pw.clear()

		elem_login.send_keys(username)
		elem_pw.send_keys(password)
		elem_submit.click()
		print("logged in")

	
	def search(self, term, id_search):
		elem_search = self.load_by_id(id_search)
		elem_search.clear()
		elem_search.send_keys(term)
		elem_search.send_keys(Keys.ENTER)

	
	def click_target(self, target, by, kind):
		elem = self.load_element(target, by, kind)
		if elem is not None:
			try:
				elem.click()
				return True
			except:
				return False
			
		else:
			return False


	def get_target_html(self, target=None, by='', kind='', loaded_element=None):
		if loaded_element is None:
			elem = self.load_element(target, by, kind)
		else:
			elem = loaded_element
		if elem is not None:
			return elem.get_attribute("innerHTML")
		else:
			return 0


	def get_target_text(self, target, by, kind):
		elem = self.load_element(target, by, kind)
		if elem is not None:
			return elem.get_attribute("innerHTML").strip().lstrip().replace("\n", " ")
		else:
			return 0


	def write_to_div(self, message, target, by, kind):
		elem = self.load_element(target, by, kind)
		if elem is not None:
			action = webdriver.ActionChains(self.driver)
			action.move_to_element_with_offset(elem, 10, 3)
			action.click()
			action.send_keys(message)
			action.send_keys(Keys.ENTER)
			action.perform()
			return True
		else:
			return False


	def click_back(self):
		self.driver.execute_script("window.history.go(-1)")

	
	def scroll_page_down(self):
		webdriver.ActionChains(self.driver).send_keys(Keys.PAGE_DOWN).perform()

	
	def scroll_page_up(self):
		webdriver.ActionChains(self.driver).send_keys(Keys.PAGE_UP).perform()


	def scroll_to_bottom(self):
		self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


	def scroll_up(self, Y):
		script = "window.scrollTo(0,document.body.scrollHeight-" + str(Y) + " )"
		self.driver.execute_script(script) 

		
	def write_to_csv(self, dataframe, f_name):
		dataframe.to_csv(f_name, sep=',', index=False)


	def close_connection(self):
		try:
			self.driver.close()
			return True
		except:
			return False


	def goto_url(self, url):
		self.driver.get(url)


	def switch_tab(self, tab_index):
		self.driver.switch_to.window(self.driver.window_handles[tab_index])


	def cancel_notification_popup(self):
		webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()