from django.shortcuts import render, HttpResponse, get_object_or_404
from .forms import SaleOrderForm
from .models import SaleOrder

# Create your views here.


def create_sale_order(request):
    if request.method == 'POST':
        form = SaleOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('sale_order_list')  # Redirect to the sale order list view
    else:
        form = SaleOrderForm()
    
    return render(request, 'create_sale_order.html', {'form': form})




def outlet_home(request):
    sale_orders = SaleOrder.objects.all()
    return render(request, 'outlet_home.html', {'sale_orders': sale_orders})



def sale_order_detail(request, sale_order_id):
    sale_order = get_object_or_404(SaleOrder, id=sale_order_id)
    
    return render(request, 'sale_order_detail.html', {'sale_order': sale_order})