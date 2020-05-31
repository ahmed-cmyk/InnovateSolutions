from datetime import datetime, date

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib import messages
from django_comments.models import Comment
from Accounts.views import get_user_type
from .models import HelpDeskModel
from .forms import HelpDeskForm
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.mail import send_mail
from DjangoUnlimited.settings import SENDGRID_API_KEY


class HelpDeskFormView(TemplateView):
    template_name = 'HelpDesk/Report_issue.html'
    def get(self, request, *args, **kwargs):
        user = get_user_type(request)
        if kwargs:
            pk = kwargs['pk']  # get a particular instance of the IT Support Form filled previously
            help_desk_form = HelpDeskForm(instance=HelpDeskModel.objects.get(id=pk))
            help_desk_form.fields['subject'].disabled = True  # the subject field cannot be edited once submitted
            help_desk_form.fields['issue'].disabled = True  # the issue field cannot be edited once submitted
        else:
            help_desk_form = HelpDeskForm()  # get a new form if a previous one does not exist

        try:
            thread = HelpDeskModel.objects.get(id=pk)
        except:
            thread = []

        args = {
            'help_desk_form': help_desk_form,
            'thread': thread,
            'user_type': user['user_type'],
            'obj': user['obj']
        }

        return render(request, self.template_name, args)

    # Create a comment thread
    def post(self, request, *args, **kwargs):
        form = HelpDeskForm(request.POST)

        if kwargs:
            pk = kwargs['pk']
            requesteduser = HelpDeskModel.objects.get(id=pk).name_Request.id
            content = ContentType.objects.get_for_model(HelpDeskModel)
            current_site = get_current_site(request)
            # Add a comment to the issue thread
            create_first_note = Comment(
                content_type=content,
                object_pk=request.POST['object_pk'],
                site=current_site,
                user=request.user,
                user_name=request.user.get_full_name(),
                user_email=request.user.email,
                user_url='http://dummyurl.com',
                comment=request.POST['comment'],
                submit_date=datetime.now(),
                ip_address='127.0.0.1',
            )
            create_first_note.save()

            return redirect('HelpDesk', pk)
        else:
            if form.is_valid():
                f = form.save(commit=False)
                f.name_Request = request.user
                f.save()
                message = Mail(
                    from_email='info@murdochcareerportal.com',
                    to_emails=['ict302jan2020@gmail.com'],
                    subject='HelpDesk Request',
                    html_content="A new helpdesk complaint has been filed by."
                )
                sg = SendGridAPIClient(SENDGRID_API_KEY)
             #   sg.send(message)
                messages.success(request, "Your request has been submitted.")
                return redirect('HelpDesk', f.id)


# Admin view of HelpDesk Requests
class HelpDeskRequests(TemplateView):
    template_name = 'HelpDesk/Admin_List_of_Requests.html'

    def get(self, request, *args, **kwargs):
        c = HelpDeskModel.objects.all().order_by("-completed_date")
        user = get_user_type(request)
        args = {
            'reqs': c,
            'user_type': user['user_type'],
            'obj': user['obj']
        }
        print (c)

        return render(request, 'HelpDesk/Admin_List_of_Requests.html', args)


# Each User's own view of their own requests
class MyHelpDeskRequests(TemplateView):
    template_name = 'HelpDesk/my_helpdesk_requests.html'

    def get(self, request, *args, **kwargs):
        c = HelpDeskModel.objects.filter(name_Request=request.user.id)
        pending_requests = HelpDeskModel.objects.filter(name_Request=request.user.id).order_by("completed")
        user = get_user_type(request)
        return render(request, 'HelpDesk/my_helpdesk_requests.html',
                      {'helpdeskRequests': pending_requests,
                       'user_type': user['user_type'],
                       'obj': user['obj']
                       })