from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
from django.contrib import messages
from DjangoUnlimited.settings import DEFAULT_FROM_EMAIL
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.core.files import File
import os
from django.contrib.postgres.search import SearchVector
# Create your views here.

from Employer.models import Employer
from Admin.models import Admin
from Student.models import Student, StudentJobApplication
from Alumni.models import Alumni, AlumniJobApplication
from Accounts.views import get_user_type
from .models import Job, Skill, UserNotifications, send_html_mail
from .forms import CreateJobForm, EditJobForm, FilterJobForm, FilterStudentForm, FilterAlumniForm
from Employer.forms import EmployerForm, InitialEmployerForm, EditEmployerForm
from Student.forms import StudentJobApplicationForm
from Alumni.forms import AlumniJobApplicationForm


def index(request):
    user = get_user_type(request)
    if request.user.is_authenticated:
        if request.method == 'POST':
            text = request.POST.get("search_item")
            if text:
                jobs = Job.objects.annotate(search=SearchVector('job_title', 'description'), ).filter(search=text)
                form = FilterJobForm()
                companies = Employer.objects.all()
                args = {'companies': companies, 'jobs': jobs, 'obj': user['obj'], 'user_type': user['user_type'],
                        'form': form}
                return render(request, "Home/view_jobs.html", args)
        else:
            try:
                if user['user_type'] == 'employer':
                    latest_jobs = Job.objects.filter(posted_by=user['obj']).exclude(is_active='Rejected',
                                                                                    status="Deleted").order_by(
                        '-date_posted')[:3]
                else:
                    latest_jobs = Job.objects.filter(status="Open", is_active='Accepted').order_by('-date_posted')[:3]
                args = {'job_list': latest_jobs, 'obj': user['obj'], 'user_type': user['user_type']}
                return render(request, "Home/index.html", args)
            except:
                return render(request, "Home/index.html", user)

    return render(request, "Home/index.html", user)


def terms(request):
    return render(request, "Home/terms.html", get_user_type(request))


def faq(request):
    return render(request, "Home/faq.html", get_user_type(request))


def anti_scam(request):
    return render(request, "Home/anti_scam.html", get_user_type(request))


def privacy(request):
    return render(request, "Home/privacy.html", get_user_type(request))


def sitemap(request):
    return render(request, "Home/sitemap.html", get_user_type(request))


def get_user(request):
    try:
        student = Student.objects.get(user_id=request.user.id)
        return student
    except:
        pass

    try:
        alumni = Alumni.objects.get(user_id=request.user.id)
        return alumni
    except:
        pass


