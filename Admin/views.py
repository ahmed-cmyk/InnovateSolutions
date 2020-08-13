from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db import transaction
from django.contrib.admin.views.decorators import staff_member_required
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.mail import send_mail

from Alumni.models import Alumni, AlumniJobApplication
from DjangoUnlimited.settings import DEFAULT_FROM_EMAIL
from django.utils import timezone
from datetime import timedelta, datetime, date
import csv
from django.http import HttpResponse, JsonResponse

# Create your views here.

from Home.forms import CreateJobForm, EditJobForm
from Employer.forms import InitialEmployerForm, EmployerForm, EmployerAccVerificationForm
from .forms import InitialAdminForm, AdminForm, AddIndustryForm, Statistics
from Accounts.views import isValidated, get_user_type, number_symbol_exists
from .models import Admin
from .forms import EditAdminProfileForm
from Student.forms import EditStudentProfileForm
from Student.models import Student, StudentJobApplication
from Home.models import Job, send_html_mail
from Employer.models import Employer
from Employer import views as EmployerViews


# Create your views here.

@staff_member_required
def create_admin(request):
    if request.method == 'POST':
        user_form = InitialAdminForm(request.POST)

        if user_form.is_valid():
            if user_form.usernameExists():
                messages.info(request,
                              'Username already taken. Try a different one.')  # checks if username exists in db
                return redirect("admin_register")

            elif user_form.emailExists():
                messages.info(request, 'Email already taken. Try a different one.')  # checks if email exists in db
                return redirect("admin_register")

            elif number_symbol_exists(user_form.cleaned_data["first_name"]):  # checks if number/symbol exists in string
                messages.info(request, 'Please enter a valid first name.')
                return redirect("admin_register")

            elif number_symbol_exists(user_form.cleaned_data["last_name"]):  # checks if number/symbol exists in string
                messages.info(request, 'Please enter a valid last name.')
                return redirect("admin_register")

            elif not user_form.samePasswords():
                messages.info(request,
                              'Passwords not matching. Try again.')  # checks if password and confirm password are matching
                return redirect("admin_register")

            elif not user_form.emailDomainExists():  # checks if there is an exising domain for given email
                messages.info(request, 'Email domain does not exist. Try again.')
                return redirect("admin_register")

            else:
                if isValidated(user_form.cleaned_data.get('password1')):  # checks if password is valid
                    admin_form = AdminForm(request.POST, request.FILES)

                    if admin_form.is_valid():
                        with transaction.atomic():
                            user = user_form.save()
                            admin = admin_form.save(commit=False)
                            admin.user = user
                            admin.save()
                            next_page = request.POST.get('next', '/')
                            return redirect(next_page)
                    else:
                        messages.error(request, admin_form.errors)
                        return redirect("admin_register")
                else:
                    messages.error(request,
                                   'ERROR: Password must be 8 characters or more, and must have atleast 1 numeric character and 1 letter.')
                    return redirect("admin_register")
        else:
            messages.error(request, user_form.errors)
            return redirect("admin_register")
    else:
        user_form = InitialAdminForm()
        admin_form = AdminForm()
        args = {'admin_form': admin_form, 'user_form': user_form}
        return render(request, 'Admin/admin_registration.html', args)


@staff_member_required
def view_pending(request):
    user = get_user_type(request)
    applicants_students = Student.objects.filter(is_active='Pending')
    applicants_alumni = Alumni.objects.filter(is_active='Pending')
    applicants_employers = Employer.objects.filter(is_active='Pending')
    args = {'user_type': user['user_type'], 'applicants_students': applicants_students, 'applicants_alumni': applicants_alumni, 'applicants_employers': applicants_employers}
    return render(request, 'Admin/view_pending_requests.html', args)


def change_accept_status(request):
    status = request.GET.get('status', 'Pending')
    user_id = request.GET.get('user_id', None)
    print(user_id)
    user = User.objects.get(id=user_id)
    print(user)

    subject = 'Account Verification Complete'
    htmlText = f"Your account creation request has been reviewed by an admin and the request has been {status}"

    try:
        user_employer = Employer.objects.get(user_id=user_id)
        user_employer.is_active = status
        user_employer.save()
        receipent = str(user_employer.user)
        send_html_mail(subject, htmlText, [receipent])
        print(user_employer.is_active)
    except:
        pass

    try:
        user_alumni = Alumni.objects.get(user_id=user_id)
        user_alumni.is_active = status
        user_alumni.save()
        receipent = str(user_alumni.user)
        send_html_mail(subject, htmlText, [receipent])
        print(user_alumni.is_active)
    except:
        pass

    try:
        user_student = Student.objects.get(user_id=user_id)
        user_student.is_active = status
        user_student.save()
        receipent = str(user_student.user)
        send_html_mail(subject, htmlText, [receipent])
        print(user_student.is_active)
    except:
        pass

    try:
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False})


