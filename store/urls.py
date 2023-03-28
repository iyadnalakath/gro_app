# from rest_framework_nested.routers import NestedDefaultRouter
# from . import views
# from rest_framework import routers


# router=routers.DefaultRouter()

# router.register('products',views.ProductViewSet,basename="product")
# router.register('category',views.CategoryViewSet),
# router.register('review',views.ReviewViewSet),
# router.register('banner',views.BannerViewSet),
# router.register('carts',views.CartViewSet,basename="carts")
# router.register('order',views.OrderViewSet,basename='order'),




# products_router= NestedDefaultRouter(router,'products',lookup='product')
# products_router.register('reviews',views.ReviewViewSet,basename='product_reviews')

# carts_router=NestedDefaultRouter(router,'carts',lookup='cart')
# carts_router.register('items',views.CartItemViewSet,basename='cart-item') # cart-item-list / cart-item-detail




# URLConf
# urlpatterns = router.urls + products_router.urls + carts_router.urls

from django.urls import path, include
from rest_framework_nested import routers
from . import views
from rest_framework_nested.routers import NestedDefaultRouter
from .views import CartView, CartItemView,OrderItemView,OrderView

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename="product")
router.register('category', views.CategoryViewSet)
router.register('review', views.ReviewViewSet)
router.register('banner', views.BannerViewSet)
# router.register('carts', views.CartViewSet, basename="carts")
# router.register('order', views.OrderView, basename='order')
# router.register('orderitems', views.OrderViewSet, basename='order_itemss')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product_reviews')

# urlpatterns = router.urls + products_router.urls

# carts_router = NestedDefaultRouter(router, 'carts', lookup='cart')
# carts_router.register('items', views.CartItemViewSet, basename='cart-item')



urlpatterns = [

    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/items/', CartItemView.as_view(), name='cart-items'),
    path('cart/items/<int:pk>/', CartItemView.as_view(), name='cart-item'),
    path('order/', OrderView.as_view(), name='order'),
    path('orders/<int:pk>/', OrderView.as_view(), name='user-order'),
    # path('store/order/items/<int:pk>/update_payment_status/', UpdatePaymentStatusView.as_view(), name='update_payment_status'),
    path('order/items/', OrderItemView.as_view(), name='order-items'),
    path('order/items/<int:pk>/', OrderItemView.as_view(), name='order-item'),
]

urlpatterns += router.urls