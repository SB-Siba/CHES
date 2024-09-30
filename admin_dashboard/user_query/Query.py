from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings
from EmailIntigration.views import send_template_email
from helpers import utils
from app_common import models
from app_common.error import render_error_page
from . import form
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

app = "admin_dashboard/user_query/"


@method_decorator(utils.super_admin_only, name='dispatch')
class UsersQueryList(View):
    model = models.User_Query
    form_class = form.UserQueryReply
    template = app + "query_list.html"

    def get(self, request):
        try:
            query_list = self.model.objects.all().order_by('-id')
            paginated_data = utils.paginate(request, query_list, 50)

            context = {
                "message_list": paginated_data,
                "form": self.form_class(),
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.super_admin_only, name='dispatch')
class QueryReply(View):
    model = models.User_Query
    form_class = form.UserQueryReply

    def post(self, request, id):
        # Fetch the message object using the id
        message = get_object_or_404(self.model, id=id)

        # Bind form with POST data and instance of the message
        form = self.form_class(request.POST, instance=message)

        if form.is_valid():
            # Save the form without committing immediately
            obj = form.save(commit=False)

            # Only set is_solved to True if the user checked the box
            obj.is_solve = form.cleaned_data.get('is_solve', False)  # This assumes 'is_solve' is a checkbox in your form

            # Save the modified instance
            obj.save()

            # Send email notification
            send_template_email(
                subject="Reply To Your Query",
                template_name="mail_template/query_reply.html",
                context={
                    'full_name': obj.full_name,
                    "email": obj.email,
                    'reply': obj.reply,
                    'message': obj.message
                },
                recipient_list=[obj.email]
            )
            return redirect('admin_dashboard:users_query_list')

        else:
            error_list = [f'{field}: {error}' for field, errors in form.errors.items() for error in errors]
            error_message =  f"Errors occurred: {', '.join(error_list)}"
            return render_error_page(request, error_message, status_code=400)
        
@method_decorator(utils.super_admin_only, name='dispatch')
class DeleteQuery(View):
    model = models.User_Query

    def get(self,request,id):
        message = get_object_or_404(self.model, id=id)
        message.delete()
        return redirect('admin_dashboard:users_query_list')



