import mimetypes
import os
import time
import datetime

from django.core.files.storage import get_storage_class
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string

from Alumni.models import Alumni, AlumniJobApplication
from DjangoUnlimited.settings import DEFAULT_FROM_EMAIL, BASE_DIR, BACKUP_ROOT
from django.utils import timezone
from datetime import timedelta, date
import csv
import subprocess
from django.http import HttpResponse, JsonResponse

# Create your views here.

from Home.forms import CreateJobForm
from Employer.forms import InitialEmployerForm, EmployerForm
from .forms import InitialAdminForm, AdminForm, Statistics, JobStats, StudentStats
from Accounts.views import isValidated, get_user_type, number_symbol_exists
from .models import Admin
from .forms import EditAdminProfileForm
from Student.forms import EditStudentProfileForm, EditStudentProfileInitialForm
from Student.models import Student, StudentJobApplication
from Home.models import Job, send_html_mail
from Employer.models import Employer
from Alumni.forms import EditAlumniProfileInitialForm, EditAlumniProfileForm


# Create your views here.
@staff_member_required
def backup_database(request):
    if 'backup_database' in request.POST:
        DB_USER = 'postgres'
        DB_NAME = 'django_unlimited'

        # BACKUP_PATH = r'backup'
        filename = time.strftime("%Y%m%d_%H%M%S") + '_backup.sql'
        destination = r'%s/%s' % (BACKUP_ROOT, filename)

        print('Backing up %s database to %s' % (DB_NAME, destination))
        ps = subprocess.Popen(
            ['pg_dump', '-U', DB_USER, '-h', 'localhost', '-d', DB_NAME, '-f', destination],
            stdout=subprocess.PIPE
        )
        return redirect('backup_view')


def download_file(request):
    filename = 'DB_backup.sql'
    return redirect('backup_download/%s' % (filename))


def download_source_code(request):
    extension = 'zip'
    code_storage = get_storage_class()()

    # zip_filename = 'SourceCodeBackup.zip'
    # ziph = zipfile.ZipFile('SourceCodeBackup.zip', 'w')
    # for root, dirs, files in os.walk(BASE_DIR):
    #     for file in files:
    #         ziph.write(os.path.join(root, file))
    #
    # ziph.close()
    # print('---------------Ziph---------------' + str(ziph))
    # resp = HttpResponse(mimetype="application/x-zip-compressed")
    # resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
    #
    # return resp


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
                        messages.warning(request, admin_form.errors.as_text)
                        return redirect("admin_register")
                else:
                    messages.warning(request,
                                     'ERROR: Password must be 8 characters or more, and must have at least 1 numeric character and 1 letter.'
                                     'character and 1 letter.')
                    return redirect("admin_register")
        else:
            messages.warning(request, user_form.errors.as_text)
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
    args = {'user_type': user['user_type'], 'applicants_students': applicants_students,
            'applicants_alumni': applicants_alumni, 'applicants_employers': applicants_employers}
    return render(request, 'Admin/view_pending_requests.html', args)


def change_accept_status(request):
    status = request.GET.get('status', 'Pending')
    user_id = request.GET.get('user_id', None)
    print(user_id)
    user = User.objects.get(id=user_id)
    print(user)

    subject = 'Your account creation request has been resolved'

    try:
        user_employer = Employer.objects.get(user_id=user_id)
        user_employer.is_active = status
        user_employer.save()
        receipent = str(user_employer.user)

        first_name = user_employer.company_name
        context = {'first_name': first_name, 'status': status}

        htmlText = render_to_string('Accounts/account_creation_resolution.html', context)
        send_html_mail(subject, htmlText, [receipent])
    except:
        pass

    try:
        user_alumni = Alumni.objects.get(user_id=user_id)
        user_alumni.is_active = status
        user_alumni.save()
        receipent = str(user_alumni.user)

        first_name = user_alumni.user.first_name
        context = {'first_name': first_name, 'status': status}

        htmlText = render_to_string('Accounts/account_creation_resolution.html', context)
        send_html_mail(subject, htmlText, [receipent])
    except:
        pass

    try:
        user_student = Student.objects.get(user_id=user_id)
        user_student.is_active = status
        user_student.save()
        receipent = str(user_student.user)

        first_name = user_student.user.first_name
        context = {'first_name': first_name, 'status': status}

        htmlText = render_to_string('Accounts/account_creation_resolution.html', context)
        send_html_mail(subject, htmlText, [receipent])
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
def view_employer_profile(request, id):
    user = get_user_type(request)
    employer = Employer.objects.get(user_id=id)
    args = {'employer': employer, 'user_type': user['user_type']}
    return render(request, 'Admin/view_employer_profile.html', args)


