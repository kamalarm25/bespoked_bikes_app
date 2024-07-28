from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='sales-home'),
    path('salespersons/', views.salesperson_list, name='salesperson_list'),
    path('salesperson/update/<int:pk>/', views.salesperson_update, name='salesperson_update'),
    path('products/', views.product_list, name='product_list'),
    path('product/update/<int:pk>/', views.product_update, name='product_update'),
    path('customers/', views.customer_list, name='customer_list'),
    path('sales/', views.sales_list, name='sales_list'),
    path('sale/create/', views.create_sale, name='create_sale'),
    path('report/quarterly-commission/', views.quarterly_commission_report, name='quarterly_commission_report_default'),
    path('report/quarterly-commission/<int:year>/<int:quarter>/', views.quarterly_commission_report, name='quarterly_commission_report'),

]
