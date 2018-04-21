from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.conf import settings
import platform


class ProductPage(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'product.html', context=None)

    def post(self, request, **kwargs):
        if request.POST['action'] == "Continue":
            url = request.POST.get("sendURL")
            productData = GetProductData(url)
            if productData is None:
                redirect('HomePage')
            else:
                return render(request, 'productDescription.html', context=productData)
        else:
            return redirect('LandingPage')


class PaymentsPage(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'billDetails.html', context=None)


def GetProductData(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    if platform.system() == "Darwin":
        browser = webdriver.Chrome(settings.BASE_DIR + "/chromedriver", chrome_options=chrome_options)
    elif platform.system() == "Windows":
        browser = webdriver.Chrome(settings.BASE_DIR + "/chromedriver.exe", chrome_options=chrome_options)
    else:
        browser = webdriver.Chrome(settings.BASE_DIR + "/chromedriver_linux", chrome_options=chrome_options)

    browser.get(url)

    productTitle = browser.find_element_by_id('productTitle').text
    print(productTitle)

    productCost = browser.find_element_by_id('priceblock_ourprice').text
    print(productCost.strip())

    availability = browser.find_element_by_id('availability').text
    print(availability.strip())

    browser.quit()

    productData = {'productTitle': productTitle, 'productCost': productCost, 'availability': availability}

    return productData
