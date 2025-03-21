from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from helpers import utils
from django.forms.models import model_to_dict

from helpers import utils
from app_common import models as common_model
from app_common.error import render_error_page
from user_dashboard.serializers import OrderSerializer
from .forms import OrderUpdateForm, ProduceOrderUpdateForm
from ..tasks import update_order_status
from django.utils.decorators import method_decorator
from helpers import utils
from helpers.utils import login_required

app = "admin_dashboard/orders/"

# ================================================== patient management ==========================================
        
@method_decorator(utils.super_admin_only, name='dispatch')
class ProduceOrderList(View):
    model = common_model.ProduceBuy
    template = app + "order_list.html"

    def get(self, request):
        try:
            order_list = self.model.objects.all().order_by('-id')
            paginated_data = utils.paginate(request, order_list, 50)
            order_status_options = common_model.ProduceBuy.BUYINGSTATUS
            context = {
                "order_list": paginated_data,
                "order_status_options": order_status_options,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.super_admin_only, name='dispatch')
class ProduceOrderSearch(View):
    model = common_model.ProduceBuy
    template = app + "order_list.html"

    def get(self, request):
        try:
            query = request.GET.get('query')
            order_list = self.model.objects.filter(id__icontains=query)
            context = {
                "order_list": order_list,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)


@method_decorator(utils.super_admin_only, name='dispatch')
class ProduceOrderStatusSearch(View):
    model = common_model.ProduceBuy
    template = app + "order_list.html"

    def get(self, request):
        try:
            filter_by = request.GET.get('filter_by')
            order_list = self.model.objects.filter(buying_status=filter_by)
            paginated_data = utils.paginate(request, order_list, 50)
            order_status_options = common_model.ProduceBuy.BUYINGSTATUS
            context = {
                "order_list": paginated_data,
                "order_status_options": order_status_options,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

    
@method_decorator(utils.super_admin_only, name='dispatch')
class ProduceOrderDetail(View):
    model = common_model.ProduceBuy
    form_class = ProduceOrderUpdateForm
    template = app + "order_detail.html"

    def get(self, request, order_id):
        try:
            order = self.model.objects.get(id=order_id)
            context = {
                'order': order,
                'form': ProduceOrderUpdateForm(instance=order)
            }
            return render(request, self.template, context)
        except self.model.DoesNotExist:
            messages.error(request, 'Order does not exist.')
            return redirect('admin_dashboard:produce_order_list')
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

    def post(self, request, order_id):
        try:
            order = self.model.objects.get(id=order_id)
            form = self.form_class(request.POST, instance=order)

            if form.is_valid():
                obj = form.save()
                # update_order_status.delay(obj.user.email, OrderSerializer(obj).data)
                messages.success(request, 'Order Status is updated....')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')

            return redirect('admin_dashboard:produce_order_detail', order_id=order_id)
        except self.model.DoesNotExist:
            messages.error(request, 'Order does not exist.')
            return redirect('admin_dashboard:produce_order_list')
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

    
@method_decorator(utils.super_admin_only, name='dispatch')
class DownloadProduceOrderInvoice(View):
    model = common_model.ProduceBuy
    form_class = ProduceOrderUpdateForm
    template = app + "produce_order_invoice.html"

    def get(self, request, order_id):
        try:
            order = self.model.objects.get(id=order_id)
            context = {
                'order': order,
            }
            return render(request, self.template, context)
        except self.model.DoesNotExist:
            messages.error(request, 'Order does not exist.')
            return redirect('admin_dashboard:produce_order_list')
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
