from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Salesperson, Product, Customer, Sales

class SalespersonForm(forms.ModelForm):
    class Meta:
        model = Salesperson
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'termination_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(SalespersonForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

    #def clean(self):
        #cleaned_data = super().clean()
        #first_name = cleaned_data.get('first_name')
        #last_name = cleaned_data.get('last_name')
        #if Salesperson.objects.filter(first_name=first_name, last_name=last_name).exists():
            #raise forms.ValidationError('A salesperson with this name already exists.')
        #return cleaned_data

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = '__all__'
        widgets = {
            'sales_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the 'price' field read-only
        self.fields['price'].widget.attrs['readonly'] = True

