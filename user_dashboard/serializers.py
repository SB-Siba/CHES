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

    #coupon validation and calculation
    # def coupon_validation(self, code, amount):
    #     error_dict = {
    #         "valid" : False,
    #         "discount" : "0",
    #         "message": "Invalid Coupon Code"
    #     }
        
    #     try:
    #         coupon_obj = common_models.Coupon.objects.get(code = code)
    #     except:
    #         return error_dict
        
    #     if coupon_obj.quantity < 1 or coupon_obj.active == 'no':
    #         return error_dict
        
    #     if coupon_obj.discount_type == "flat":
    #         discount = coupon_obj.discount_digit
    #         return {
    #         "coupon":code,
    #         "valid" : True,
    #         "discount" : discount,
    #         "message": f"{code} : is applied successfully"
    #         }
    #     elif coupon_obj.discount_type == "pencentage":
    #         discount = round(amount*(coupon_obj.discount_digit/100),2)
    #         return {
    #             "coupon":code,
    #             "valid" : True,
    #             "discount" : discount,
    #             "message": f"{code} : is applied successfully"
    #         }
    #     else:
    #         return error_dict

    def get_products_data(self,obj):
        total_items = 1
        total_value = 0
        charges = {}
        gross_value = 0 #market price or product_max_price
        our_price = 0
        final_payable_amount =0


        products = {}
        product_list = []

        try:
            product = get_object_or_404(models.ProductFromVendor,id = obj.id)
            gross_value += float(product.max_price)
            #____________
            product_discounted__price = float(product.discount_price)
            our_price = product_discounted__price
            price = product.discount_price

            x = {}
            
            x['quantity'] = 1
            x['price_per_unit'] = float(price)
            x['total_price'] = float(price)

            products[product.name] = x
            #______________

            
        except Exception as e:
            print(e)
        discount_amount = gross_value - our_price
        result = {
            'products':products,
            'total_items':total_items,
            'gross_value': gross_value,
            'our_price':our_price,
            'discount_amount':discount_amount,
            'discount_percentage': round((discount_amount/gross_value)*100,1),
            'charges':charges,
        }

        # calculating final amount by adding the charges
        final_value = float(our_price)
        if len(charges) > 0:
            for key, value in charges.items():
                final_value += value
        
        #checking is coupon service is on or not
        # result['coupon_enable'] = settings.COUPON_ENABLE

        result['final_value'] = final_value

        #CALCULATE charges -------------------------------------------------

        # GST
        if settings.GST_CHARGE > 0:
            gst_value = final_value * float(settings.GST_CHARGE)
            charges['GST'] = '{:.2f}'.format(gst_value)
        else:
            charges['GST']=0
        
        #delivary
        if result['final_value'] < settings.DELIVARY_FREE_ORDER_AMOUNT:
            delevery_charge = total_items * float(settings.DELIVARY_CHARGE_PER_BAG)
            charges['Delivary'] = '{:.2f}'.format(delevery_charge)
        else:
            charges['Delivary']= 0

        for key, value in charges.items():
            final_value += float(value)

        #modifing coupon data
        if settings.COUPON_ENABLE and self.coupon:
            cuopon_validation_response= self.coupon_validation(self.coupon, final_value)
            result['cuopon_validation_result']=cuopon_validation_response

            if cuopon_validation_response['valid'] == True:
                result['final_value'] -= cuopon_validation_response['discount']

        result['final_value'] = float(final_value)

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