@staff_member_required
def view_pend_acc_profile(request, id):
    try:
        student = Student.objects.get(user_id=id)
        user = get_user_type(request)
        args = {'student': student, 'obj': user['obj'], 'user_type': user['user_type']}
        return render(request, 'Home/student_details.html', args)
    except:
        pass

    try:
        alumni = Alumni.objects.get(user_id=id)
        user = get_user_type(request)
        args = {'alumni': alumni, 'obj': user['obj'], 'user_type': user['user_type']}
        return render(request, 'Home/alumni_details.html', args)
    except:
        pass

    try:
        employer = Employer.objects.get(user_id=id)
        user = get_user_type(request)
        args = {'employer': employer, 'obj': user['obj'], 'user_type': user['user_type']}
        return render(request, 'Admin/view_employer_profile.html', args)
    except:
        pass

    return redirect('view_pending_requests')


@staff_member_required
def view_pending_jobs(request):
    user = get_user_type(request)
    jobs = Job.objects.filter(is_active='Pending')
    args = {'user_type': user['user_type'], 'jobs': jobs}
    return render(request, 'Admin/view_pending_jobs.html', args)


@staff_member_required
def view_pending_job_details(request, id):
    user = get_user_type(request)
    job = Job.objects.get(id=id)
    companies = Employer.objects.all()

    if request.POST.get("viewcandidates"):
        alumniCandidates = AlumniJobApplication.objects.filter(job_id=job)
        studentCandidates = StudentJobApplication.objects.filter(job_id=job)
        args = {'studentCandidates': studentCandidates, 'alumniCandidates': alumniCandidates, 'obj': user['obj'],
                'user_type': user['user_type']}
        return render(request, 'Home/view_candidates.html', args)

    args = {'job': job, 'obj': user['obj'], 'user_type': user['user_type'],
            'companies': companies, 'applied': True}
    return render(request, 'Admin/job_details.html', args)


def change_job_status(request):
    status = request.GET.get('status', 'Pending')
    job_id = request.GET.get('user_id', None)

    subject = 'Job Verification Complete'
    htmlText = f"Your account Job request has been reviewed by an admin and the request has been {status}"

    try:
        print(id)
        job = Job.objects.get(id=job_id)
        print(job)
        print(job.posted_by)
        job.is_active = status
        job.save()
        receipent = str(job.posted_by)
        send_html_mail(subject, htmlText, [receipent])
        print(job.is_active)
    except:
        pass

    try:
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False})
# @staff_member_required
# def view_pending(request, id=None):
#     employers = Employer.objects.all()
#     form = EmployerAccVerificationForm()
#     print(id)
#     if id is not None:
#         print("I'm here")
#         print(request.method)
#         user = User.objects.filter(id=id)
#         args = {'user': user, 'employers': employers, 'form': form}
#         if 'accept' in request.GET:
#             print('I found an accept')
#             user.is_active = True
#             print(user.is_active)
#             messages.success(request, 'Account Approved')
#             return render(request, 'Admin/view_pending_requests.html', args)
#         elif 'reject' in request.GET:
#             print('I found a reject')
#             user.is_active = False
#             print(user.is_active)
#             messages.info(request, 'Account Rejected')
#             return render(request, 'Admin/view_pending_requests.html', args)
#         return render(request, 'Admin/view_pending_requests.html', args)
#     else:
#         print("Still else")
#         user = request.user
#         args = {'user': user, 'employers': employers, 'form': form}
#         return render(request, 'Admin/view_pending_requests.html', args)


@staff_member_required
def view_profile(request):
    user = request.user
    hasAdminDetails = True
    try:
        admin = Admin.objects.get(user_id=user.id)
        args = {'admin': admin, 'user': user, 'hasAdminDetails': hasAdminDetails}
        return render(request, 'admin/view_admin_profile.html', args)
    except:
        if request.method == 'POST':
            admin_form = AdminForm(request.POST, request.FILES)

            if admin_form.is_valid():
                with transaction.atomic():
                    admin = admin_form.save(commit=False)
                    admin.user = user
                    admin.save()
                    return redirect(request.path_info)
            else:
                messages.info(request, admin_form.errors)
                return redirect(request.path_info)

        else:
            hasAdminDetails = False
            admin_form = AdminForm()
            args = {'admin_form': admin_form, 'hasAdminDetails': hasAdminDetails}
            return render(request, 'admin/view_admin_profile.html', args)


@staff_member_required
def edit_profile(request):
    admin = Admin.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        user_form = EditAdminProfileForm(request.POST, instance=request.user)
        admin_form = AdminForm(request.POST, request.FILES, instance=admin)

        if user_form.is_valid() and admin_form.is_valid():
            with transaction.atomic():
                user_form.save()
                admin_form.save()
                next_page = request.POST.get('next', '/')
                return redirect(next_page)
        else:
            messages.info(request, admin_form.errors)
            messages.info(request, user_form.errors)
            return redirect(request.path_info)
    else:
        user_form = EditAdminProfileForm(instance=request.user)
        admin_form = AdminForm(instance=admin)
        args = {'admin_form': admin_form, 'user_form': user_form}
        return render(request, 'admin/edit_admin_profile.html', args)


