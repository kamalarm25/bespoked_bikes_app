from django.shortcuts import render, get_object_or_404, redirect
from .models import Salesperson, Product, Customer, Sales, Discount
from .forms import SalespersonForm, ProductForm, CustomerForm, SalesForm
from django.db.models import Sum, F
from django.utils.dateparse import parse_date
import json
from decimal import Decimal
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

def home(request):
    return render(request, 'sales/home.html', {})

def salesperson_list(request):
    salespersons = Salesperson.objects.all()
    return render(request, 'sales/salesperson_list.html', {'salespersons': salespersons, 'title':'Salesperson'})

def salesperson_update(request, pk):
    salesperson = get_object_or_404(Salesperson, pk=pk)
    if request.method == 'POST':
        form = SalespersonForm(request.POST, instance=salesperson)
        if form.is_valid():
            form.save()
            return redirect('salesperson_list')
    else:
        form = SalespersonForm(instance=salesperson)
    return render(request, 'sales/salesperson_form.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'sales/product_list.html', {'products': products, 'title':'Products'})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'sales/product_form.html', {'form': form})

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'sales/customer_list.html', {'customers': customers, 'title':'Customers'})

def sales_list(request):
    sales = Sales.objects.all()
    

    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    if from_date:
        from_date_parsed = parse_date(from_date)
        if from_date_parsed:
            sales = sales.filter(sales_date__gte=from_date_parsed)
    if to_date:
        to_date_parsed = parse_date(to_date)
        if to_date_parsed:
            sales = sales.filter(sales_date__lte=to_date_parsed)

    for sale in sales:
        sale.commission = sale.price * (sale.product.commission_percentage / 100)

    context = {
        
        'from_date': from_date,
        'to_date': to_date,
        
    }


    return render(request, 'sales/sales_list.html', {'sales': sales, 'title': 'Saleslist'})



def create_sale(request):
    if request.method == 'POST':
        form = SalesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales_list')
    else:
        form = SalesForm()

    products = Product.objects.all()
    discounts = Discount.objects.all()

    # Convert Decimal to float for JSON serialization
    products_data = {
        product.id: {
            'sale_price': float(product.sale_price)  # Convert Decimal to float
        }
        for product in products
    }
    
    discounts_data = [
        {
            'product': discount.product.id,
            'begin_date': discount.begin_date.isoformat(),  # Convert to ISO format
            'end_date': discount.end_date.isoformat(),      # Convert to ISO format
            'discount_percentage': float(discount.discount_percentage)
        }
        for discount in discounts
    ]

    return render(request, 'sales/sales_form.html', {'form': form, 
        'products_json': json.dumps(products_data, cls=DjangoJSONEncoder),
        'discounts_json': json.dumps(discounts_data, cls=DjangoJSONEncoder),
        })

def quarterly_commission_report(request, year=None, quarter=None):
    # Define the start and end dates of the quarter
    if (year == None) or (quarter == None):
        report = Sales.objects.values('salesperson__first_name', 'salesperson__last_name').annotate(
        total_sales=Sum(F('price')),
        total_commission=Sum(F('price') * F('product__commission_percentage') / 100)
    )
    else:
        if quarter == 1:
            start_date = f"{year}-01-01"
            end_date = f"{year}-03-31"
        elif quarter == 2:
            start_date = f"{year}-04-01"
            end_date = f"{year}-06-30"
        elif quarter == 3:
            start_date = f"{year}-07-01"
            end_date = f"{year}-09-30"
        elif quarter == 4:
            start_date = f"{year}-10-01"
            end_date = f"{year}-12-31"

        report = Sales.objects.filter(
            sales_date__range=[start_date, end_date]
        ).values('salesperson__first_name', 'salesperson__last_name').annotate(
            total_sales=Sum(F('price')),
            total_commission=Sum(F('price') * F('product__commission_percentage') / 100)
        )

    # Get a list of years for the dropdown
    current_year = datetime.now().year
    years = list(range(current_year - 10, current_year + 1))
    years.sort(reverse=True)
    return render(request, 'sales/quarterly_commission_report.html', {'report': report, 'title':'Report', 'current_year': year,
        'years': years})

def decimal_to_float(obj):
    """Convert Decimal to float."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError("Type not serializable")
