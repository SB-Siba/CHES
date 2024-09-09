from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings
from app_common import models as common_models
from django.utils.decorators import method_decorator
from django.db.models import Q
from helpers import utils
from django.db.models import Count
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from Blogs.models import Blogs

app = "admin_dashboard/"

@method_decorator(utils.super_admin_only, name='dispatch')
class AdminDashboard(View):
    template = app + "index.html"

    def get(self, request):
        not_approvedlist = common_models.User.objects.filter(is_approved=False).order_by('-id')
        not_approvedlist_rtg = common_models.User.objects.filter(is_approved=False,is_rtg = True).order_by('-id')
        not_approvedlist_vendor = common_models.User.objects.filter(is_approved=False,is_vendor = True).order_by('-id')
        not_approvedlist_service_provider = common_models.User.objects.filter(is_approved=False,is_serviceprovider = True).order_by('-id')

        profile_update_obj = common_models.GardeningProfileUpdateRequest.objects.all()
        activity_request_obj = common_models.UserActivity.objects.filter(is_accepted='pending').order_by('-date_time')
        gardener_sell_request_obj = common_models.SellProduce.objects.filter(is_approved='pending').order_by('-date_time')

        total_rt_gardeners = common_models.User.objects.filter(is_rtg = True,is_approved = True).count()
        total_vendors = common_models.User.objects.filter(is_vendor = True,is_approved = True).count()
        total_service_provider = common_models.User.objects.filter(is_serviceprovider = True,is_approved = True).count()
        total_activities = common_models.UserActivity.objects.all().count()
        rtg_garden_profile = common_models.GardeningProfile.objects.all()
        rtg_total_garden_area = sum([i.garden_area for i in rtg_garden_profile])
        rtg_total_plants = sum([i.number_of_plants for i in rtg_garden_profile])

        bhubaneswar_rtg = common_models.User.objects.filter(is_rtg = True,is_approved = True,city = "Bhubaneswar").count()
        cuttack_rtg = common_models.User.objects.filter(is_rtg = True,is_approved = True,city = "Cuttack").count()
        brahmapur_rtg = common_models.User.objects.filter(is_rtg = True,is_approved = True,city = "Brahmapur").count()
        sambalpur_rtg = common_models.User.objects.filter(is_rtg = True,is_approved = True,city = "Sambalpur").count()
        jaipur_rtg = common_models.User.objects.filter(is_rtg = True,is_approved = True,city = "Jaipur").count()
        other_cities_rtg = common_models.User.objects.filter(is_rtg=True,is_approved = True).exclude(Q(city="Bhubaneswar") | Q(city="Cuttack") | Q(city="Brahmapur") | Q(city="Sambalpur") | Q(city="Jaipur")).count()

        bhubaneswar_vendor = common_models.User.objects.filter(is_vendor = True,is_approved = True,city = "Bhubaneswar").count()
        cuttack_vendor = common_models.User.objects.filter(is_vendor = True,is_approved = True,city = "Cuttack").count()
        brahmapur_vendor = common_models.User.objects.filter(is_vendor = True,is_approved = True,city = "Brahmapur").count()
        sambalpur_vendor = common_models.User.objects.filter(is_vendor = True,is_approved = True,city = "Sambalpur").count()
        jaipur_vendor = common_models.User.objects.filter(is_vendor = True,is_approved = True,city = "Jaipur").count()
        other_cities_vendor = common_models.User.objects.filter(is_vendor=True,is_approved = True).exclude(Q(city="Bhubaneswar") | Q(city="Cuttack") | Q(city="Brahmapur") | Q(city="Sambalpur") | Q(city="Jaipur")).count()

        bhubaneswar_serviceprovider = common_models.User.objects.filter(is_serviceprovider = True,is_approved = True,city = "Bhubaneswar").count()
        cuttack_serviceprovider = common_models.User.objects.filter(is_serviceprovider = True,is_approved = True,city = "Cuttack").count()
        brahmapur_serviceprovider = common_models.User.objects.filter(is_serviceprovider = True,is_approved = True,city = "Brahmapur").count()
        sambalpur_serviceprovider = common_models.User.objects.filter(is_serviceprovider = True,is_approved = True,city = "Sambalpur").count()
        jaipur_serviceprovider = common_models.User.objects.filter(is_serviceprovider = True,is_approved = True,city = "Jaipur").count()
        other_cities_serviceprovider = common_models.User.objects.filter(is_serviceprovider=True,is_approved = True).exclude(Q(city="Bhubaneswar") | Q(city="Cuttack") | Q(city="Brahmapur") | Q(city="Sambalpur") | Q(city="Jaipur")).count()

        # Define your default 5 cities
        default_cities = ["Bhubaneswar", "Cuttack", "Jaipur", "Brahmapur", "Sambalpur"]

        # Query the database for city-wise data
        city_data = common_models.User.objects.values('city').annotate(total=Count('city'))

        # Initialize the data structure
        city_counts = {city: 0 for city in default_cities}
        other_count = 0

        # Categorize city data
        for data in city_data:
            city_name = data['city']
            if city_name in default_cities:
                city_counts[city_name] = data['total']
            else:
                other_count += data['total']

        # Add 'Other' category
        city_counts["Other"] = other_count

        # Prepare labels and data for the chart
        labels = list(city_counts.keys())
        chart_data = list(city_counts.values())

        all_users = common_models.User.objects.filter(is_approved = True).exclude(is_superuser = True)
        user_activity_totals = (
            common_models.UserActivity.objects
            .filter(user__in=all_users)
            .values('user')
            .annotate(total_activity=Count('id'))
            .order_by('-total_activity')
        )

        # Get top 5 users based on total activity
        top_users = user_activity_totals[:5]
        activity_data = [entry['total_activity'] for entry in top_users]
        activity_label = [
            common_models.User.objects.get(id=entry['user']).full_name
            for entry in top_users
        ]

        top_users_by_coins = common_models.User.objects.filter(coins__gt=0).order_by('-coins')[:10]
        positions = [
            'winner', 'first_runner_up', 'second_runner_up', 'third', 'fourth',
            'fifth', 'sixth', 'seventh', 'eighth', 'ninth'
        ]

        leaderboard = {
            position: top_users_by_coins[i] if i < len(top_users_by_coins) else None
            for i, position in enumerate(positions)
        }

        context = {
            'not_approvedlist': not_approvedlist,
            'not_approvedlist_rtg': not_approvedlist_rtg,
            'not_approvedlist_vendor': not_approvedlist_vendor,
            'not_approvedlist_service_provider': not_approvedlist_service_provider,
            'profile_update_obj': profile_update_obj,
            'activity_request_obj': activity_request_obj,
            'gardener_sell_request_obj': gardener_sell_request_obj,
            'total_rt_gardeners': total_rt_gardeners,
            'total_vendors': total_vendors,
            'total_service_provider': total_service_provider,
            'total_activities': total_activities,
            'rtg_total_garden_area': rtg_total_garden_area,
            'rtg_total_plants': rtg_total_plants,
            'bhubaneswar_rtg': bhubaneswar_rtg,
            'cuttack_rtg': cuttack_rtg,
            'brahmapur_rtg': brahmapur_rtg,
            'sambalpur_rtg': sambalpur_rtg,
            'jaipur_rtg': jaipur_rtg,
            'other_cities_rtg': other_cities_rtg,
            'bhubaneswar_vendor': bhubaneswar_vendor,
            'cuttack_vendor': cuttack_vendor,
            'brahmapur_vendor': brahmapur_vendor,
            'sambalpur_vendor': sambalpur_vendor,
            'jaipur_vendor': jaipur_vendor,
            'other_cities_vendor': other_cities_vendor,
            'bhubaneswar_serviceprovider': bhubaneswar_serviceprovider,
            'cuttack_serviceprovider': cuttack_serviceprovider,
            'brahmapur_serviceprovider': brahmapur_serviceprovider,
            'sambalpur_serviceprovider': sambalpur_serviceprovider,
            'jaipur_serviceprovider': jaipur_serviceprovider,
            'other_cities_serviceprovider': other_cities_serviceprovider,
            'labels': labels,
            'chart_data': chart_data,
            'activity_data':activity_data,
            'activity_label':activity_label,
            'leaderboard':leaderboard,
        }

        return render(request, self.template, context)

