from rest_framework import serializers
from app_common import models
from django.conf import settings
from django.shortcuts import get_object_or_404

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['full_name', 'email', 'password', 'confirm_password', 'contact', 'city']

class GardeningDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GardeningProfile
        fields = ['garden_area', 'number_of_plants', 'number_of_unique_plants', 'garden_image']

class GardenQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GaredenQuizModel
        fields = ['user', 'questionANDanswer']

# ----------------------------------------------------------------------
class DirectBuySerializer(serializers.ModelSerializer):
    products_data = serializers.SerializerMethodField()

    def __init__(self, *args, user_has_subscription=False, **kwargs):
        self.user_has_subscription = user_has_subscription
        self.coupon = kwargs.pop('coupon', None)
        super().__init__(*args, **kwargs)

    def get_products_data(self, obj):
        total_items = 1
        total_value = 0
        charges = {}
        gross_value = 0  # market price or product_max_price
        our_product_value = 0  # market price or product_max_price

        our_price = 0
        final_payable_amount = 0

        products = {}
        product_list = []
        coin_exchange = 0
        try:
            product = get_object_or_404(models.ProductFromVendor, id=obj.id)
            gross_value += float(product.max_price)
            our_product_value = float(product.discount_price)
            x = {}
            # ____________
            if self.context.get('offer_discount') == "1":
                discount_percentage = float(product.discount_percentage)
                product_discounted_price = float(f"{float(product.discount_price) * (1 - (discount_percentage / 100)):.2f}")
                our_price = product_discounted_price
                x['quantity'] = 1
                x['price_per_unit'] = f"{float(product.discount_price):.2f}"
                x['our_price'] = f"{float(product.discount_price):.2f}"
                x['total_price'] = f"{our_price:.2f}"
                x["coinexchange"] = f"{float(product.green_coins_required):.2f}" if product.green_coins_required is not None else "0.00"
                x["forpercentage"] = f"{discount_percentage:.2f}"
                x["taxable_price"] = f"{product.taxable_price:.2f}"
                x["gst"] = f"{product.gst_rate:.2f}"
                x["cgst"] = f"{product.cgst:.2f}"
                x["sgst"] = f"{product.sgst:.2f}"
                x["product_id"] = f"{product.id}"
                coin_exchange = product.green_coins_required if product.green_coins_required is not None else 0
            else:
                product_discounted_price = float(product.discount_price)
                our_price = product_discounted_price
                x['quantity'] = 1
                x['price_per_unit'] = f"{float(product.discount_price):.2f}"
                x['our_price'] = f"{our_price:.2f}"
                x['total_price'] = f"{our_price:.2f}"
                x["coinexchange"] = "0.00"
                x["forpercentage"] = None
                x["taxable_price"] = f"{product.taxable_price:.2f}"
                x["gst"] = f"{product.gst_rate:.2f}"
                x["cgst"] = f"{product.cgst:.2f}"
                x["sgst"] = f"{product.sgst:.2f}"
                coin_exchange = 0

            products[product.name] = x

        except Exception as e:
            print(e)

        discount_amount = gross_value - our_price
        discount_percentage = (discount_amount / gross_value) * 100 if gross_value > 0 else 0
        result = {
            'products': products,
            'total_items': total_items,
            'gross_value': f"{gross_value:.2f}",
            'our_product_value': f"{our_product_value:.2f}",
            'our_price': f"{our_price:.2f}",
            'discount_amount': f"{discount_amount:.2f}",
            'discount_percentage': f"{round(discount_percentage, 1):.2f}",
            'charges': charges,
            'coin_exchange': f"{float(coin_exchange):.2f}"  # Show actual amount if coin_exchange is true, otherwise 0
        }

        # calculating final amount by adding the charges
        final_value = our_price
        if len(charges) > 0:
            for key, value in charges.items():
                final_value += float(value)

        # delivery
        if final_value < settings.DELIVARY_FREE_ORDER_AMOUNT:
            delivery_charge = total_items * float(settings.DELIVARY_CHARGE_PER_BAG)
            charges['Delivery'] = f"{delivery_charge:.2f}"
        else:
            charges['Delivery'] = "0.00"

        for key, value in charges.items():
            final_value += float(value)

        result['final_value'] = f"{final_value:.2f}"

        return result

    class Meta:
        model = models.ProductFromVendor
        fields = [
            "products_data",
        ]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = '__all__'


class DirectServiceSerializer(serializers.ModelSerializer):
    service_data = serializers.SerializerMethodField()

    def get_service_data(self, obj):
        gross_value = float(obj.price_per_hour)
        discount_percentage = float(obj.discount_percentage_for_greencoins)
        discounted_price = gross_value * (1 - (discount_percentage / 100))
        green_points_required = obj.green_coins_required
        coin_exchange = False

        # Apply offer discount if applicable
        if self.context.get('offer_discount') == "1":
            coin_exchange = True

        final_value = discounted_price if coin_exchange else gross_value
        discount_amount = gross_value - final_value

        return {
            'service_name': obj.provider.full_name,
            'gross_value': f"{gross_value:.2f}",
            'final_value': f"{final_value:.2f}",
            'discount_amount': f"{discount_amount:.2f}",
            'discount_percentage': f"{discount_percentage:.2f}",
            'green_points_required': f"{green_points_required:.2f}",
            'coin_exchange': coin_exchange,
        }

    class Meta:
        model = models.Service
        fields = ['service_data']