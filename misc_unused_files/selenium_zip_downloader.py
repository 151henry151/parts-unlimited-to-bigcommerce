#!/usr/bin/python
# -*- coding: utf-8 -*-
#    this script opens partsnetweb.com, logs in,
#    clicks parts, clicks brand downloads,
#    and then downloads every brand in the list
#    to the default download folder on your machine
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

mypsswd = "obscured"
mydlrid = "obscured"
myusrid = "HALH"

class Grabberauto(unittest.TestCase):
    def setUp(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip")
        profile.set_preference("browser.download.manager.showWhenStarting", False)
	#suppresses the save as or open file dialog box
        self.driver = webdriver.Firefox(profile)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.partsnetweb.com/index.jsp"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_grabberauto(self):
        driver = self.driver
        driver.get(self.base_url + "/index.jsp")
        driver.find_element_by_id("dealer_id").clear()
        driver.find_element_by_id("dealer_id").send_keys(mydlrid)
        driver.find_element_by_name("user_id").clear()
        driver.find_element_by_name("user_id").send_keys(myusrid)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(mypsswd)
        driver.find_element_by_css_selector("input[type=\"image\"]").click()
        driver.find_element_by_id("mi_parts").click()
        driver.find_element_by_link_text("Brand Download").click()
        driver.find_element_by_name("br").click()
        driver.find_element_by_xpath("(//input[@name='exportType'])[2]").click()

        
        for i in range(1,567):
            string1 = "(//input[@name='br']) [%s]" % i
            driver.find_element_by_xpath(string1).click()
            driver.find_element_by_id("downloadBtn").click()

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
