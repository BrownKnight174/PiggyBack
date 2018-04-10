from django.shortcuts import render
from django.views.generic import TemplateView

class ProductPage(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'product.html', context=None)


class PaymentsPage(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'Payment_Details.html', context=None)