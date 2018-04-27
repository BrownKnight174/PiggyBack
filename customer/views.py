from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.conf import settings
import platform
from django.contrib import messages


class ProductPage(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'productDescription.html', context=None)

    def post(self, request, **kwargs):
        if request.POST['action'] == "Continue":

            url = request.POST.get("sendURL")

            productData = GetProductData(url)

            if productData is None:
                redirect('HomePage')
            else:
                cleanData = CleanData(productData)

                request.session['productCost'] = productData['productCost'][1:]
                request.session['productTitle'] = productData['productTitle']

                return render(request, 'productDescription.html', context=cleanData)
        else:
            return redirect('LandingPage')


class PaymentsPage(TemplateView):
    def get(self, request, **kwargs):
        cost = request.session.get('productCost', None)
        title = request.session.get('productTitle', None)
        if cost and title:
            context = {'productCost': cost, 'productTitle': title}
            return render(request, 'billDetails.html', context=None)
        else:
            messages.error(request, "Cannot access specified page!")
            return redirect('HomePage')


class PaymentPortalPage(TemplateView):
    def get(self, request, **kwargs):
        cost = request.session.get('productCost', None)
        title = request.session.get('productTitle', None)
        if cost and title:
            context = {'productCost': str(float(cost)*100), 'productTitle': title}
            print(context)
            return render(request, 'paymentPortal.html', context=context)
        else:
            messages.error(request, "Cannot access specified page!")
            return redirect('HomePage')


class CheckoutPage(TemplateView):
    def get(self, request, **kwargs):
        messages.error(request, "Cannot access specified page!")
        return redirect('HomePage')

    def post(self, request, **kwargs):
        return redirect('HomePage')


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

    try:
        productCost = browser.find_element_by_id('priceblock_ourprice').text
        print(productCost.strip())
        if productCost == "":
            productCost = browser.find_element_by_id('priceblock_usedprice').text
            print(productCost.strip())
    except:
        productCost = browser.find_element_by_id('priceblock_dealprice').text
        print(productCost.strip())


    availability = browser.find_element_by_id('availability').text
    print(availability.strip())

    descriptionElements = browser.find_elements_by_xpath("//*[@id='feature-bullets']/ul/li/span[@class='a-list-item']")
    description = []
    for element in descriptionElements:
        description.append(element.text)

    browser.quit()

    productData = {'productTitle': productTitle, 'productCost': productCost, 'availability': availability, 'description': description}

    return productData


def CleanData(productData):
    # Cleaning cost
    cost = productData.get("productCost", "")
    cost.strip()
    splitCost = cost.split()
    print(splitCost)
    cleanedCost = splitCost[0] + splitCost[1] + '.' + splitCost[2]
    print(cleanedCost)
    productData['productCost'] = cleanedCost

    # Cleaning product title
    title = productData.get("productTitle", "")
    title.strip()
    productData['productTitle'] = title

    # Cleaning availability
    availability = productData['availability']
    availability.strip()
    if availability == '':
        availability = "No information of availability available."
    productData['availability'] = availability

    # Cleaning product description
    description = productData['description']
    if not description:
        description.append("No description available.")
    productData['description'] = description

    return productData

