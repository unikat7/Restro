from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'order_type', 'address', 'city', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'order_type': forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'order_type':
                field.widget.attrs.setdefault('class', 'form-control')

    def clean(self):
        cleaned_data = super().clean()
        order_type = cleaned_data.get('order_type')
        address = cleaned_data.get('address')
        if order_type == 'delivery' and not address:
            self.add_error('address', 'Address is required for delivery orders.')
        return cleaned_data