@staff_member_required
def edit_employer_profile(request, id):
    user = get_user_type(request)
    if user['obj'] is not None:
        if request.method == 'POST':
            employer = Employer.objects.get(user_id=id)
            form = EmployerForm(request.POST, request.FILES, instance=employer)
            if form.is_valid():
                form.save()
                url = '{}/{}'.format('/my_admin/view_employer_profile', id)
                return redirect(url)
            else:
                messages.warning(request, form.errors.as_text)
                url = '{}/{}'.format('/my_admin/edit_employer_profile', id)
                return redirect(url)
        else:
            employer = Employer.objects.get(user_id=id)
            form = EmployerForm(instance=employer)
            args = {'employer_form': form, 'obj': employer, 'user_type': user['user_type']}
            return render(request, 'Employer/edit_employer_profile.html', args)
    else:
        messages.info(request, 'This employer user does not exist')


@staff_member_required
def view_student_profile(request, id):
    user = get_user_type(request)
    student = Student.objects.get(user_id=id)
    args = {'student': student, 'user_type': user['user_type']}
    return render(request, 'Home/student_details.html', args)


@staff_member_required
def edit_student_profile(request, id):
    if request.method == 'POST':
        student = Student.objects.get(user_id=id)
        user_form = EditStudentProfileInitialForm(request.POST, instance=student.user)
        student_form = EditStudentProfileForm(request.POST, request.FILES, instance=student)

        if user_form.is_valid() and student_form.is_valid():
            with transaction.atomic():
                user_form.save()
                student_form.save()
                url = '{}/{}'.format('/my_admin/view_student_profile', id)
                return redirect(url)
        else:
            messages.warning(request, student_form.errors.as_text)
            messages.warning(request, user_form.errors.as_text)
            url = '{}/{}'.format('/my_admin/edit_student_profile', id)
            return redirect(url)
    else:
        student = Student.objects.get(user_id=id)
        user_form = EditStudentProfileInitialForm(instance=student.user)
        student_form = EditStudentProfileForm(instance=student)
        args = {'student_form': student_form, 'user_form': user_form, 'user_type': "admin", 'obj': student}
        return render(request, 'Student/edit_student_profile.html', args)


@staff_member_required
def view_alumni_profile(request, id):
    user = get_user_type(request)
    alumni = Alumni.objects.get(user_id=id)
    args = {'alumni': alumni, 'user_type': user['user_type']}
    return render(request, 'Home/alumni_details.html', args)


@staff_member_required
def edit_alumni_profile(request, id):
    if request.method == 'POST':
        alumni = Alumni.objects.get(user_id=id)
        user_form = EditAlumniProfileInitialForm(request.POST, instance=alumni.user)
        alumni_form = EditAlumniProfileForm(request.POST, request.FILES, instance=alumni)
        if user_form.is_valid() and alumni_form.is_valid():
            with transaction.atomic():
                user_form.save()
                alumni_form.save()
                messages.success(request, 'Profile edit was successful')
                url = '{}/{}'.format('/my_admin/view_alumni_profile', id)
                return redirect(url)
        else:
            messages.warning(request, alumni_form.errors.as_text)
            messages.warning(request, user_form.errors.as_text)
            url = '{}/{}'.format('/my_admin/edit_alumni_profile', id)
            return redirect(url)
    else:
        alumni = Alumni.objects.get(user_id=id)
        user_form = EditAlumniProfileInitialForm(instance=alumni.user)
        alumni_form = EditAlumniProfileForm(instance=alumni)
        args = {'alumni_form': alumni_form, 'user_form': user_form, 'user_type': "admin", 'obj': alumni}
        return render(request, 'Alumni/edit_alumni_profile.html', args)


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

    subject = 'Your job posting request has been resolved'

    try:
        print(id)
        job = Job.objects.get(id=job_id)
        print(job)
        print(job.posted_by)
        job.is_active = status
        job.save()
        receipent = str(job.posted_by)

        first_name = job.posted_by.company_name
        context = {'first_name': first_name, 'status': status}

        htmlText = render_to_string('Employer/job_post_resolution.html', context)
        send_html_mail(subject, htmlText, [receipent])
        print(job.is_active)
    except:
        pass

    try:
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False})


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
            user_form = EditAdminProfileForm(request.POST, instance=request.user)

            if user_form.is_valid() and admin_form.is_valid():
                with transaction.atomic():
                    admin = admin_form.save(commit=False)
                    admin.user = user
                    user_form.save()
                    admin.save()
                    return redirect(request.path_info)
            else:
                messages.info(request, admin_form.errors)
                return redirect(request.path_info)

        else:
            hasAdminDetails = False
            admin_form = AdminForm()
            user_form = EditAdminProfileForm(instance=request.user)
            args = {'admin_form': admin_form, 'user_form': user_form, 'hasAdminDetails': hasAdminDetails}
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
            messages.warning(request, jobForm.errors.as_text)
            messages.warning(request, companyForm.errors.as_text)
            return redirect(request.path_info)
    else:
        userForm = InitialEmployerForm()
        companyForm = EmployerForm()
        jobForm = CreateJobForm()

        args = {'companyForm': companyForm, 'jobForm': jobForm}
        return render(request, "Admin/admin_create_job.html", args)