@login_required
def view_jobs(request):
    user = get_user_type(request)
    if request.method == 'POST':
        min_duration = request.POST.get("min_duration")
        max_duration = request.POST.get("max_duration")
        duration_type = request.POST.get("duration_type")
        location = request.POST.get("location")
        job_type_id = request.POST.get("job_type_id")
        salary_min = request.POST.get("salary_min")
        salary_max = request.POST.get("salary_max")
        industry_id = request.POST.get("industry_id")
        if min_duration:
            min_duration_jobs = Job.objects.filter(duration__gte=min_duration)
        else:
            min_duration_jobs = Job.objects.all()

        if max_duration:
            max_duration_jobs = Job.objects.filter(duration__lte=max_duration)
        else:
            max_duration_jobs = Job.objects.all()

        if duration_type and duration_type != "--Select--":
            chosen_duration_type = Job.objects.filter(duration_type=duration_type)
        else:
            chosen_duration_type = Job.objects.all()

        if location and location != "--Select--":
            location_jobs = Job.objects.filter(location=location)
        else:
            location_jobs = Job.objects.all()

        if salary_min:
            min_salary_jobs = Job.objects.filter(salary_min_gte=salary_min)
        else:
            min_salary_jobs = Job.objects.all()

        if salary_max:
            max_salary_jobs = Job.objects.filter(salary_max_lte=salary_max)
        else:
            max_salary_jobs = Job.objects.all()

        if job_type_id:
            job_type_id_jobs = Job.objects.filter(job_type_id=job_type_id)
        else:
            job_type_id_jobs = Job.objects.all()

        if industry_id:
            industry_id_jobs = Job.objects.filter(industry_id=industry_id)
        else:
            industry_id_jobs = Job.objects.all()

        filtered_jobs = min_duration_jobs & max_duration_jobs & chosen_duration_type & location_jobs & max_salary_jobs & min_salary_jobs & job_type_id_jobs & industry_id_jobs
        jobs_all = Job.objects.filter(status="Open", is_active='Accepted').order_by('-date_posted')
        jobs = jobs_all & filtered_jobs
        form = FilterJobForm()
        companies = Employer.objects.all()

        args = {'companies': companies, 'jobs': jobs, 'obj': user['obj'], 'user_type': user['user_type'], 'form': form}
        return render(request, "Home/view_jobs.html", args)
    elif user['user_type'] == 'employer':
        jobs = Job.objects.filter(posted_by=request.user.id).order_by('-date_posted').exclude(status="Deleted")
        args = {'jobs': jobs, 'obj': user['obj'], 'user_type': user['user_type']}
    elif user['user_type'] == 'admin':
        jobs = Job.objects.filter(is_active='Accepted').exclude(status="Deleted").order_by('-date_posted')
        companies = Employer.objects.all()
        form = FilterJobForm()
        args = {'jobs': jobs, 'companies': companies, 'form': form, 'obj': user['obj'], 'user_type': user['user_type']}
    elif user['user_type'] == 'student' or user['user_type'] == 'alumni':
        jobs = Job.objects.filter(status="Open", is_active='Accepted').order_by('-date_posted')
        companies = Employer.objects.all()
        student = get_user(request)
        jobs_applied = student.jobs_applied.all().values_list('id', flat=True)
        form = FilterJobForm()
        args = {'jobs': jobs, 'companies': companies, 'form': form, 'obj': user['obj'], 'user_type': user['user_type'],
                'jobs_applied': jobs_applied}
    else:
        redirect('/')
    return render(request, 'Home/view_jobs.html', args)


