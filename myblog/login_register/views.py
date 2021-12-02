from django.shortcuts import render


def loginPage(request):
    return render(request, 'login_register/login_register.html')