@staff_member_required
def export_stats_file(request, users, admins, students, current, alumni, employers, jobs_posted, apps, open_jobs,
                      closed_jobs, deleted_jobs, total_users, pending_users, pending_jobs, alumni_apps, rejected_users, rejected_jobs):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + date.today().strftime("%B %d %Y") + ".csv"
    writer = csv.writer(response)
    writer.writerow(['Type of Statistics', 'Count'])
    writer.writerow(['Total Users', total_users])
    writer.writerow(['Total Approved Users', users])
    writer.writerow(['Administrators', admins])
    writer.writerow(['Total Students', students])
    writer.writerow(['Current Students', current])
    writer.writerow(['Alumni Students', alumni])
    writer.writerow(['Employers', employers])
    writer.writerow(['Users Pending Approval', pending_users])
    writer.writerow(['Users Rejected', rejected_users])
    writer.writerow(['Jobs Posted', jobs_posted])
    writer.writerow(['Jobs Pending Approval', pending_jobs])
    writer.writerow(['Jobs Rejected', rejected_jobs])
    writer.writerow(['Current Student Applications', apps])
    writer.writerow(['Alumni Applications', alumni_apps])
    writer.writerow(['Active Jobs', open_jobs])
    writer.writerow(['Jobs Closed and Filled by Murdoch Students', closed_jobs])
    writer.writerow(['Jobs Deleted', deleted_jobs])
    return response


