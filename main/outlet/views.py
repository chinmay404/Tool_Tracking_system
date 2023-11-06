from django.shortcuts import render, HttpResponse, get_object_or_404,redirect
from .forms import SaleOrderForm,AddUUIDForm
from .models import SaleOrder,SaleOrderProduct
from django.http import HttpResponse, HttpResponseBadRequest
from inlet.models import Product,Master
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from managment.decorators import unauth_user, allowed_users
from django.db.models import Sum, Count
# Create your views here.





@login_required(login_url='managment/login/')
@allowed_users(allowed_roles=['admins', 'outlet_user',])
def outlet_home(request):
    sale_orders = SaleOrder.objects.all()
    return render(request, 'outlet_home.html', {'sale_orders': sale_orders})



@login_required(login_url='managment/login/')
@allowed_users(allowed_roles=['admins', 'outlet_user',])
def sale_order_detail(request, bill_no):
    sale_order = get_object_or_404(SaleOrder, bill_no=bill_no)
    
    total_products_required = sale_order.saleorderproduct_set.aggregate(total_required=Sum('quantity'))['total_required']
    total_products_added = len(sale_order.uuids)
    remaning = total_products_required-total_products_added
    print(sale_order.products)
    
    context = {
        'sale_order': sale_order,
        'total_products_required': total_products_required,
        'total_products_added': total_products_added,
        'remaning':remaning
    }
    
    return render(request, 'sale_order_detail.html', context)



@login_required(login_url='managment/login/')
@allowed_users(allowed_roles=['admins', 'outlet_user',])
def sale_order_product_detail(request, bill_no, sale_order_product_id):
    sale_order = get_object_or_404(SaleOrder, bill_no=bill_no)
    sale_order_product = get_object_or_404(SaleOrderProduct, product_id=sale_order_product_id, sale_order=sale_order)
    inventory_count = Master.objects.filter(product_id=sale_order_product.product_id,status='active').count()
    selected_master_uuids = sale_order_product.uuids
    form = AddUUIDForm(request.POST)
    product = sale_order_product.product
    selected_master_uuids_count = len(selected_master_uuids)
    if selected_master_uuids_count == sale_order_product.quantity:
        sale_order_product.status = 'complete'
        sale_order_product.save()    
    return render(request, 'sale_order_product_detail.html', {'sale_order': sale_order, 'sale_order_product': sale_order_product, 'inventory_count': inventory_count, 'selected_master_uuids': selected_master_uuids ,'form': form,'product':product,'selected_master_uuids_count':selected_master_uuids_count})


@login_required(login_url='managment/login/')
@allowed_users(allowed_roles=['admins', 'outlet_user',])
def add_uuid(request, bill_no, sale_order_product_id):
    if request.method == 'POST':
        new_uuid = request.POST.get('new_uuid')
        sale_order = get_object_or_404(SaleOrder, bill_no=bill_no)
        sale_order_product = get_object_or_404(SaleOrderProduct, product_id=sale_order_product_id, sale_order=sale_order)
        print(sale_order)

        if new_uuid in sale_order_product.uuids:
            messages.error(request, f"UUID '{new_uuid}' is already in the list.")
            return redirect('sale_order_product_detail', bill_no=bill_no, sale_order_product_id=sale_order_product_id)

        matching_master = Master.objects.filter(product=sale_order_product.product, uuid=new_uuid).first()

        if not matching_master:
            messages.error(request, f"UUID '{new_uuid}' does not match the product in the sale order.")
        elif matching_master.status != 'active':
            messages.error(request, f"UUID '{new_uuid}' is not active for the product.")
        else:
            sale_order_product.uuids.append(new_uuid)
            sale_order_product.save()

    return redirect('sale_order_product_detail', bill_no=bill_no, sale_order_product_id=sale_order_product_id)






def save_and_return(request, bill_no, sale_order_product_id):
    sale_order = get_object_or_404(SaleOrder, bill_no=bill_no)
    sale_order_product = get_object_or_404(SaleOrderProduct, id=sale_order_product_id, sale_order=sale_order)

    
    appended_data = {
        "added_by": request.user.username,  
        "added_date_time": timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        "Bill_no": sale_order.bill_no,
        "Veichal_no": sale_order.vehicle_no,
        "bill_no": sale_order.bill_no,
        "po_number": sale_order.po_number,
    }

    for _ in sale_order_product.uuids:
        master = Master.objects.get(uuid=_)
        print(master)
        master_data = master.data_json or {}
        outlet_data = master_data.get('outlet', {})  
        outlet_data[bill_no] = appended_data
        master_data['outlet'] = outlet_data

        master.data_json = master_data
        master.status = 'deactive'
        master.save()
        sale_order.uuids.append(str(master.uuid))
    sale_order.save()
    
    
    if sale_order_product.quantity == len(sale_order_product.uuids):
        sale_order_product.status = 'complete'
        sale_order_product.save()
    
    return redirect('sale_order_detail', bill_no=bill_no)


def remove_uuid(request, bill_no, sale_order_product_id):
    if request.method == 'POST':
        removed_uuid = request.POST.get('removed_uuid')
        sale_order = get_object_or_404(SaleOrder, bill_no=bill_no)
        sale_order_product = get_object_or_404(SaleOrderProduct, product_id=sale_order_product_id, sale_order=sale_order)

        if removed_uuid in sale_order_product.uuids:
            sale_order_product.uuids.remove(removed_uuid)
            specific_master = sale_order_product.product.master_set.filter(uuid=removed_uuid).first()
            
            if specific_master:
                master_data = specific_master.data_json or {}
                outlet_data = master_data.get('outlet', {})
                

                if bill_no in outlet_data:
                    del outlet_data[bill_no]

                master_data['outlet'] = outlet_data
                specific_master.data_json = master_data
                specific_master.status = 'active'
                if removed_uuid in sale_order.uuids:
                    sale_order.uuids.remove(removed_uuid)
                    sale_order.save()

                print(specific_master.save())
                print(sale_order_product.save())

    return redirect('sale_order_product_detail', bill_no=bill_no, sale_order_product_id=sale_order_product_id)

