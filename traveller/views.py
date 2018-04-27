from django.shortcuts import render
from django.views.generic import TemplateView
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.conf import settings
import platform

class TravellerPage(TemplateView):
    def get(self, request, **kwargs):
        PNR = ""      
        lName = ""
        print(CheckBooking(PNR, lName))
        return render(request, 'traveller.html', context=None)  #why are we checking before entering anything


class VerificationPage(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'Verification.html', context=None)

def CheckBooking(ref, lName):

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    if platform.system() == "Darwin":
        browser = webdriver.Chrome(settings.BASE_DIR + "/chromedriver", chrome_options=chrome_options)
    elif platform.system() == "Windows":
        browser = webdriver.Chrome(settings.BASE_DIR + "/chromedriver.exe", chrome_options=chrome_options)
    else:
        browser = webdriver.Chrome(settings.BASE_DIR + "/chromedriver_linux", chrome_options=chrome_options)

    browser.get("https://book.goindigo.in/Flight/Map#viewchange")

    refElement = browser.find_element_by_id("indiGoRetrieveBooking_RecordLocator")
    lNameElement = browser.find_element_by_id("indiGoRetrieveBooking_EmailAddress")

    refElement.send_keys(ref)
    lNameElement.send_keys(lName)

    submitButton = browser.find_element_by_id("submitButtonId")
    submitButton.click()

    errorElement = browser.find_elements_by_class_name("errorMsgs")
    if len(errorElement) == 0:
        return True
    else:
        return False
