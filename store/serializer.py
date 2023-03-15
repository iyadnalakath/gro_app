from rest_framework import serializers
from . models import *
from decimal import Decimal
from django.db import transaction
from .signals import order_created
from main.functions import get_auto_id, password_generater
import pdb



class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source ='category.name',read_only=True)
    # image_url = serializers.SerializerMethodField()

    class Meta:
        model= Product
        fields = ['id','name','image','category','price','offer_price','offer_in_percentage','unit','category_name','last_update']

    offer_price = serializers.SerializerMethodField(method_name='calculate_final_price')
    
    def calculate_final_price(self,product:Product):
        final= product.price * int(product.offer_in_percentage)/ Decimal(100)
        return product.price - final

    # def get_image_url(self, product):
    #     request = self.context.get('request')
    #     if product.image:
    #         return request.build_absolute_uri(product.image.url)
    #     return None


 

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




class CartItemSerializer(serializers.ModelSerializer):
    # product_details = serializers.SerializerMethodField()
    product_details = ProductSerializer(source='product', read_only=True, context={'request': serializers.SerializerMethodField()})

    cart = serializers.CharField(source ='cart.id',read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'product_details','total_price']
        # extra_kwargs = {
        #     'cart': {'required': False},
        # }

    def get_total_price(self,cart_item:CartItem):
        return cart_item.quantity * cart_item.product.offer_price
    
    def get_product_details(self, obj):
        product = obj.product
        serializer = ProductSerializer(product)
        return serializer.data
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    account_view = serializers.CharField(source="account.username", read_only=True)
    total_price_of_products_in_cart = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'created_at','account','account_view', 'items','total_price_of_products_in_cart']

    def get_total_price_of_products_in_cart(self,cart):
        return sum([item.quantity * item.product.offer_price for item in cart.items.all()])

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','price','offer_in_percentage','image']
    # offer_price = serializers.SerializerMethodField(method_name='calculate_final_price')
    # def calculate_final_price(self,product:Product):
    #     final= product.price * int(product.offer_in_percentage)/ Decimal(100)
    #     return product.price - final
    


class OrderItemSerializer(serializers.ModelSerializer):
    # product = SimpleProductSerializer()
    # total_price = serializers.SerializerMethodField()
    # item = serializers.SerializerMethodField()
    # order = OrderSerializer(many=True,source='items')
    order = serializers.CharField(source ='order.id',read_only=True)
    cart_view = CartSerializer(source='cart',read_only=True,context={'request': serializers.SerializerMethodField()})
    # product_details = SimpleProductSerializer(source='product',read_only=True,context={'request': serializers.SerializerMethodField()})
    product_view = SimpleProductSerializer(read_only=True, source="product")

    # def get_product_details(self, obj):
    #     order_item = Product.objects.get(id=obj.id)
    #     return order_item

    # def get_total_price(self,cart_item:CartItem):
    #     return cart_item.quantity * cart_item.product.offer_price
    def get_cart_view(self, obj):
        cart = obj.cart
        serializer = CartSerializer(cart)
        return serializer.data
    
    class Meta:
        model =OrderItem
        fields = ['id','order','price','quantity','cart','cart_view','product','product_view']

# ,'product_details'

# class OrderSerializer(serializers.ModelSerializer):
#     items_order = OrderItemSerializer(many=True, read_only=True) 
#     account_view = serializers.CharField(source="account.username", read_only=True)
#     total = serializers.SerializerMethodField()
#     product_details = SimpleProductSerializer(source='product', read_only=True)

    
#     def get_total(self, obj):
#         return obj.total_price_of_order()
#     class Meta:
#         model = Order
#         fields = ['id','account','account_view','placed_at','items_order','payment_status','total','product_details']
class OrderSerializer(serializers.ModelSerializer):
    items_order = OrderItemSerializer(many=True, read_only=True) 
    account_view = serializers.CharField(source="account.username", read_only=True)
    total = serializers.SerializerMethodField()
    

    def get_total(self, obj):
        return obj.total_price_of_order()

    class Meta:
        model = Order
        fields = ['id','account','account_view','placed_at','items_order','payment_status','total']





