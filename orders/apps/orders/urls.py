from django.urls import path
from .views import *

app_name="orders"

urlpatterns = [
    # path('get-orders', ListOrdersView.as_view()),
    # path('by/search', SearchOrderItemsView.as_view()),
    # path('search-orders', SearchOrdersView.as_view()),
    # path('library/products', ListOrdersProductsView.as_view()),
    # path('library/sellers', ListOrdersSellerView.as_view()),
    # path('order-items', ListMyOrderItemsView.as_view()),
    # path('order-item/<order_id>', OrderItemDetailView.as_view()),
    # path('update-order-item', UpdateOrderItemStatus.as_view()),
    # path('update-tracking', UpdateOrderItemTracking.as_view()),
    # path('update-tracking-url', UpdateOrderItemTrackingUrl.as_view()),
    # path('get-order/<transactionId>', ListOrderDetailView.as_view()),
    # path('create-order', CreateOrderView.as_view()),
    # path('create-order-saved', CreateOrderSavedView.as_view()),
    # path('create-order-crypto', CreateOrderCryptoView.as_view()),
    # path('create-game-order', CreateGameOrderView.as_view()),
    # path('by/search/transaction', SearchTransactionView.as_view()),
]