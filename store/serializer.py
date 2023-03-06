from rest_framework import serializers
from . models import *
from decimal import Decimal
from django.db import transaction
from .signals import order_created
from main.functions import get_auto_id, password_generater
import pdb

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source ='category.name',read_only=True)
    class Meta:
        model= Product
        fields = ['id','name','image','category','price','offer_price','offer_in_percentage','unit','category_name','last_update']
    

    offer_price = serializers.SerializerMethodField(method_name='calculate_final_price')
    
    def calculate_final_price(self,product:Product):
        final= product.price * int(product.offer_in_percentage)/ Decimal(100)
        return product.price - final
 

class ReviewSerializer(serializers.ModelSerializer):
    class  Meta:
        model=Review
        fields =['name','description','product']

# class CustomerSerializer(serializers.ModelSerializer):

#     user_id = serializers.IntegerField(read_only=True)


#     class Meta:
#         model = Customer
#         fields = ['id','user_id','phone','birth_date']

class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "username",
            "phone",
            "email"
        ]

        def create(self, validated_data):
            password = password_generater(8)
            validated_data["password"] = password
            validated_data["password2"] = password

            account_serializer = CustomerUserSerializer(data=validated_data)
            if account_serializer.is_valid():
                account = account_serializer.save()

            return account

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields =['id','name','product_count','image']
    
    product_count = serializers.IntegerField(read_only = True)

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id','name','image']


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','price','offer_in_percentage','offer_price']
    offer_price = serializers.SerializerMethodField(method_name='calculate_final_price')
    def calculate_final_price(self,product:Product):
        final= product.price * int(product.offer_in_percentage)/ Decimal(100)
        return product.price - final
    


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'items']

# class CartItemSerializer(serializers.ModelSerializer):
#     product =  SimpleProductSerializer()
#     total_price = serializers.SerializerMethodField()

#     def get_total_price(self,cart_item:CartItem):
#         return cart_item.quantity * cart_item.product.offer_price
        
#     class Meta:
#         model=CartItem
#         fields = ['id','product','quantity','total_price']


# class CartSerializer(serializers.ModelSerializer):
#     # id = serializers.UUIDField(read_only = True)
#     items = CartItemSerializer(many=True,read_only=True)
#     total_price = serializers.SerializerMethodField()
#     id=serializers.UUIDField(read_only=True)
#     account_view =CustomerUserSerializer(read_only=True, source="account")

#     def get_total_price(self,cart):
#         return sum([item.quantity * item.product.offer_price for item in cart.items.all()])

#     class Meta:
#         model = Cart
#         fields = ['id','items','total_price',"account_view",'account']


# class AddCartSerializer(serializers.ModelSerializer):
#     # product_id = serializers.IntegerField(write_only=True)
#     # product_id = serializers.CharField(source="product", read_only=True)
#     # product = serializers.SerializerMethodField(read_only=True)

#     # def get_product(self, obj):
#     #     product = Product.objects.get(pk=obj.product_id)
#     #     return ProductSerializer(product).data
    
#     def validate_product_id(self,value):
#         if not Product.objects.filter(pk=value).exists():
#             raise serializers.ValidationError('No product with given ID was found.')
#         return value 
#     def save(self, **kwargs):
#         cart_id = self.context['cart_id']
#         product_id = self.context['product_id']
#         quantity = self.validated_data['quantity']
# # ,product_id=product
#         try:
#             cart_item = CartItem.objects.get(cart_id=cart_id,product_id=product_id)
#             cart_item.quantity += quantity
#             cart_item.save()
#             self.instance = cart_item
#         except CartItem.DoesNotExist:
#             self.instance = CartItem.objects.create(cart_id=cart_id,**self._validated_data)
        
#         return self.instance

#     class Meta:
#         model = CartItem
#         fields =['id','product','quantity']


# class AddCartSerializer(serializers.ModelSerializer):
#     # pdb.set_trace()
#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('context')['request']
#         super().__init__(*args, **kwargs)

#     def validate_cart_id(self, value):
#         if not Cart.objects.filter(pk=value).exists():
#             raise serializers.ValidationError('No cart with given ID was found.')
#         return value

#     def validate_product_id(self, value):
#         if not Product.objects.filter(pk=value).exists():
#             raise serializers.ValidationError('No product with given ID was found.')
#         return value

#     def save(self, **kwargs):
#         cart_id = self.validated_data['cart_id']
#         product_id = self.context['request'].query_params.get('product')
#         quantity = self.validated_data['quantity']

#         try:
#             cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
#             cart_item.quantity += quantity
#             cart_item.save()
#             self.instance = cart_item
#         except CartItem.DoesNotExist:
#             self.instance = CartItem.objects.create(cart_id=cart_id, product_id=product_id, quantity=quantity)

#         return self.instance
    

#     class Meta:
#         model = CartItem
#         fields = ['id', 'product_id', 'quantity','cart_id']
    

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self,cart_item:CartItem):
        return cart_item.quantity * cart_item.product.offer_price

    class Meta:
        model =OrderItem
        fields = ['id','product','quantity','total_price']

class OrderSerializer(serializers.ModelSerializer): 
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id','customer','placed_at','payment_status','items']

class CreateOrderSerializer(serializers.Serializer):
    # cart_id = serializers.UUIDField()
    def validate_cart_id(self,cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('no cart with given ID was found')
        if CartItem.objects.filter(cart_id=cart_id).count()==0:
            raise serializers.ValidationError("The cart is empty")
        return cart_id
    
    def save(self, **kwargs): 
        with transaction.atomic():
            cart_id =self.validated_data['cart_id']
            try:
                customer = Account.objects.get(user_id=self.context['user_id'])
            except Account.DoesNotExist:
                customer=None
            order = Order.objects.create(customer=customer)
            cart_items=CartItem.objects.select_related('product').filter(cart_id=cart_id)

            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.offer_price,
                    quantity=item.quantity
                        )
                    for item in cart_items
                ]
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(pk=cart_id).delete()
            order_created.send_robust(self.__class__,order=order)
            return order


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields=['payment_status']