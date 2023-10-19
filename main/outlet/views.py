from django.shortcuts import render, HttpResponse, get_object_or_404,redirect
from .forms import SaleOrderForm,AddUUIDForm
from .models import SaleOrder,SaleOrderProduct
from django.http import HttpResponse, HttpResponseBadRequest
from inlet.models import Product,Master
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
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



def sale_order_detail(request, bill_no):
    sale_order = get_object_or_404(SaleOrder, bill_no=bill_no)
    
    return render(request, 'sale_order_detail.html', {'sale_order': sale_order})



def sale_order_product_detail(request, bill_no, sale_order_product_id):
    sale_order = get_object_or_404(SaleOrder, bill_no=bill_no)
    sale_order_product = get_object_or_404(SaleOrderProduct, product_id=sale_order_product_id, sale_order=sale_order)
    inventory_count = Master.objects.filter(product_id=sale_order_product.product_id).count()
    selected_master_uuids = sale_order_product.uuids
    form = AddUUIDForm(request.POST)
    
    return render(request, 'sale_order_product_detail.html', {'sale_order': sale_order, 'sale_order_product': sale_order_product, 'inventory_count': inventory_count, 'selected_master_uuids': selected_master_uuids ,'form': form})


def add_uuid(request, bill_no, sale_order_product_id):
    if request.method == 'POST':
        new_uuid = request.POST.get('new_uuid')
        sale_order = get_object_or_404(SaleOrder, bill_no=bill_no)
        sale_order_product = get_object_or_404(SaleOrderProduct, product_id=sale_order_product_id, sale_order=sale_order)

        # Check for duplicate UUIDs in selected_master_uuids
        if new_uuid in sale_order_product.uuids:
            messages.error(request, f"UUID '{new_uuid}' is already in the list.")
            return redirect('sale_order_product_detail', bill_no=bill_no, sale_order_product_id=sale_order_product_id)

        # Check if the new_uuid exists in the Master model for the same product
        matching_master = Master.objects.filter(product=sale_order_product.product, uuid=new_uuid).first()
        if not matching_master:
            messages.error(request, f"UUID '{new_uuid}' does not match the product in the sale order.")
            return redirect('sale_order_product_detail', bill_no=bill_no, sale_order_product_id=sale_order_product_id)

        # Add the new UUID to the selected_master_uuids list
        sale_order_product.uuids.append(new_uuid)
        sale_order_product.save()

    # Redirect back to the sale_order_product_detail page
    return redirect('sale_order_product_detail', bill_no=bill_no, sale_order_product_id=sale_order_product_id)





def save_and_return(request, bill_no, sale_order_product_id):
    sale_order = get_object_or_404(SaleOrder, bill_no=bill_no)
    sale_order_product = get_object_or_404(SaleOrderProduct, id=sale_order_product_id, sale_order=sale_order)

    # Assuming you have gathered the required data, build the JSON data
    appended_data = {
        "added_by": request.user.username,  # Adjust as needed
        "added_date_time": timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        "Bill_no": sale_order.bill_no,
        # Add other fields like Grn no, vehicle no, PO Number, etc.
    }

    # Iterate through the Master objects associated with the SaleOrderProduct
    for master in sale_order_product.product.master_set.all():
        master_data = master.data_json or {}  # Retrieve existing data or initialize an empty dictionary
        master_data.setdefault('outlet', {}).update(appended_data)

        # Update the data_json field of the Master
        master.data_json = master_data
        master.save()

    # Redirect back to the Sale Order details page
    return redirect('sale_order_detail', bill_no=bill_no)





