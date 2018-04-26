from django.shortcuts import render
from django.views.generic import TemplateView

class TravellerPage(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'traveller.html', context=None)


class VerificationPage(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'Verification.html', context=None)
