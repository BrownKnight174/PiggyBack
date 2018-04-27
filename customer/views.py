from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.conf import settings
import platform
from django.contrib import messages
from customer.models import Customer, Order
from django.contrib.auth.models import User
from django.utils import timezone


class ProductPage(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'productDescription.html', context=None)

    def post(self, request, **kwargs):
        if request.POST['action'] == "Continue":

            url = request.POST.get("sendURL")

            try:
                productData = GetProductData(url)
            except:
                messages.error(request, "Please enter valid URL!")
                return render(request, "home.html", context={"user": request.user})

            if productData is None:
                messages.error(request, "Please enter valid URL!")
                return render(request, "home.html", context={"user": request.user})
            else:
                try:
                    cleanData = CleanData(productData)
                except:
                    cleanData = productData

                request.session['productCost'] = productData['productCost'][1:]
                request.session['productTitle'] = productData['productTitle']
                request.session['url'] = url

                return render(request, 'productDescription.html', context=cleanData)
        else:
            return render(request, "home.html")


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
            context = {'productCost': str(float(cost)*100*0.15), 'productTitle': title}
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
        order = Order()
        order.product_name = request.session['productTitle']
        order.product_url = request.session['url']
        order.fee = float(request.session['productCost'])*0.15
        order.status = "Finding a traveller"
        order.creation_time = timezone.now()
        order.save()

        user = User.objects.get(pk=request.user.pk)

        customer = Customer()
        customer.order = order
        customer.user = user
        customer.save()

        messages.info(request, "Payment successful! We'll notify you when we find a traveller for you!")
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

    try:
        productTitle = browser.find_element_by_id('productTitle').text
        print(productTitle)

        try:
            try:
                productCost = browser.find_element_by_id('priceblock_ourprice').text
                print(productCost.strip())
                if productCost == "":
                    productCost = browser.find_element_by_id('priceblock_usedprice').text
                    print(productCost.strip())
            except:
                productCost = browser.find_element_by_id('priceblock_usedprice').text
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

    except:
        productData = None

    return productData


def CleanData(productData):
    # Cleaning cost
    cost = productData.get("productCost", "")
    cost.strip()
    splitCost = cost.split()
    if len(splitCost) == 3:
        print(splitCost)
        cleanedCost = splitCost[0] + splitCost[1] + '.' + splitCost[2]
    elif len(splitCost) == 1:
        cleanedCost = splitCost[0]
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