@login_required
def create_job(request):
    try:
        user = get_user_type(request)
        admin = Admin.objects.get(user_id=request.user.id)
        if user['user_type'] == 'admin':
            if request.method == 'POST':
                job_data = {'job_title': request.POST.get('job_title'),
                            'description': request.POST.get('description'),
                            'description_upload': request.FILES.get('description_upload'),
                            'location': request.POST.get('location'),
                            'job_type_id': request.POST.get('job_type_id'),
                            'industry_id': request.POST.get('industry_id'),
                            'duration_type': request.POST.get('duration_type'),
                            'job_level': request.POST.get('job_level'),
                            'duration': request.POST.get('duration'),
                            'salary_min': request.POST.get('salary_min'),
                            'salary_max': request.POST.get('salary_max'),
                            'skills': request.POST.getlist('skills')
                            }
                employer_data = {'email': request.POST.get('email')}
                company_data = {'logo': request.FILES.get('logo'),
                                'company_name': request.POST.get('company_name'),
                                'company_description': request.POST.get('company_description'),
                                'company_website': request.POST.get('company_website'),
                                'phone_number': request.POST.get('phone_number'),
                                'contact_name': request.POST.get('contact_name'),
                                'trade_license': request.FILES.get('trade_license')
                                }
                jobForm = CreateJobForm(request.POST, request.FILES)
                employerForm = InitialEmployerForm(request.POST)
                companyForm = EmployerForm(request.POST, request.FILES)

                if jobForm.is_valid() and employerForm.is_valid() and companyForm.is_valid():
                    with transaction.atomic():
                        if employerForm.usernameExists():
                            messages.error(request, 'Username already taken. Try a different one.', extra_tags='danger')
                        else:
                            user = employerForm.save()
                            company = companyForm.save(commit=False)
                            company.user = user
                            company.is_active = 'Accepted'
                            company.save()
                            job = jobForm.save(commit=False)
                            print(job.job_level)
                            job.posted_by = Employer.objects.get(user_id=company.user.id)
                            email = company.user
                            job.save()
                            print(job.id)
                            if job.is_active == 'Accepted':
                                find_student_match(job.id)
                                find_alumni_match(job.id)
                            jobForm.save_m2m()

                            first_name = companyForm.cleaned_data.get('company_name')
                            context = {'first_name': first_name}
                            admin_context = {'first_name': first_name, 'protocol': 'https',
                                             'domain': 'murdochdubaicareerportal.com'}

                            subject = 'Your job posting request has been received'
                            htmlText = render_to_string('Employer/job_post_request.html', context)
                            send_html_mail(subject, htmlText, [email])

                            subject = 'A job posting request has been received'
                            htmlText = render_to_string('Home/job_created_admin.html', admin_context)
                            send_html_mail(subject, htmlText, [DEFAULT_FROM_EMAIL])

                            messages.success(request, "Job successfully created")
                            return redirect('view_jobs')

                else:
                    if jobForm.errors:
                        messages.error(request, jobForm.errors, extra_tags='danger')
                    if companyForm.errors:
                        messages.error(request, companyForm.errors, extra_tags='danger')
                    if employerForm.errors:
                        messages.error(request, employerForm.errors, extra_tags='danger')
                    jobForm = CreateJobForm(job_data)
                    employerForm = InitialEmployerForm(employer_data)
                    companyForm = EmployerForm(company_data)
            else:
                jobForm = CreateJobForm()
                employerForm = InitialEmployerForm()
                companyForm = EmployerForm()

            others, created = Skill.objects.get_or_create(skill_name="Others")
            args = {'jobForm': jobForm, 'employerForm': employerForm, 'companyForm': companyForm,
                    'obj': user['obj'], 'user_type': user['user_type'], 'others_id': others.id}
            return render(request, "Home/employer_create_jobs.html", args)
    except Admin.DoesNotExist:
        pass

    try:
        user = get_user_type(request)
        employer = Employer.objects.get(user_id=request.user.id)
        email = str(request.user)
        if user['user_type'] == 'employer':
            if request.method == 'POST':
                job_data = {'job_title': request.POST.get('job_title'),
                            'description': request.POST.get('description'),
                            'description_upload': request.FILES.get('description_upload'),
                            'location': request.POST.get('location'),
                            'job_type_id': request.POST.get('job_type_id'),
                            'industry_id': request.POST.get('industry_id'),
                            'job_level': request.POST.get('job_level'),
                            'duration_type': request.POST.get('duration_type'),
                            'duration': request.POST.get('duration'),
                            'salary_min': request.POST.get('salary_min'),
                            'salary_max': request.POST.get('salary_max'),
                            'skills': request.POST.getlist('skills')
                            }
                form = CreateJobForm(request.POST, request.FILES)
                if form.is_valid():
                    data = form.save(commit=False)
                    data.posted_by = employer
                    data.save()
                    form.save_m2m()

                    first_name = employer.company_name
                    context = {'first_name': first_name}
                    admin_context = {'first_name': first_name, 'protocol': 'https',
                                     'domain': 'murdochdubaicareerportal.com'}

                    subject = 'Your job posting request has been received'
                    htmlText = render_to_string('Employer/job_post_request.html', context)
                    send_html_mail(subject, htmlText, [email])

                    subject = 'A job posting request has been received'
                    htmlText = render_to_string('Home/job_created_admin.html', admin_context)
                    send_html_mail(subject, htmlText, [DEFAULT_FROM_EMAIL])

                    messages.success(request, "Job successfully created")
                    return redirect('view_jobs')
                else:
                    messages.error(request, form.errors, extra_tags='danger')
                    form = CreateJobForm(job_data)
            else:
                form = CreateJobForm()

            others, created = Skill.objects.get_or_create(skill_name="Others")
            args = {'form': form, 'obj': user['obj'], 'user_type': user['user_type'], 'others_id': others.id}
            return render(request, "Home/employer_create_jobs.html", args)
    except Employer.DoesNotExist:
        pass

    return redirect('log_in')


