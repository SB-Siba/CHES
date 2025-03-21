from app_common.models import Booking

def service_provider_data(request):
    # Count the total bookings for the logged-in service provider
    total_bookings_count = Booking.objects.filter(service_provider=request.user).count()  # Adjust the filter as per your logic

    return {
        'total_bookings_count': total_bookings_count
    }