@staff_member_required
def create_job(request):
    admin = Admin.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        jobForm = CreateJobForm(request.POST, request.FILES)
        companyForm = EmployerForm(request.POST, request.FILES)

        if jobForm.is_valid() and companyForm.is_valid():
            with transaction.atomic():
                company = companyForm.save(commit=False)
                company.user_id = admin.user.id
                company.save()
                job = jobForm.save(commit=False)
                job.save()

                subject = 'New Job has been posted'
                htmlText = 'A new Job has been posted on the Murdoch Career Portal.'
                send_html_mail(subject, htmlText, [DEFAULT_FROM_EMAIL])

                for skill in request.POST.getlist('skills'):
                    job.skills.add(skill)

                next_page = request.POST.get('next', '/')
                return redirect(next_page)
        else:
            messages.error(request, jobForm.errors)
            messages.error(request, companyForm.errors)
            return redirect(request.path_info)
    else:
        userForm = InitialEmployerForm()
        companyForm = EmployerForm()
        jobForm = CreateJobForm()

        args = {'companyForm': companyForm, 'jobForm': jobForm}
        return render(request, "Admin/admin_create_job.html", args)


def export_stats_file(request, users, admins, students, current, alumni, employers, jobs_posted, apps, open_jobs,
                      closed_jobs, deleted_jobs):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + date.today().strftime("%B %d %Y") + ".csv"
    writer = csv.writer(response)
    writer.writerow(['Type of Statistics', 'Count'])
    writer.writerow(['Total Users Signed Up', users])
    writer.writerow(['Administrators Signed Up', admins])
    writer.writerow(['Total Students Signed Up', students])
    writer.writerow(['Current Students Signed Up', current])
    writer.writerow(['Alumni Signed Up', alumni])
    writer.writerow(['Employers Signed Up', employers])
    writer.writerow(['Jobs Posted', jobs_posted])
    writer.writerow(['Student Applications', apps])
    writer.writerow(['Active Jobs', open_jobs])
    writer.writerow(['Jobs Closed and Filled by Murdoch Students', closed_jobs])
    writer.writerow(['Jobs Deleted', deleted_jobs])
    return response


@staff_member_required
def generate_statistics(request):
    user = get_user_type(request)
    if request.method == "POST":
        end_date = timezone.now()
        time = request.POST.get('period')
        if time == "Past 7 Days":
            start_date = end_date - timedelta(6)
        elif time == "Past 30 Days":
            start_date = end_date - timedelta(29)
        elif time == "Past Year":
            start_date = end_date - timedelta(364)

        users = User.objects.filter(date_joined__range=[start_date, end_date])
        admins = Admin.objects.filter(user_id__in=User.objects.filter(date_joined__range=[start_date, end_date]))
        admin_users = User.objects.filter(id__in=Admin.objects.all())
        students = Student.objects.filter(user_id__in=User.objects.filter(date_joined__range=[start_date, end_date]))
        current = Student.objects.filter(user_id__in=User.objects.filter(date_joined__range=[start_date, end_date]))
        alumni = Alumni.objects.filter(user_id__in=User.objects.filter(date_joined__range=[start_date, end_date]))
        employers = Employer.objects.filter(
            user_id__in=User.objects.filter(date_joined__range=[start_date, end_date])).exclude(user_id__in=admin_users)
        jobs_posted = Job.objects.filter(date_posted__range=[start_date, end_date])
        open_jobs = Job.objects.filter(date_posted__range=[start_date, end_date], status="Open")
        closed_jobs = Job.objects.filter(date_posted__range=[start_date, end_date], status="Closed")
        deleted_jobs = Job.objects.filter(date_posted__range=[start_date, end_date], status="Deleted")
        apps = StudentJobApplication.objects.filter(date_applied__range=[start_date, end_date])

        users = len(list(set(users)))
        admins = len(list(set(admins)))
        students = len(list(set(students))) + len(list(set(alumni)))
        current = len(list(set(current)))
        alumni = len(list(set(alumni)))
        employers = len(list(set(employers)))
        jobs_posted = len(list(set(jobs_posted)))
        open_jobs = len(list(set(open_jobs)))
        closed_jobs = len(list(set(closed_jobs)))
        deleted_jobs = len(list(set(deleted_jobs)))
        apps = len(list(set(apps)))

        args = {'users': users, 'admins': admins, 'students': students, 'current': current, 'alumni': alumni,
                'employers': employers,
                'jobs_posted': jobs_posted, 'open_jobs': open_jobs, 'closed_jobs': closed_jobs,
                'deleted_jobs': deleted_jobs, 'apps': apps, 'user_type': user['user_type'], 'obj': user['obj']}

        return render(request, "Admin/view_statistics.html", args)
    else:
        form = Statistics()
        args = {'form': form, 'user_type': user['user_type'], 'obj': user['obj']}
        return render(request, "Admin/generate_statistics.html", args)