@login_required
def job_details(request, id):
    user = get_user_type(request)
    job = Job.objects.get(id=id)
    companies = Employer.objects.all()
    student_user = get_user(request)

    if user['user_type'] == 'student' or user['user_type'] == 'alumni':
        job_applied = student_user.jobs_applied.all().values_list('id', flat=True)
        args = {'job': job, 'obj': user['obj'], 'user_type': user['user_type'],
                'companies': companies, 'job_applied': job_applied}
    else:
        args = {'job': job, 'obj': user['obj'], 'user_type': user['user_type'],
                'companies': companies}

    form = StudentJobApplicationForm()
    alumniForm = AlumniJobApplicationForm()
    if request.method == 'POST':
        if "apply" in request.POST:
            if user['user_type'] == 'student':
                if job.id not in student_user.jobs_applied.all().values_list('id', flat=True):
                    post = form.save(commit=False)
                    post.job_id = job
                    id = request.user.id
                    student = Student.objects.get(user_id=id)
                    post.applied = student
                    post.date_applied = timezone.now()
                    post.save()
                return render(request, 'Home/job_details.html', args)
            elif user['user_type'] == 'alumni':
                if job.id not in student_user.jobs_applied.all().values_list('id', flat=True):
                    postAlumni = alumniForm.save(commit=False)
                    postAlumni.job_id = job
                    id = request.user.id
                    alumni = Alumni.objects.get(user_id=id)
                    postAlumni.applied = alumni
                    postAlumni.date_applied = timezone.now()
                    postAlumni.save()
                return render(request, 'Home/job_details.html', args)

        elif "viewcandidates" in request.POST:
            alumniCandidates = AlumniJobApplication.objects.filter(job_id=job.id)
            studentCandidates = StudentJobApplication.objects.filter(job_id=job.id)
            args = {'studentCandidates': studentCandidates, 'alumniCandidates': alumniCandidates, 'obj': user['obj'],
                    'user_type': user['user_type']}
            return render(request, 'Home/view_candidates.html', args)

    try:
        if user['user_type'] == 'student':
            student = Student.objects.get(user_id=request.user.id)
            job = Job.objects.get(id=id)
            StudentJobApplication.objects.get(job_id_id=job, applied=student)
        elif user['user_type'] == 'alumni':
            alumni = Alumni.objects.get(user_id=request.user.id)
            job = Job.objects.get(id=id)
            AlumniJobApplication.objects.get(job_id_id=job, applied=alumni)
        return render(request, 'Home/job_details.html', args)

    except:
        if user['user_type'] == 'student' or user['user_type'] == 'alumni':
            job_applied = student_user.jobs_applied.all().values_list('id', flat=True)
            args = {'job': job, 'obj': user['obj'], 'user_type': user['user_type'],
                    'companies': companies, 'job_applied': job_applied}
            return render(request, 'Home/job_details.html', args)
        else:
            args = {'job': job, 'obj': user['obj'], 'user_type': user['user_type'],
                    'companies': companies}
            return render(request, 'Home/job_details.html', args)


