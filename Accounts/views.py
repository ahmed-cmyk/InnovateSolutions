from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.views.generic import TemplateView
from django.http import JsonResponse

from Student.models import Student
from Alumni.models import Alumni
from Employer.models import Employer
from Admin.models import Admin


def isValidated(passwd):
    status = True

    if len(passwd) > 8:
        status = True

    if not any(char.isdigit() for char in passwd):
        status = False

    if not any(char.isalpha() for char in passwd):
        status = False

    return status


def number_symbol_exists(string):
    status = False

    special_symbols = {'$', '@', '%', '&', '?', '.', '!', '#', '*', '_'}

    if any(char.isdigit() for char in string):
        status = True

    if any(char in special_symbols for char in string):
        status = True

    return status


def check_username(request):
    if request.is_ajax and request.method == 'GET':
        email = request.GET.get("username", None)
        if Alumni.objects.filter(username=email).exists():
            return JsonResponse({"valid": False}, status=200)
        else:
            return JsonResponse({"valid": True}, status=200)

    return JsonResponse({}, status=400)


def signup(request):
    return render(request, 'signup.html', get_user_type(request))


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is None:
            messages.info(request, 'Credentials do not exist, please try a different username/password')
            return redirect("log_in")
        else:
            if user.is_superuser == True or user.is_staff == True:
                messages.info(request, 'To login in as admin, please visit the admin site.')
                return redirect("log_in")
            else:
                auth.login(request, user)
                auth_user = get_user_type(request)
                print(auth_user['user_type'])
                if auth_user['user_type'] == 'employer':
                    print('This is an employer')
                return redirect('/', get_user_type(request))
                # return render(request, "Home/index.html", get_user_type(request))
    else:
        return render(request, 'login.html', get_user_type(request))


def forgot_password(request):
    if request.method == 'POST':
        return redirect("/")
    else:
        return render(request, 'Accounts/forgot_password.html')


def logout(request):
    auth.logout(request)
    return redirect("/")


def get_user_type(request):
    type = 'none'
    args = {'user_type': type}

    try:
        e = Employer.objects.get(user_id=request.user.id)
        type = 'employer'
        args = {'user_type': type, 'obj': e}
    except Employer.DoesNotExist:
        pass

    try:
        s = Student.objects.get(user_id=request.user.id)
        type = 'student'
        args = {'user_type': type, 'obj': s}
    except Student.DoesNotExist:
        pass

    try:
        al = Alumni.objects.get(user_id=request.user.id)
        type = 'alumni'
        args = {'user_type': type, 'obj': al}
    except Alumni.DoesNotExist:
        pass

    try:
        a = Admin.objects.get(user_id=request.user.id)
        type = 'admin'
        args = {'user_type': type, 'obj': a}
    except Admin.DoesNotExist:
        pass

    return args
