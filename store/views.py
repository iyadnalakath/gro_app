from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.filters import SearchFilter,OrderingFilter
from . pagination import DefaultPagination
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser,DjangoModelPermissions
from . models import *
from . serializer import *
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin,ListModelMixin
from django.db.models import Count
from rest_framework import status
from  . permissions import IsAdminOrReadOnly,FullDjangoModelPermissions,ViewCustomerHistoryPermissions
from rest_framework import generics
from .models import Product
from . serializer import ProductSerializer
from rest_framework import generics, permissions
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from django.db.models import F
from rest_framework.request import Request
from django.http import Http404
from rest_framework.generics import RetrieveAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
import json
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication,SessionAuthentication,BasicAuthentication
from .authentication import CustomTokenAuthentication
# Create your views here.


# product fulldetails

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # filter_backends = [SearchFilter,OrderingFilter]
    filter_backends = [SearchFilter]
    # pagination_class = DefaultPagination
    permission_classes =[IsAdminOrReadOnly]
    # permission_classes =[AllowAny]
    # authentication_classes = [CustomTokenAuthentication]
    search_fields = ['name','category__name']
    # ordering_fields = ['offer_price']

    def get_serializer_context(self):
        return {'request':self.request}
    

    def get_authenticators(self):
        if self.request.method == 'GET':
            return []
        return [CustomTokenAuthentication()]

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count()>0:
            return Response({'error':'producty cannot be deleted because it is assoiciated with an order item .'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


# review details

class ReviewViewSet(ModelViewSet):
    queryset =Review.objects.all()
    serializer_class =ReviewSerializer



# custome details

# class CustomerViewSet(ModelViewSet):
#     queryset = Customer.objects.all()
#     serializer_class =CustomerSerializer
#     permission_classes=[IsAdminUser]


#     @action(detail=True,permission_classes=[ViewCustomerHistoryPermissions])
#     def history(self,request,pk):
#         return Response("okk")

 

#     @action(detail=False ,methods=['GET','PUT'],permission_classes =[IsAuthenticated])
#     def me(self,request):
#         try:
#             (customer,created) =Customer.objects.get_or_create(user_id=request.user.id)
#         except Customer.DoesNotExist:
#             customer=None
#         if request.method =='GET':
#             serializer =CustomerSerializer(customer)
#             return Response(serializer.data)
#         elif request.method=='PUT':
#             serializer=CustomerSerializer(customer,data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data)


# Category details



class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        queryset = Product.objects.filter(category_id=category_id)
        return queryset



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(product_count=Count('product')).all()
    serializer_class = CategorySerializer
    permission_classes =[IsAdminOrReadOnly]


    def get_authenticators(self):
        if self.request.method == 'GET':
            return []
        return [CustomTokenAuthentication()]
    
    def delete(self,request,pk):
        collection = get_object_or_404(Category,pk=pk)
        if collection.products.count()>0:
            return Response({'error':'Category canot be deleted becase it includes one or more products'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# Banner details


class BannerViewSet(ModelViewSet):
    permission_classes =[IsAdminOrReadOnly]
    queryset =Banner.objects.all()
    serializer_class =BannerSerializer

    def get_authenticators(self):
        if self.request.method == 'GET':
            return []
        return [CustomTokenAuthentication()]
# cartprogram

# class CartViewSet(CreateModelMixin,GenericViewSet,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin,ListModelMixin):
#     queryset = Cart.objects.prefetch_related('items__product').all()
#     serializer_class = CartSerializer
#     permission_classes=[IsAuthenticated]

  
#     def create(self, request, *args, **kwargs):

#         data = request.data.copy()
#         # print (self.request.user.role)
#         data["account"]=self.request.user.id

#         serializer = CartSerializer(data=data)

#         if serializer.is_valid():
#             # print (self.request.user.role)
#             if self.request.user.role in ['admin','customer']:

#                 # serializer.save(event_team=self.request.user)
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             else:
#                 raise PermissionDenied("You are not allowed to create this object.")
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def list(self, request, *args, **kwargs):
#         # queryset = self.filter_queryset(queryset)
#         queryset = self.get_queryset()
#         queryset = self.filter_queryset(queryset)

#         if self.request.user.role == "customer":
#             queryset = queryset.filter(account=self.request.user)
#             serializer = CartSerializer(queryset, many=True)
#             return Response(serializer.data)
#         elif self.request.user.role in ["admin"]:
#             return super().list(request, *args, **kwargs)

#         else:
#             raise PermissionDenied("You are not allowed to retrieve this object.")

#     # def list(self, request, *args, **kwargs):



# # class CartItemViewSet(ModelViewSet):
# #     http_method_names=['get','post','patch','delete']
# #     def get_serializer_class(self):
# #         if self.request.method=='POST':
# #             return AddCartSerializer

# #         elif self.request.method=='PATCH':
# #             return UpdateCartItemSerializer

# #         return CartItemSerializer


 
# #     def get_serializer_context(self):
# #         return {'cart_id':self.kwargs['cart_pk'], 'request': self.request}


# #     def get_queryset(self):
# #         return CartItem.objects.select_related('product').filter(cart_id =self.kwargs['cart_pk'])
        
# class CartItemViewSet(viewsets.ModelViewSet):
#     serializer_class = CartItemSerializer
#     queryset = CartItem.objects.all()
#     # lookup_url_kwarg = 'cart_pk'
#     lookup_field = 'id'
#     http_method_names = ['get', 'post', 'patch', 'delete']
#     def get_queryset(self):
#             return CartItem.objects.select_related('product').filter(cart_id=self.kwargs['cart_pk'])


#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return AddCartSerializer
#         elif self.request.method == 'PATCH':
#             return UpdateCartItemSerializer
#         return CartItemSerializer

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context.update({
#             'cart_id': self.kwargs['cart_pk'],
#             'request': self.request
#         })
#         return context

 


class CartView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Cart.objects.all()
        if self.request.user.role == "customer":
            queryset = queryset.filter(account=self.request.user)
        return queryset




    
class CartItemView(generics.ListCreateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'



    # def get_cart(self):
    #     cart_view = CartView()
    #     return cart_view.get_object(request=self.request)
    def get_queryset(self):
        return CartItem.objects.filter(cart__account=self.request.user)
 
    def get(self, request, *args, **kwargs):
        try:
            item = self.get_object()
        except Http404:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(item)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        try:
            item = self.get_object()
        except Http404:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if item.cart.account != request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        self.perform_destroy(item)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        product_id = self.request.query_params.get('product')

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"product": "Invalid product ID."}, status=status.HTTP_400_BAD_REQUEST)

        data["product"] = product_id
        serializer = CartItemSerializer(data=data,context={'request': request})

        if serializer.is_valid():
            quantity = serializer.validated_data.get('quantity', 1)
            # cart = self.get_cart()
            cart = Cart.objects.filter(account=request.user).first()
            if not cart:
                cart = Cart.objects.create(account=request.user)

                serializer.validated_data['cart'] = cart  # set the cart field to the correct Cart instance

            existing_item = CartItem.objects.filter(cart=cart, product=product).first()

            if existing_item:
                existing_item.quantity += quantity
                existing_item.save(update_fields=['quantity'])
                serializer = CartItemSerializer(existing_item)
            else:
                serializer.save(cart=cart, product=product, quantity=quantity)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request, *args, **kwargs):
    #     self.request = request
    #     return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.request = request
        return super().post(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        try:
            item = self.get_object()
        except Http404:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        if item.cart.account != request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# class OrderViewSet(ModelViewSet):
#     http_method_names=['get','post','patch','delete','head','options']

#     # def get_permissions(self):
#     #     if self.request.method in ['PUT','PATCH','DELETE']:
#     #         return [IsAdminUser()]
#     #     return [IsAuthenticated()]
#     queryset = Order.objects.all()
#     # serializer_class = CartItemSerializer
#     permission_classes = [permissions.IsAuthenticated]


#     def get_serializer_class(self):
#         if self.request.method=='POST':
#             return CreateOrderSerializer
#         elif self.request.method=='PATCH':
#             return UpdateOrderSerializer
#         # elif self.request.method=='GET':
#         #     return OrderItemSerializer
#         return OrderSerializer

#     def create(self, request, *args, **kwargs):
#         data = request.data.copy()
#         data["account"] = self.request.user.id
#         # cart = data.get("cart") # Get the Cart instance with ID 1
#         data["cart"] = self.request.query_params.get("cart")
#         serializer = CreateOrderSerializer(data=data, context={'request': request})

#         if serializer.is_valid():
#             if self.request.user.role in ["admin", "customer"]:
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             else:
#                 raise PermissionDenied("You are not allowed to create this object.")
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_staff:
#             return Order.objects.all()
#         try:
#             account_id = Account.objects.only('id').get(id=user.id)
#         except Account.DoesNotExist:
#             account_id = None
#         return Order.objects.filter(account_id=account_id)
# class OrderDetailView(ModelViewSet):
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     lookup_field = 'pk'

#     def get_queryset(self):
#         return Order.objects.all()

#     def get_object(self):
#         queryset = self.get_queryset()
#         obj = queryset.filter(pk=self.kwargs[self.lookup_field]).first()
#         if obj:
#             if self.request.user.role == "customer":
#                 if obj.account != self.request.user:
#                     raise PermissionDenied("You are not allowed to access this order")
        # return obj

# class UpdatePaymentStatusView(generics.UpdateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = UpdateOrderItemSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     lookup_field = 'pk'

#     def update(self, request, *args, **kwargs):
#         order_id = kwargs['pk']
#         payment_status = request.data.get('payment_status')

#         try:
#             order = self.get_queryset().get(id=order_id)
#         except Order.DoesNotExist:
#             return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

#         order.payment_status = payment_status
#         order.save()

#         serializer = self.get_serializer(order)
#         return Response(serializer.data)
# class OrderView(ModelViewSet):
class OrderView(generics.ListAPIView,RetrieveUpdateDestroyAPIView):
    # queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    # lookup_field = 'pk'

    def get_queryset(self):
        queryset = Order.objects.all()
        # queryset = Order.objects.select_related('account', 'orderitems__product')
        if self.request.user.role == "customer":
            queryset = queryset.filter(account=self.request.user)
        return queryset

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

    # def get(self, request, *args, **kwargs):
    #     order_id = kwargs['pk']
    #     try:
    #         order = self.get_queryset().get(id=order_id)
    #     except Order.DoesNotExist:
    #         return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = self.get_serializer(order)
    #     return Response(serializer.data)
    

    
    # def update_payment_status(self, request, *args, **kwargs):
    #     order_id = kwargs['pk']
    #     payment_status = request.data.get('payment_status')

    #     try:
    #         order = self.get_queryset().get(id=order_id)
    #     except Order.DoesNotExist:
    #         return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    #     order.payment_status = payment_status
    #     order.save()

    #     serializer = self.get_serializer(order)
    #     return Response(serializer.data)
    # def get_object(self):
    #     queryset = Order.objects.filter(account=self.request.user)
    #     obj = get_object_or_404(queryset)
    #     return obj
 
    
class OrderItemView(generics.ListCreateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'



    # def get_serializer_class(self):
    #     if self.request.method=='POST':
    #         return CreateOrderSerializer
    #     elif self.request.method=='PATCH':
    #         return UpdateOrderSerializer
    #     return OrderSerializer


    # def get_cart(self):
    #     cart_view = CartView()
    #     return cart_view.get_object(request=self.request)
    def get_queryset(self):
        if self.request.user.role == "customer":
            return OrderItem.objects.filter(order__account=self.request.user)
        return OrderItem.objects.all()
    
    def get(self, request, *args, **kwargs):
        try:
            items_order = self.get_object()
        except Http404:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(items_order)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        try:
            items_order = self.get_object()
        except Http404:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if items_order.order.account != request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        self.perform_destroy(items_order)
        return Response(status=status.HTTP_204_NO_CONTENT)
    



    def create(self, request, *args, **kwargs):
        cart_id = self.request.query_params.get('cart')
        try:
            cart = Cart.objects.get(pk=cart_id)
        except Cart.DoesNotExist:
            return Response({"cart": "Invalid cart ID."}, status=status.HTTP_400_BAD_REQUEST)
        
        if cart.items.count() == 0:
            return Response({"cart": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

    
    # rest of the code to create Order and OrderItem instances

        order_data = {
            'account': request.user,
            # 'payment_status': 'pending',
            # 'total': cart.total_price_of_products_in_cart,
  
        }
        order = Order(**order_data)
        order.save() # save the order to the database

        # Iterate through the items in the cart and create a new OrderItem instance for each item
        order_items = []
        for cart_item in cart.items.all():
            order_item_data = {
                'order': order,
                'product': cart_item.product.id,
                'quantity': cart_item.quantity,
                'price': cart_item.product.offer_price,
                'cart_id': cart_id,
            }
            order_item = OrderItem(**order_item_data)
            order_item.save() # save the order item to the database
            order_items.append(order_item)
            

        order.items_order.add(*order_items) # add the saved order items to the order instance

        # Clear the cart
        # cart.clear()
        cart.items.all().delete()
        

        # Return the serialized Order instance
        serializer = self.get_serializer(order)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
        response_data = {
            'message': 'Order created successfully.',
            # 'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    # def get(self, request, *args, **kwargs):
    #     self.request = request
    #     return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.request = request
        return super().post(request, *args, **kwargs)
    

    # def update(self, request, *args, **kwargs):
    #     try:
    #         order_item = self.get_object()
    #     except Http404:
    #         return Response({'error': 'Order item not found'}, status=status.HTTP_404_NOT_FOUND)

    #     # if order_item.order.account != request.user:
    #     if not request.user.is_staff:
    #         return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

    #     order = order_item.order
    #     if order.payment_status == 'paid':
    #         return Response({'error': 'Payment has already been made for this order'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Update the payment_status field of the Order instance
    #     order.payment_status = request.data.get('payment_status', order.payment_status)
    #     order.save()

    #     serializer = self.get_serializer(order_item, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            order_item = self.get_object()
        except Http404:
            return Response({'error': 'Order item not found'}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_staff:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        order = order_item.order
        if order.payment_status == Order.PAYMENT_STATUS_COMPLETE:
            return Response({'error': 'Payment has already been made for this order'}, status=status.HTTP_400_BAD_REQUEST)

        payment_status = request.data.get('payment_status')
        if payment_status is not None and payment_status not in dict(Order.PAYMENT_STATUS_CHOICES).keys():
            return Response({'error': 'Invalid payment status'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the payment_status field of the Order instance
        order.payment_status = payment_status or order.payment_status
        order.save()

        serializer = self.get_serializer(order_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    # def update(self, request, *args, **kwargs):
    #     order = self.get_object()
    #     data = request.data.copy()
    #     data["account"] = self.request.user.id

    #     serializer =OrderSerializer(order, data)
    #     if serializer.is_valid():
    #         if request.user.role == "admin":
    #             # if order.account.id == self.request.user.id:
    #             serializer.save()
    #             return Response(serializer.data)
    #             # else:
    #             #     raise PermissionDenied("You are not allowed to update this object.")
    #         else:
    #             raise PermissionDenied("only autherised team allowed to update it")
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.payment_status = request.data.get('payment_status', instance.payment_status)
    #     instance.save()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
    
    # def update(self, request, *args, **kwargs):
    #     try:
    #         item = self.get_object()
    #     except Http404:
    #         return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    #     # if item.cart.account != request.user:
    #     if self.request.user != "admin":
    #         return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    #     # serializer = self.get_serializer(item, data=request.data, partial=True)
    #     serializer= UpdateOrderSerializer(item, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # def create(self, request, *args, **kwargs):
    #     cart_id = request.query_params.get('cart')
    #     cart = get_object_or_404(Cart, pk=cart_id)
    #     if cart.user != request.user:
    #         raise PermissionDenied("You are not allowed to create an order item from this cart.")
    #     order = Order.objects.create(account=request.user)
    #     order_items = []
    #     for cart_item in cart.cart_items.all():
    #         order_item = OrderItem.objects.create(
    #             order=order,
    #             product=cart_item.product,
    #             quantity=cart_item.quantity,
    #             price=cart_item.product.price,
    #         )
    #         order_items.append(order_item)
    #     serializer = OrderItemSerializer(order_items, many=True)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # def create(self, request, *args, **kwargs):





















    # def get_queryset(self):
    #     return CartItem.objects.filter(cart__account=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     serializer = CartItemSerializer(data=request.data)
    #     product_id = self.request.query_params.get('product')
    #     print(product_id)

    #     if not product_id:
    #         return Response({'product': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)
    #     if serializer.is_valid():
    #         cart = Cart.objects.get_or_create(account=self.request.user)[0]
    #         quantity = serializer.validated_data.get('quantity', 1)

    #         # Check if the product already exists in the cart
    #         existing_item = CartItem.objects.filter(cart=cart, product=product_id).first()

    #         if existing_item:
    #             # If the product exists in the cart, increase its quantity
    #             existing_item.quantity = F('quantity') + quantity
    #             existing_item.save(update_fields=['quantity'])
    #         else:
    #             # Otherwise, add the new product to the cart
    #             serializer.save(cart=cart, product=product_id, quantity=quantity)

    #         # Return a success response
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def create(self, request, *args, **kwargs):
    #     # data = request.data.copy()
    #     # product_id = self.request.query_params.get('product')
    #     data = request.data.copy()
    #     data["product"] = self.request.query_params.get('product')
    #     data["cart"] = self.request.query_params.get('cart')
        

    #     # if not product:
    #     #     return Response({'product': 'This field is requireded.'}, status=status.HTTP_400_BAD_REQUEST)
    #     serializer = CartItemSerializer(data=data)
    #     if serializer.is_valid():
    #         cart = Cart.objects.get_or_create(account=self.request.user)[0]
    #         quantity = serializer.validated_data.get('quantity', 1)
    #         product_id = data.get("product")
    #         cart_id = data.get("cart")


    #         # Retrieve the product instance using the product_id
    #         # try:
    #         #     product = Product.objects.get(id=product)
    #         # except Product.DoesNotExist:
    #         #     return Response({'product': 'Invalid product id.'}, status=status.HTTP_400_BAD_REQUEST)

    #         # Check if the product already exists in the cart
    #         existing_item = CartItem.objects.filter(cart=cart_id, product=product_id).first()

    #         if existing_item:
    #             # If the product exists in the cart, increase its quantity
    #             existing_item.quantity = F('quantity') + quantity
    #             existing_item.save(update_fields=['quantity'])
    #         else:
    #             # Otherwise, add the new product to the cart
    #             # serializer.save(cart=cart_id, product=product_id, quantity=quantity)
    #             serializer.save()

    #         # Return a success response
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#  class CartItemView(generics.ListCreateAPIView):
#     serializer_class = CartItemSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return CartItem.objects.filter(cart__account=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     data = request.data.copy()
    #     product_id = self.request.query_params.get('product')

    #     try:
    #         product = Product.objects.get(pk=product_id)
    #     except Product.DoesNotExist:
    #         return Response({"product": "Invalid product ID."}, status=status.HTTP_400_BAD_REQUEST)

    #     data["product"] = product_id
    #     serializer = CartItemSerializer(data=data)

    #     if serializer.is_valid():
    #         quantity = serializer.validated_data.get('quantity', 1)
    #         cart_view = CartView()
    #         cart = cart_view.get_object()

    #         serializer.validated_data['cart'] = cart
    #         existing_item = CartItem.objects.filter(cart=cart, product=product).first()

    #         if existing_item:
    #             existing_item.quantity += quantity
    #             existing_item.save(update_fields=['quantity'])
    #             serializer = CartItemSerializer(existing_item)
    #         else:
    #             serializer.save(cart=cart, product=product, quantity=quantity)

    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class OrderViewSet(ModelViewSet):
#     http_method_names=['get','post','patch','delete','head','options']

#     def get_permissions(self):
#         if self.request.method in ['PUT','PATCH','DELETE']:
#             return [IsAdminUser()]
#         return [IsAuthenticated()]



    # def create(self, request, *args, **kwargs):
    #     serializer =CreateOrderSerializer(data=request.data,context={'user_id':self.request.user.id})
    #     serializer.is_valid(raise_exception=True)
    #     order = serializer.save()
    #     serializer=OrderSerializer(order)
    #     return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     serializer_context = {
    #         'user_id': request.user.id,
    #         'request': request  # add the request object to the context
    #     }
    #     serializer = CreateOrderSerializer(data=request.data, context=serializer_context)
    #     serializer.is_valid(raise_exception=True)
    #     order = serializer.save()
    #     serializer = OrderSerializer(order)
    #     return Response(serializer.data)

    # def get_serializer_class(self):
    #     if self.request.method=='POST':
    #         return CreateOrderSerializer
    #     elif self.request.method=='PATCH':
    #         return UpdateOrderSerializer
    #     return OrderSerializer
    
    # # def post(self, request, *args, **kwargs):
    # #         serializer_context = {'request': request}
    # #         serializer = self.get_serializer(data=request.data, context=serializer_context)
    # #         serializer.is_valid(raise_exception=True)
    # #         self.perform_create(serializer)
    # #         return Response(serializer.data, status=status.HTTP_201_CREATED) 

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_staff:
    #         return Order.objects.all()
    #     try:
    #         customer_id = Account.objects.only('id').get(id = user.id)
    #     except Account.DoesNotExist:
    #         customer_id =None
    #     return Order.objects.filter(customer_id=customer_id)







    
    # def list(self, request, *args, **kwargs):
    #     # queryset = self.filter_queryset(queryset)
    #     queryset = self.get_queryset()
    #     queryset = self.filter_queryset(queryset)

    #     if self.request.user.role == "customer":
    #         queryset = queryset.filter(account=self.request.user)
    #         serializer = CartSerializer(queryset, many=True)
    #         return Response(serializer.data)
    #     elif self.request.user.role in ["admin"]:
    #         return super().list(request, *args, **kwargs)

    #     else:
    #         raise PermissionDenied("You are not allowed to retrieve this object.")

    # def get_object(self, request=None):
    #     try:
    #         cart = Cart.objects.get(account=request.user)
    #     except Cart.DoesNotExist:
    #         cart = Cart.objects.create(account=request.user)
    #     return cart
    # def get_object(self, request=None):
    #     try:
    #         cart = Cart.objects.get(account=self.request.user)
    #     except Cart.DoesNotExist:
    #         cart = Cart.objects.create(account=self.request.user)
    #     return cart
# class CartItemView(generics.ListCreateAPIView):
#     serializer_class = CartItemSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return CartItem.objects.filter(cart__account=self.request.user)