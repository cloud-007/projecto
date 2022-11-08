from django.shortcuts import render
from django.views import View


class SignInView(View):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