class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','placed_at','account','payment_status']


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields=['payment_status']





        
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
    

    # def validate(self, data):
    #     cart_id = self.context['request'].query_params.get('cart_id')
    #     if not cart_id:
    #         raise serializers.ValidationError('cart_id is required')
    #     if not Cart.objects.filter(pk=cart_id).exists():
    #         raise serializers.ValidationError('no cart with given ID was found')
    #     if CartItem.objects.filter(cart_id=cart_id).count() == 0:
    #         raise serializers.ValidationError("The cart is empty")
    #     data['cart_id'] = cart_id
    #     return data

    # def create(self, validated_data):
    #     with transaction.atomic():
    #         cart_id = validated_data['cart_id']
    #         try:
    #             customer = Account.objects.get(owner=self.context['request'].user.id)
    #         except Account.DoesNotExist:
    #             customer = None
    #         order = Order.objects.create(customer=customer)
    #         cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)

    #         order_items = [
    #             OrderItem(
    #                 order=order,
    #                 product=item.product,
    #                 unit_price=item.offer_price,
    #                 quantity=item.quantity
    #             )
    #             for item in cart_items
    #         ]
    #         OrderItem.objects.bulk_create(order_items)
    #         Cart.objects.filter(pk=cart_id).delete()
    #         order_created.send_robust(self.__class__, order=order)
    #         return order

    # def validate(self, data):
    #     cart_id = self.context['request'].query_params.get('cart_id')
    #     if not cart_id:
    #         raise serializers.ValidationError('cart_id is required')
    #     if not Cart.objects.filter(pk=cart_id).exists():
    #         raise serializers.ValidationError('no cart with given ID was found')
    #     if CartItem.objects.filter(cart_id=cart_id).count() == 0:
    #         raise serializers.ValidationError("The cart is empty")
    #     data['cart_id'] = cart_id
    #     return data

    # def create(self, validated_data):
    #     with transaction.atomic():
    #         cart_id = validated_data['cart_id']
    #         try:
    #             customer = Account.objects.get(owner=self.context['request'].user)
    #         except Account.DoesNotExist:
    #             customer = None
    #         order = Order.objects.create(customer=customer)
    #         cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)

    #         order_items = [
    #             OrderItem(
    #                 order=order,
    #                 product=item.product,
    #                 unit_price=item.offer_price,
    #                 quantity=item.quantity
    #             )
    #             for item in cart_items
    #         ]
    #         OrderItem.objects.bulk_create(order_items)
    #         Cart.objects.filter(pk=cart_id).delete()
    #         order_created.send_robust(self.__class__, order=order)
    #         return order

# def save(self, **kwargs): 
#     with transaction.atomic():
#         cart_id = self.validated_data['cart_id']
#         try:
#             customer = Account.objects.get(user=self.context['request'].user)
#         except Account.DoesNotExist:
#             customer = None
#         order = Order.objects.create(customer=customer)
#         cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)

#         order_items = [
#             OrderItem(
#                 order=order,
#                 product=item.product,
#                 unit_price=item.offer_price,
#                 quantity=item.quantity
#             )
#             for item in cart_items
#         ]
#         OrderItem.objects.bulk_create(order_items)
#         Cart.objects.filter(pk=cart_id).delete()
#         order_created.send_robust(self.__class__,order=order)
#         return order


# class CreateOrderSerializer(serializers.Serializer):
#     cart_id = serializers.UUIDField()
#     def validate_cart_id(self,cart_id):
#         if not Cart.objects.filter(pk=cart_id).exists():
#             raise serializers.ValidationError('no cart with given ID was found')
#         if CartItem.objects.filter(cart_id=cart_id).count()==0:
#             raise serializers.ValidationError("The cart is empty")
#         return cart_id
    
#     def save(self, **kwargs): 
#         with transaction.atomic():
#             cart_id =self.validated_data['cart_id']
#             try:
#                 customer = Account.objects.get(user_id=self.context['user_id'])
#             except Account.DoesNotExist:
#                 customer=None
#             order = Order.objects.create(customer=customer)
#             cart_items=CartItem.objects.select_related('product').filter(cart_id=cart_id)

#             order_items = [
#                 OrderItem(
#                     order=order,
#                     product=item.product,
#                     unit_price=item.offer_price,
#                     quantity=item.quantity
#                         )
#                     for item in cart_items
#                 ]
#             OrderItem.objects.bulk_create(order_items)
#             Cart.objects.filter(pk=cart_id).delete()
#             order_created.send_robust(self.__class__,order=order)
#             return order



# class CartItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CartItem
#         fields = '__all__'
# *
# class CartItemSerializer(serializers.ModelSerializer):
#     product_details = serializers.SerializerMethodField()
#     # cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all(), required=False)
#     cart = serializers.SerializerMethodField()

#     class Meta:
#         model = CartItem
#         fields = ['id', 'cart', 'product', 'quantity', 'product_details']

#     def get_product_details(self, obj):
#         product = obj.product
#         serializer = ProductSerializer(product)
#         return serializer.data

#     def get_cart(self, obj):
#         cart = obj.cart
#         serializer = CartSerializer(cart)
#         return serializer.data
# *
# class CartItemSerializer(serializers.ModelSerializer):
#     product_details = serializers.SerializerMethodField()
#     cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all(), required=False)

#     class Meta:
#         model = CartItem
#         fields = ['id', 'cart', 'product', 'quantity', 'product_details']

#     def get_product_details(self, obj):
#         product = obj.product
#         serializer = ProductSerializer(product)
#         return serializer.data


# class ProductSerializer(serializers.ModelSerializer):
#     category_name = serializers.CharField(source ='category.name',read_only=True)
#     # image = serializers.SerializerMethodField()
#     class Meta:
#         model= Product
#         fields = ['id','name','image','category','price','offer_price','offer_in_percentage','unit','category_name','last_update']
    

#     offer_price = serializers.SerializerMethodField(method_name='calculate_final_price')
    
#     def calculate_final_price(self,product:Product):
#         final= product.price * int(product.offer_in_percentage)/ Decimal(100)
#         return product.price - final

#     # def get_image(self, obj):
#     #     if obj.image:
#     #         # if the image file is stored locally, return the full URL using the staticfiles_storage
#     #         if hasattr(settings, 'LOCAL_MEDIA_URL'):
#     #             return f"{settings.LOCAL_MEDIA_URL}{obj.image}"
#     #         # if the image file is stored remotely, return the full URL using the MEDIA_URL setting
#     #         else:
#     #             return f"{settings.MEDIA_URL}{obj.image}"
#     #     return None





































# important

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     print(data['product'])
    #     return data