@login_required
def edit_job(request, id):
    job = Job.objects.get(id=id)
    job_poster = Employer.objects.get(user_id=job.posted_by_id)
    user = get_user_type(request)
    email = str(request.user)
    try:
        if user['user_type'] == 'employer':
            employer = Employer.objects.get(user_id=request.user.id)
            if request.method == 'POST':
                form = EditJobForm(request.POST, request.FILES, instance=job)
                if form.is_valid():
                    data = form.save(commit=False)
                    data.posted_by = employer
                    data.save()
                    form.save_m2m()
                    next = request.POST.get('next', '/')

                    subject = 'Job Edit Successful'
                    htmlText = 'You have successfully edited your job.'
                    send_html_mail(subject, htmlText, [email])

                    if job.is_active == 'Accepted':
                        find_student_match(id)
                        find_alumni_match(id)

                    return redirect(next)
                else:
                    messages.info(request, form.errors)
                    return redirect(request.path_info)
            else:
                jobForm = EditJobForm(instance=job)
                others, created = Skill.objects.get_or_create(skill_name="Others")
                args = {'job': job, 'jobForm': jobForm, 'obj': user['obj'], 'user_type': user['user_type'],
                        'others_id': others.id}
                return render(request, 'Home/edit_job.html', args)
    except Employer.DoesNotExist:
        pass

    try:
        if user['user_type'] == 'admin':
            admin = Admin.objects.get(user_id=request.user.id)
            if request.method == 'POST':
                jobForm = EditJobForm(request.POST, request.FILES, instance=job)
                companyForm = EditEmployerForm(request.POST, request.FILES, instance=job_poster)

                if jobForm.is_valid() and companyForm.is_valid():
                    # if jobForm.is_valid():
                    with transaction.atomic():
                        company = companyForm.save(commit=False)
                        # company.user_id = admin.user.id
                        company.save()
                        j = jobForm.save(commit=False)
                        j.posted_by = Employer.objects.get(user_id=job_poster.user.id)
                        j.save()
                        jobForm.save_m2m()
                        next_page = request.POST.get('next', '/')

                        subject = 'Job Edit Successful'
                        htmlText = 'You have successfully edited a job.'
                        send_html_mail(subject, htmlText, [email])

                        if job.is_active == 'Accepted':
                            find_student_match(id)
                            find_alumni_match(id)

                        return redirect(next_page)
                else:
                    messages.warning(request, jobForm.errors.as_text)
                    messages.warning(request, companyForm.errors.as_text)
                    return redirect(request.path_info)
            else:
                jobForm = EditJobForm(instance=job)
                companyForm = EditEmployerForm(instance=job_poster)
                others, created = Skill.objects.get_or_create(skill_name="Others")
                args = {'job': job, 'jobForm': jobForm, 'companyForm': companyForm, 'obj': user['obj'],
                        'user_type': user['user_type'], 'others_id': others.id}
                return render(request, 'Home/edit_job.html', args)
    except Admin.DoesNotExist:
        pass

    return redirect('log_in')


@login_required
def my_applications(request):
    user = get_user_type(request)
    if user['user_type'] == 'student':
        jobs_applied = StudentJobApplication.objects.filter(applied_id=user['obj'])
    elif user['user_type'] == 'alumni':
        jobs_applied = AlumniJobApplication.objects.filter(applied_id=user['obj'])
    args = {'jobs_applied': jobs_applied, 'obj': user['obj'], 'user_type': user['user_type']}
    return render(request, 'Home/my_applications.html', args)


@login_required
def reopen_job(request, id):
    user = get_user_type(request)
    job = Job.objects.get(id=id)
    companies = Employer.objects.all()

    args = {'job': job, 'obj': user['obj'], 'user_type': user['user_type'], 'companies': companies, 'applied': True}
    if request.method == 'POST':
        job.status = 'Open'
        job.save()
        messages.success(request, "You have successfully reopened the job")
        return redirect('job_details', job.id)
    else:
        form = EditJobForm()
        return render(request, 'Home/reopen_job.html', args)


@login_required
def delete_job(request, id):
    user = get_user_type(request)
    job = Job.objects.get(id=id)
    companies = Employer.objects.all()
    email = str(request.user)

    args = {'job': job, 'obj': user['obj'], 'user_type': user['user_type'], 'companies': companies, 'applied': True}
    if request.method == 'POST':
        job.status = 'Deleted'
        job.save()

        first_name = job.posted_by.company_name
        context = {'first_name': first_name}

        subject = 'Your job posting has been deleted'
        htmlText = render_to_string('Employer/job_deletion.html', context)
        send_html_mail(subject, htmlText, [email])
        messages.success(request, "You have successfully deleted the job")
        return redirect('view_jobs')
    else:
        form = EditJobForm()
        return render(request, 'Home/delete_job.html', args)


