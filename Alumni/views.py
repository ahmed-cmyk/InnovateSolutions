from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db import transaction
from django.contrib.auth.decorators import login_required

from Accounts.views import isValidated, get_user_type
from .models import Alumni
from .forms import *

def signup(request):
	if request.method == 'POST':
		user_form = InitialAlumniForm(request.POST)

		if user_form.is_valid():
			if user_form.usernameExists():
				messages.info(request, 'Username already taken. Try a different one.') #checks if username exists in db
				return redirect("alumni_register")

			elif user_form.emailExists():
				messages.info(request, 'Email already taken. Try a different one.') #checks if email exists in db
				return redirect("alumni_register")

			elif not user_form.samePasswords():
				messages.info(request, 'Passwords not matching. Try again.') #checks if password and confirm password are matching
				return redirect("alumni_register")

			elif not user_form.emailDomainExists():
				messages.info(request, 'Email domain does not exist. Try again.') #checks if there is an exising domain for given email
				return redirect("alumni_register")

			else:
				if isValidated(user_form.cleaned_data.get('password1')): #checks if password is valid
					alumni_form = AlumniForm(request.POST, request.FILES)

					if alumni_form.is_valid():
						with transaction.atomic():
							user = user_form.save()
							alumni = alumni_form.save(commit=False)
							alumni.user = user
							alumni.save()
							alumni_form.save_m2m()

						messages.success(request, 'Alumni account created')
						return redirect("log_in")

					else:
						messages.error(request, alumni_form.errors)
						return redirect("alumni_register")

				else:
					messages.info(request,'ERROR: Password must be 8 characters or more, and must have atleast 1 numeric character and 1 letter.')
					return redirect("alumni_register")

		else:
			messages.info(request, user_form.errors)
			return redirect("alumni_register")

	else:
		user_form = InitialAlumniForm()
		alumni_form = AlumniForm()
		user = get_user_type(request)
		args = {'alumni_form': alumni_form, 'user_form': user_form, 'user_type': user['user_type']}
		
		return render(request, 'Alumni/alumni_registration.html', args)

@login_required
def edit_profile(request):
    alumni = Alumni.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        user_form = EditAlumniProfileInitialForm(request.POST, instance=request.user)
        alumni_form = EditAlumniProfileForm(request.POST, request.FILES, instance=alumni)

        if user_form.is_valid() and alumni_form.is_valid():
            with transaction.atomic():
                user_form.save()
                alumni_form.save()
                return redirect('view_alumni_profile')
        else:
            print(alumni_form)
            messages.error(request, alumni_form.errors)
            messages.error(request, user_form.errors)
            return redirect("edit_alumni_profile")
    else:
        user_form = EditAlumniProfileInitialForm(instance=request.user)
        alumni_form = EditAlumniProfileForm(instance=alumni)
        args = {'alumni_form': alumni_form, 'user_form': user_form, 'user_type': "alumni", 'obj': alumni}
        return render(request, 'Alumni/edit_alumni_profile.html', args)


@login_required
def view_profile(request):
    user = request.user
    u = get_user_type(request)
    args = {'user': user, 'user_type': u['user_type'], 'obj': u['obj']}
    return render(request, 'Alumni/view_alumni_profile.html', args)