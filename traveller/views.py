from django.shortcuts import render
from django.views.generic import TemplateView
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.conf import settings
import platform


class TravellerPage(TemplateView):
    def get(self, request, **kwargs):
        # print(CheckBooking(PNR, lName))
        return render(request, 'traveller.html', context=None)


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
        city = browser.find_element_by_css_selector("body > div.push.containerpage_main > div.pageHeight > section.main.search_fligh_main.clearfix > div.itineraryWrapper.middle_container > section > div > div.indigo_flights > div.itiFlightDetails.flights_table > table > tbody > tr > td:nth-child(5)").text
        print(city)
        return True, city
    else:
        return False, None