@login_required
def close_job(request, id):
    user = get_user_type(request)
    job = Job.objects.get(id=id)
    companies = Employer.objects.all()
    email = str(request.user)

    args = {'job': job, 'obj': user['obj'], 'user_type': user['user_type'], 'companies': companies, 'applied': True}
    if request.method == 'POST':
        job.status = 'Closed'
        job.date_closed = timezone.now()
        job.save()

        first_name = job.posted_by.company_name
        context = {'first_name': first_name}

        subject = 'Your job posting has been closed'
        htmlText = render_to_string('Employer/job_closing.html', context)
        send_html_mail(subject, htmlText, [email])

        students = Student.objects.filter(jobs_applied=job.id)
        for student in students:
            first_name = student.user.first_name
            context = {'first_name': first_name, 'job_name': job.job_title}
            htmlText = render_to_string('Student/job_closed.html', context)
            subject = 'Job posting has been closed'

            email = str(student.user)
            student_email = str(student.personal_email)
            send_html_mail(subject, htmlText, [email])
            send_html_mail(subject, htmlText, [student_email])

        alumni = Alumni.objects.filter(jobs_applied=job.id)
        for alumnus in alumni:
            first_name = alumnus.user.first_name
            context = {'first_name': first_name, 'job_name': job.job_title}
            htmlText = render_to_string('Student/job_closed.html', context)
            subject = 'Job posting has been closed'

            email = str(alumnus.user)
            send_html_mail(subject, htmlText, [email])

        messages.success(request, "You have successfully closed the job")
        return redirect('job_details', job.id)
    else:
        form = EditJobForm()
        return render(request, 'Home/close_job.html', args)


@login_required
def view_students(request):
    user = get_user_type(request)
    if request.method == 'POST':
        skills = request.POST.get("skills")
        majors = request.POST.get("majors")
        min_graduation_date = request.POST.get('min_graduation_date')
        max_graduation_date = request.POST.get('max_graduation_date')

        if skills:
            skills_students = Student.objects.filter(skills=skills)
        else:
            skills_students = Student.objects.all()

        if min_graduation_date:
            min_graduation_date_students = Student.objects.filter(expected_graduation_date__gte=min_graduation_date)
        else:
            min_graduation_date_students = Student.objects.all()

        if max_graduation_date:
            max_graduation_date_students = Student.objects.filter(expected_graduation_date__lte=max_graduation_date)
        else:
            max_graduation_date_students = Student.objects.all()

        if majors:
            majors_students = Student.objects.filter(majors=majors)
        else:
            majors_students = Student.objects.all()

        filtered_stds = skills_students & majors_students & min_graduation_date_students & max_graduation_date_students
        students_all = Student.objects.filter(is_active="Accepted")
        students = students_all & filtered_stds
        form = FilterStudentForm()
        args = {'students': students, 'form': form, 'obj': user['obj'], 'user_type': user['user_type']}
        return render(request, "Home/view_students.html", args)
    elif user['user_type'] == 'employer' or user['user_type'] == 'admin':
        students = Student.objects.filter(is_active="Accepted")
        users = User.objects.all()
        form = FilterStudentForm()
        args = {'students': students, 'obj': user['obj'], 'user_type': user['user_type'], 'form': form}
    else:
        return redirect('/')
    return render(request, 'Home/view_students.html', args)


@login_required
def view_alumni(request):
    user = get_user_type(request)
    if request.method == 'POST':
        skills = request.POST.get("skills")
        majors = request.POST.get("majors")

        if skills:
            skills_students = Alumni.objects.filter(skills=skills)
        else:
            skills_students = Alumni.objects.all()

        if majors:
            majors_alumni = Alumni.objects.filter(majors=majors)
        else:
            majors_alumni = Alumni.objects.all()

        filtered_stds = skills_students & majors_alumni
        alumni_all = Alumni.objects.filter(is_active="Accepted")
        alumnus = alumni_all & filtered_stds
        form = FilterAlumniForm()
        args = {'alumnus': alumnus, 'form': form, 'obj': user['obj'], 'user_type': user['user_type']}
        return render(request, "Home/view_alumni.html", args)
    elif user['user_type'] == 'employer' or user['user_type'] == 'admin':
        alumnus = Alumni.objects.filter(is_active="Accepted")
        users = User.objects.all()
        form = FilterAlumniForm()
        args = {'alumnus': alumnus, 'obj': user['obj'], 'user_type': user['user_type'], 'form': form}
    else:
        return redirect('/')
    return render(request, 'Home/view_alumni.html', args)