@staff_member_required
def generate_statistics(request):
    user = get_user_type(request)
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)
        admins = Admin.objects.filter(
            user_id__in=User.objects.filter(date_joined__range=[start_date, end_date]))
        admin_users = User.objects.filter(id__in=Admin.objects.all())
        current = Student.objects.filter(is_active='Accepted', user_id__in=User.objects.filter(
            date_joined__range=[start_date, end_date]))
        alumni = Alumni.objects.filter(is_active='Accepted', user_id__in=User.objects.filter(
            date_joined__range=[start_date, end_date]))
        employers = Employer.objects.filter(is_active='Accepted',
            user_id__in=User.objects.filter(date_joined__range=[start_date, end_date])).exclude(
            user_id__in=admin_users)
        jobs_posted = Job.objects.filter(date_posted__range=[start_date, end_date], is_active='Accepted')
        open_jobs = Job.objects.filter(date_posted__range=[start_date, end_date], status="Open", is_active='Accepted')
        closed_jobs = Job.objects.filter(date_posted__range=[start_date, end_date], status="Closed", is_active='Accepted')
        deleted_jobs = Job.objects.filter(date_posted__range=[start_date, end_date], status="Deleted", is_active='Accepted')
        apps = StudentJobApplication.objects.filter(date_applied__range=[start_date, end_date])
        alumni_apps = AlumniJobApplication.objects.filter(date_applied__range=[start_date, end_date])

        pending_employers = Employer.objects.filter(is_active='Pending',
            user_id__in=User.objects.filter(date_joined__range=[start_date, end_date])).exclude(
            user_id__in=admin_users)
        pending_students = Student.objects.filter(is_active='Pending', user_id__in=User.objects.filter(
            date_joined__range=[start_date, end_date]))
        pending_alumni = Alumni.objects.filter(is_active='Pending', user_id__in=User.objects.filter(
            date_joined__range=[start_date, end_date]))
        rejected_employers = Employer.objects.filter(is_active='Rejected',
                                                    user_id__in=User.objects.filter(
                                                        date_joined__range=[start_date, end_date])).exclude(
            user_id__in=admin_users)
        rejected_students = Student.objects.filter(is_active='Rejected', user_id__in=User.objects.filter(
            date_joined__range=[start_date, end_date]))
        rejected_alumni = Alumni.objects.filter(is_active='Rejected', user_id__in=User.objects.filter(
            date_joined__range=[start_date, end_date]))
        pending_jobs = Job.objects.filter(date_posted__range=[start_date, end_date], is_active='Pending')
        rejected_jobs = Job.objects.filter(date_posted__range=[start_date, end_date], is_active='Rejected')
        total_users = User.objects.filter(date_joined__range=[start_date, end_date])

        total_users = len(list(set(total_users)))
        admins = len(list(set(admins)))
        current = len(list(set(current)))
        alumni = len(list(set(alumni)))
        employers = len(list(set(employers)))
        jobs_posted = len(list(set(jobs_posted)))
        open_jobs = len(list(set(open_jobs)))
        closed_jobs = len(list(set(closed_jobs)))
        deleted_jobs = len(list(set(deleted_jobs)))
        apps = len(list(set(apps)))
        alumni_apps = len(list(set(alumni_apps)))
        pending_employers = len(list(set(pending_employers)))
        pending_students = len(list(set(pending_students)))
        pending_alumni = len(list(set(pending_alumni)))
        pending_jobs = len(list(set(pending_jobs)))
        rejected_employers = len(list(set(rejected_employers)))
        rejected_students = len(list(set(rejected_students)))
        rejected_alumni = len(list(set(rejected_alumni)))
        rejected_jobs = len(list(set(rejected_jobs)))

        pending_users = pending_employers + pending_students + pending_alumni
        rejected_users = rejected_employers + rejected_students + rejected_alumni
        users = admins + current + alumni + employers
        students = current + alumni

        args = {'users': users, 'admins': admins, 'students': students, 'current': current, 'alumni': alumni,
                'employers': employers, 'pending_users': pending_users, 'pending_jobs': pending_jobs,
                'jobs_posted': jobs_posted, 'open_jobs': open_jobs, 'closed_jobs': closed_jobs, 'total_users':total_users,
                'deleted_jobs': deleted_jobs, 'apps': apps, 'alumni_apps': alumni_apps, 'rejected_users': rejected_users,
                'rejected_jobs': rejected_jobs, 'user_type': user['user_type'], 'obj': user['obj']}

        return render(request, "Admin/view_statistics.html", args)
    else:
        form = Statistics()
        args = {'form': form, 'user_type': user['user_type'], 'obj': user['obj']}
        return render(request, "Admin/generate_statistics.html", args)


@staff_member_required
def generate_job_statistics(request):
    user = get_user_type(request)
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)
        location = request.POST.get("location")
        industry = request.POST.getlist("industry")
        job_type = request.POST.get("job_type")

        if location and location != "--Select--":
            location_jobs = Job.objects.filter(location=location, date_posted__range=[start_date, end_date])
        else:
            location_jobs = Job.objects.all()

        if job_type and job_type != "---------":
            job_type_jobs = Job.objects.filter(job_type_id=job_type, date_posted__range=[start_date, end_date])
        else:
            job_type_jobs = Job.objects.all()

        if industry:
            industry_jobs = Job.objects.filter(industry_id__in=industry, date_posted__range=[start_date, end_date])
        else:
            industry_jobs = Job.objects.all()

        filtered_jobs = location_jobs & job_type_jobs & industry_jobs
        open_jobs = filtered_jobs.filter(status="Open", is_active='Accepted')
        closed_jobs = filtered_jobs.filter(status="Closed", is_active='Accepted')
        deleted_jobs = filtered_jobs.filter(status="Deleted", is_active='Accepted')
        pending_jobs = filtered_jobs.filter(date_posted__range=[start_date, end_date], is_active='Pending')
        rejected_jobs = filtered_jobs.filter(date_posted__range=[start_date, end_date], is_active='Rejected')

        total_jobs = len(list(set(filtered_jobs)))
        open_jobs = len(list(set(open_jobs)))
        closed_jobs = len(list(set(closed_jobs)))
        deleted_jobs = len(list(set(deleted_jobs)))
        pending_jobs = len(list(set(pending_jobs)))
        rejected_jobs = len(list(set(rejected_jobs)))
        total_accepted_jobs = open_jobs + closed_jobs + deleted_jobs

        args = {'total_jobs': total_jobs, 'total_accepted_jobs': total_accepted_jobs, 'open_jobs': open_jobs,
                'closed_jobs': closed_jobs, 'deleted_jobs': deleted_jobs, 'pending_jobs': pending_jobs,
                'rejected_jobs': rejected_jobs, 'user_type': user['user_type'], 'obj': user['obj']}

        return render(request, "Admin/view_job_statistics.html", args)

    else:
        form = JobStats()
        args = {'form': form, 'user_type': user['user_type'], 'obj': user['obj']}
        return render(request, "Admin/generate_statistics.html", args)

