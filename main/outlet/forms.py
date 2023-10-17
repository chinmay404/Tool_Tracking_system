from django import forms
from .models import SaleOrder, SaleOrderProduct

class SaleOrderForm(forms.ModelForm):
    class Meta:
        model = SaleOrder
        fields = ['grn_number', 'po_number', 'bill_no', 'vehicle_no']

    product_quantities = forms.ModelMultipleChoiceField(
        queryset=SaleOrderProduct.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(SaleOrderForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            initial_data = self.instance.saleorderproduct_set.values_list('product', 'quantity')
            self.fields['product_quantities'].initial = initial_data

    def save(self, commit=True):
        instance = super(SaleOrderForm, self).save(commit=False)
        if commit:
            instance.save()

        # Update product quantities
        selected_product_quantities = self.cleaned_data['product_quantities']
        instance.saleorderproduct_set.all().delete()  # Clear existing product quantities

        for product, quantity in selected_product_quantities:
            SaleOrderProduct.objects.create(sale_order=instance, product=product, quantity=quantity)

        return instance