@login_required
def student_details(request, id):
    student = Student.objects.get(user_id=id)
    user = get_user_type(request)
    args = {'student': student, 'obj': user['obj'], 'user_type': user['user_type']}
    return render(request, 'Home/student_details.html', args)


@login_required
def alumni_details(request, id):
    alumni = Alumni.objects.get(user_id=id)
    user = get_user_type(request)
    args = {'alumni': alumni, 'obj': user['obj'], 'user_type': user['user_type']}
    return render(request, 'Home/alumni_details.html', args)


@login_required
def job_to_student_skills(request, id):
    user = get_user_type(request)
    job = Job.objects.get(id=id)
    studentApplicants = Student.objects.filter(skills__in=job.skills.all(), is_active='Accepted')
    studentList = list(set(studentApplicants))
    args = {'studentApplicants': studentList, 'obj': user['obj'], 'user_type': user['user_type']}

    return render(request, "Home/view_student_applicants.html", args)


@login_required
def job_to_alumni_skills(request, id):
    user = get_user_type(request)
    job = Job.objects.get(id=id)
    alumniApplicants = Alumni.objects.filter(skills__in=job.skills.all(), is_active='Accepted')
    alumniList = list(set(alumniApplicants))
    args = {'alumniApplicants': alumniList, 'obj': user['obj'], 'user_type': user['user_type']}

    return render(request, "Home/view_alumni_applicants.html", args)


def find_student_match(job_id):
    try:
        job = Job.objects.get(id=job_id)
        studentApplicants = Student.objects.filter(skills__in=job.skills.all(), is_active='Accepted')
        studentList = list(set(studentApplicants))
        for student in studentList:
            subject = 'We found a match!'
            first_name = student.user.first_name
            context = {'first_name': first_name, 'protocol': 'https', 'domain': 'murdochdubaicareerportal.com', 'job_id': job_id}
            htmlText = render_to_string('Home/found_matching_jobs.html', context)
            email = str(student.user)
            student_email = str(student.personal_email)
            send_html_mail(subject, htmlText, [email])
            send_html_mail(subject, htmlText, [student_email])
    except:
        pass


def find_alumni_match(job_id):
    try:
        job = Job.objects.get(id=job_id)
        alumniApplicants = Alumni.objects.filter(skills__in=job.skills.all(), is_active='Accepted')
        alumniList = list(set(alumniApplicants))
        for alumni in alumniList:
            subject = 'We found a match!'
            first_name = alumni.user.first_name
            context = {'first_name': first_name, 'protocol': 'https', 'domain': 'murdochdubaicareerportal.com', 'job_id': job_id}
            htmlText = render_to_string('Home/found_matching_jobs.html', context)
            email = str(alumni.user)
            send_html_mail(subject, htmlText, [email])
    except:
        pass


@login_required
def get_student_cv_file(request, id):
    student = Student.objects.get(user_id=id)
    cv = student.cv
    file_name = os.path.basename(cv.file.name)

    wrapper = FileWrapper(File(cv, 'rb'))
    response = HttpResponse(wrapper, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + file_name
    return response


@login_required
def get_job_description_file(request, id):
    job = Job.objects.get(id=id)
    job_description = job.description_upload
    file_name = os.path.basename(job_description.file.name)

    wrapper = FileWrapper(File(job_description, 'rb'))
    response = HttpResponse(wrapper, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + file_name
    return response


@login_required
def get_alumni_cv_file(request, id):
    alumni = Alumni.objects.get(user_id=id)
    cv = alumni.cv
    file_name = os.path.basename(cv.file.name)

    wrapper = FileWrapper(File(cv, 'rb'))
    response = HttpResponse(wrapper, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + file_name
    return response


def usernotification(user, notification_string, type_of_notif):
    user_notif = UserNotifications(to_user=user, notification=notification_string, type=type_of_notif, to_show=True)
    user_notif.save()


def seeneach_notification(request):
    id = request.POST['noti_id']
    UserNotifications.objects.filter(id=id).update(to_show=False)
    return None


def seen_notification(request):
    UserNotifications.objects.filter(to_user=request.user).update(to_show=False)
    return None