@staff_member_required
def export_job_stats(request, total_jobs, accepted_jobs, open_jobs, closed_jobs, deleted_jobs, pending_jobs, rejected_jobs):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="JobStats"' + date.today().strftime("%B %d %Y") + ".csv"
    writer = csv.writer(response)
    writer.writerow(['Type of Statistics', 'Count'])
    writer.writerow(['Total Jobs', total_jobs])
    writer.writerow(['Total Accepted Jobs', accepted_jobs])
    writer.writerow(['Open Jobs', open_jobs])
    writer.writerow(['Closed Jobs', closed_jobs])
    writer.writerow(['Deleted Jobs', deleted_jobs])
    writer.writerow(['Pending Jobs', pending_jobs])
    writer.writerow(['Rejected Jobs', rejected_jobs])
    return response


@staff_member_required
def generate_student_statistics(request):
    user = get_user_type(request)
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)
        major = request.POST.getlist("major")
        skill = request.POST.getlist("skill")

        users = User.objects.filter(date_joined__range=[start_date, end_date])
        students = Student.objects.filter(user_id__in=users)
        alumni = Alumni.objects.filter(user_id__in=users)

        if major:
            major_students = students.filter(majors__in=major)
            major_alumni = alumni.filter(majors__in=major)
        else:
            major_students = students
            major_alumni = alumni

        if skill:
            skill_students = students.filter(skills__in=skill)
            skill_alumni = alumni.filter(skills__in=skill)
        else:
            skill_students = students
            skill_alumni = alumni

        filtered_students = major_students & skill_students
        filtered_alumni = major_alumni & skill_alumni
        accepted_students = filtered_students.filter(is_active='Accepted')
        accepted_alumni = filtered_alumni.filter(is_active='Accepted')
        pending_students = filtered_students.filter(is_active='Pending')
        pending_alumni = filtered_alumni.filter(is_active='Pending')
        rejected_students = filtered_students.filter(is_active='Rejected')
        rejected_alumni = filtered_alumni.filter(is_active='Rejected')

        filtered_students = len(list(set(filtered_students)))
        filtered_alumni = len(list(set(filtered_alumni)))
        accepted_students = len(list(set(accepted_students)))
        accepted_alumni = len(list(set(accepted_alumni)))
        pending_students = len(list(set(pending_students)))
        pending_alumni = len(list(set(pending_alumni)))
        rejected_students = len(list(set(rejected_students)))
        rejected_alumni = len(list(set(rejected_alumni)))

        args = {'students': filtered_students, 'alumni': filtered_alumni, 'pending_students': pending_students,
                'pending_alumni': pending_alumni, 'rejected_students': rejected_students, 'rejected_alumni': rejected_alumni,
                'accepted_students': accepted_students, 'accepted_alumni' : accepted_alumni, 'user_type': user['user_type'],
                'obj': user['obj']}
        return render(request, "Admin/view_student_statistics.html", args)
    else:
        form = StudentStats()
        args = {'form': form, 'user_type': user['user_type'], 'obj': user['obj']}
        return render(request, "Admin/generate_statistics.html", args)

@staff_member_required
def export_student_stats(request, students, accepted_students, pending_students, rejected_students, alumni, accepted_alumni,
                         pending_alumni, rejected_alumni):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Student & Alumni Stats"' + date.today().strftime("%B %d %Y") + ".csv"
    writer = csv.writer(response)
    writer.writerow(['Type of Statistics', 'Count'])
    writer.writerow(['Total Student', students])
    writer.writerow(['Accepted Students', accepted_students])
    writer.writerow(['Pending Students', pending_students])
    writer.writerow(['Rejected Students', rejected_students])
    writer.writerow(['Total Alumni', alumni])
    writer.writerow(['Accepted Alumni', accepted_alumni])
    writer.writerow(['Pending Alumni', pending_alumni])
    writer.writerow(['Rejected Alumni', rejected_alumni])
    return response