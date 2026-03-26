from django import forms
from django.forms import inlineformset_factory
from .models import Cliente, Proveedor, Producto, Venta, ImagenProducto

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'proveedor', 'imagen_principal']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'imagen_principal': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

ImagenProductoFormSet = inlineformset_factory(
    Producto, ImagenProducto,
    fields=('imagen', 'orden'),
    extra=3,
    can_delete=True,
    widgets={
        'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        'orden': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Orden'}),
    }
)

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'producto', 'cantidad']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class CheckoutForm(forms.Form):
    PAISES = [
        ('Argentina', 'Argentina'),
        ('Uruguay', 'Uruguay'),
        ('Chile', 'Chile'),
        ('Brasil', 'Brasil'),
    ]

    PROVINCIAS_ARGENTINAS = [
        ('Buenos Aires', 'Buenos Aires'),
        ('Córdoba', 'Córdoba'),
        ('Santa Fe', 'Santa Fe'),
        ('Mendoza', 'Mendoza'),
        ('Tucumán', 'Tucumán'),
        ('Salta', 'Salta'),
        ('Jujuy', 'Jujuy'),
        ('Misiones', 'Misiones'),
        ('Entre Ríos', 'Entre Ríos'),
        ('Corrientes', 'Corrientes'),
        ('San Juan', 'San Juan'),
        ('San Luis', 'San Luis'),
        ('La Pampa', 'La Pampa'),
        ('Neuquén', 'Neuquén'),
        ('Río Negro', 'Río Negro'),
        ('Chubut', 'Chubut'),
        ('Santa Cruz', 'Santa Cruz'),
        ('Tierra del Fuego', 'Tierra del Fuego'),
    ]

    pais = forms.ChoiceField(choices=PAISES, initial='Argentina', widget=forms.Select(attrs={'class': 'form-select'}))
    provincia = forms.ChoiceField(choices=PROVINCIAS_ARGENTINAS, widget=forms.Select(attrs={'class': 'form-select'}))
    ciudad = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    direccion = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