class CityDetailView(View):
    template_name = app + "city_detail.html"

    def get(self, request, *args, **kwargs):
        city_name = self.kwargs.get('city_name')

        # Define the default cities
        default_cities = ["Bhubaneswar", "Cuttack", "Jaipur", "Brahmapur", "Sambalpur"]

        if city_name == "Other":
            # Filter users from cities not in the default list
            rtgs = common_models.User.objects.filter(is_rtg=True).exclude(city__in=default_cities)
            vendors = common_models.User.objects.filter(is_vendor=True).exclude(city__in=default_cities)
            service_providers = common_models.User.objects.filter(is_serviceprovider=True).exclude(city__in=default_cities)
            
            # Aggregate data for all non-default cities
            total_users = common_models.User.objects.filter(city__in=default_cities).count()

            rtgs_and_vendors = common_models.User.objects.filter(Q(is_rtg=True) | Q(is_vendor=True)).exclude(city__in=default_cities)

            activity_label = []
            activity_data = []
            rtg_sales_label = []
            rtg_sales_data = []
            vendor_sales_label = []
            vendor_sales_data = []

            # Calculate total activity for all time
            user_activity_totals = (
                common_models.UserActivity.objects
                .filter(user__in=rtgs_and_vendors)
                .values('user')
                .annotate(total_activity=Count('id'))
                .order_by('-total_activity')
            )

            # Get top 5 users based on total activity
            top_users = user_activity_totals[:5]
            activity_data = [entry['total_activity'] for entry in top_users]
            activity_label = [
                common_models.User.objects.get(id=entry['user']).full_name
                for entry in top_users
            ]

            # Calculate sales data for RTGs
            for rtg in rtgs:
                total_amount = common_models.ProduceBuy.objects.filter(seller=rtg).aggregate(
                    total_amount=Sum('ammount_based_on_quantity_buyer_want')
                )['total_amount'] or 0
                rtg_sales_data.append(total_amount)
                rtg_sales_label.append(rtg.full_name)

            # Get top 5 RTG sales
            top_rtg_sales = sorted(zip(rtg_sales_data, rtg_sales_label), reverse=True)[:5]
            top_sales_data = [data for data, _ in top_rtg_sales]
            top_sales_label = [label for _, label in top_rtg_sales]

            # Calculate sales data for vendors
            for vendor in vendors:
                total_amount = common_models.Order.objects.filter(vendor=vendor).aggregate(
                    total_amount=Sum('order_value')
                )['total_amount'] or 0
                vendor_sales_data.append(total_amount)
                vendor_sales_label.append(vendor.full_name)

            # Get top 5 Vendor sales
            top_vendor_sales = sorted(zip(vendor_sales_data, vendor_sales_label), reverse=True)[:5]
            vendor_top_sales_data = [data for data, _ in top_vendor_sales]
            vendor_top_sales_label = [label for _, label in top_vendor_sales]

            # Prepare graph data
            graph_data = {
                'activity_label': activity_label,
                'activity_data': activity_data,
                'rtg_sales_data': top_sales_data,
                'rtg_sales_label': top_sales_label,
                'vendor_sales_data': vendor_top_sales_data,
                'vendor_sales_label': vendor_top_sales_label,
            }

            labels = ['RTGs', 'Vendors', 'Service Providers']
            chart_data = [rtgs.count(), vendors.count(), service_providers.count()]

        else:
            # For specific cities, use the city_name
            rtgs = common_models.User.objects.filter(is_rtg=True, city=city_name)
            vendors = common_models.User.objects.filter(is_vendor=True, city=city_name)
            service_providers = common_models.User.objects.filter(is_serviceprovider=True, city=city_name)
            
            total_users = common_models.User.objects.filter(city=city_name).count()

            rtgs_and_vendors = common_models.User.objects.filter(
                Q(is_rtg=True) | Q(is_vendor=True),
                city=city_name
            )

            activity_label = []
            activity_data = []
            rtg_vendor_sales_data = []
            rtg_vendor_sales_label = []
            vendor_sales_label = []
            vendor_sales_data = []

            # Calculate total activity for all time
            user_activity_totals = (
                common_models.UserActivity.objects
                .filter(user__in=rtgs_and_vendors)
                .values('user')
                .annotate(total_activity=Count('id'))
                .order_by('-total_activity')
            )

            # Get top 5 users based on total activity
            top_users = user_activity_totals[:5]
            activity_data = [entry['total_activity'] for entry in top_users]
            activity_label = [
                common_models.User.objects.get(id=entry['user']).full_name
                for entry in top_users
            ]

            # Calculate sales data for RTGs
            for rtgandvendor in rtgs_and_vendors:
                total_amount = common_models.ProduceBuy.objects.filter(seller=rtgandvendor).aggregate(
                    total_amount=Sum('ammount_based_on_quantity_buyer_want')
                )['total_amount'] or 0
                rtg_vendor_sales_data.append(total_amount)
                rtg_vendor_sales_label.append(rtgandvendor.full_name)

            # Get top 5 RTG sales
            top_rtg_vendor_sales = sorted(zip(rtg_vendor_sales_data, rtg_vendor_sales_label), reverse=True)[:5]
            top_sales_data = [data for data, _ in top_rtg_vendor_sales]
            top_sales_label = [label for _, label in top_rtg_vendor_sales]

            # Calculate sales data for vendors
            for vendor in vendors:
                total_amount = common_models.Order.objects.filter(vendor=vendor).aggregate(
                    total_amount=Sum('order_value')
                )['total_amount'] or 0
                vendor_sales_data.append(total_amount)
                vendor_sales_label.append(vendor.full_name)

            # Get top 5 Vendor sales
            top_vendor_sales = sorted(zip(vendor_sales_data, vendor_sales_label), reverse=True)[:5]
            vendor_top_sales_data = [data for data, _ in top_vendor_sales]
            vendor_top_sales_label = [label for _, label in top_vendor_sales]

            # Prepare graph data
            graph_data = {
                'activity_label': activity_label,
                'activity_data': activity_data,
                'rtg_vendor_sales_data': top_sales_data,
                'rtg_vendor_sales_label': top_sales_label,
                'vendor_sales_data': vendor_top_sales_data,
                'vendor_sales_label': vendor_top_sales_label,
            }
            print(graph_data)
            labels = ['RTGs', 'Vendors', 'Service Providers']
            chart_data = [rtgs.count(), vendors.count(), service_providers.count()]
        # Pass data to template
        context = {
            'city_name': city_name,
            'rtgs': rtgs,
            'vendors': vendors,
            'service_providers': service_providers,
            'total_users': total_users,
            'graph_data': graph_data,
            'labels': labels,
            'chart_data': chart_data
        }
        return render(request, self.template_name, context)