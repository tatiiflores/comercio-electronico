from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal
from .models import Cliente, Proveedor, Producto, Venta, ImagenProducto
from .forms import ClienteForm, ProveedorForm, ProductoForm, VentaForm, ImagenProductoFormSet, CheckoutForm

# Vistas públicas (Sprint 1 y 2)
def index(request):
    return render(request, 'index.html')

def acercade(request):
    return render(request, 'acercade.html')

def contacto(request):
    return render(request, 'contacto.html')

class ProductoListView(ListView):
    model = Producto
    template_name = 'productos.html'
    context_object_name = 'productos'
    paginate_by = 12

    def get_queryset(self):
        return Producto.objects.prefetch_related('imagenes').all()


def _cart_items(request):
    cart = request.session.get('cart', {})
    items = []
    total = Decimal('0.00')
    for pid_str, data in cart.items():
        try:
            producto = Producto.objects.get(pk=int(pid_str))
        except (Producto.DoesNotExist, ValueError):
            continue
        cantidad = data.get('quantity', 0)
        subtotal = producto.precio * cantidad
        items.append({
            'producto': producto,
            'quantity': cantidad,
            'precio': producto.precio,
            'subtotal': subtotal,
        })
        total += subtotal
    return items, total


def add_to_cart(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        try:
            cantidad = int(request.POST.get('quantity', 1))
        except ValueError:
            cantidad = 1
        if cantidad < 1:
            cantidad = 1
        cart = request.session.get('cart', {})
        key = str(producto_id)
        cart[key] = {'quantity': cart.get(key, {}).get('quantity', 0) + cantidad}
        request.session['cart'] = cart
        messages.success(request, f'Agregaste {cantidad} unidad(es) de {producto.nombre} al carrito.')
    return redirect('productos')


def remove_from_cart(request, producto_id):
    cart = request.session.get('cart', {})
    key = str(producto_id)
    if key in cart:
        del cart[key]
        request.session['cart'] = cart
        messages.success(request, 'Producto eliminado del carrito.')
    return redirect('carrito')


def update_cart(request, producto_id):
    if request.method == 'POST':
        try:
            cantidad = int(request.POST.get('quantity', 1))
        except ValueError:
            cantidad = 1
        cart = request.session.get('cart', {})
        key = str(producto_id)
        if cantidad > 0:
            if key in cart:
                cart[key]['quantity'] = cantidad
                request.session['cart'] = cart
                messages.success(request, 'Cantidad actualizada.')
        else:
            if key in cart:
                del cart[key]
                request.session['cart'] = cart
                messages.warning(request, 'Producto eliminado porque la cantidad se puso en 0.')
    return redirect('carrito')


def carrito(request):
    items, total = _cart_items(request)
    if items:
        descripcion = ', '.join(f"{item['quantity']} {item['producto'].nombre}" for item in items)
        resumen_texto = f"Estás comprando {descripcion}. Total: ${total:.2f}"
    else:
        resumen_texto = 'Tu carrito está vacío.'
    return render(request, 'carrito.html', {
        'items': items,
        'total': total,
        'resumen_texto': resumen_texto,
    })


def checkout(request):
    items, total = _cart_items(request)
    if not items:
        messages.warning(request, 'El carrito está vacío. Agrega productos antes de iniciar el checkout.')
        return redirect('productos')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            request.session['checkout_data'] = form.cleaned_data
            return redirect('checkout_success')
    else:
        checkout_data = request.session.get('checkout_data', {})
        form = CheckoutForm(initial=checkout_data)

    return render(request, 'checkout.html', {
        'items': items,
        'total': total,
        'form': form,
    })


def checkout_success(request):
    items, total = _cart_items(request)
    checkout_data = request.session.get('checkout_data')

    if not checkout_data or not items:
        messages.warning(request, 'No hay información de checkout o el carrito está vacío.')
        return redirect('productos')

    # Guardar venta en la base de datos (opcional básico)
    # se podría crear Cliente/Venta aquí si ya se requiere persistencia.
    request.session['cart'] = {}

    return render(request, 'checkout_success.html', {
        'items': items,
        'total': total,
        'checkout_data': checkout_data,
    })

# Vistas de gestión (Sprint 3) con LoginRequiredMixin
class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'tienda/cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(Q(nombre__icontains=q) | Q(apellido__icontains=q))
        return queryset

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'tienda/cliente_form.html'
    success_url = reverse_lazy('cliente_list')

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'tienda/cliente_form.html'
    success_url = reverse_lazy('cliente_list')

class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'tienda/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente_list')

# Proveedores (similar)
class ProveedorListView(LoginRequiredMixin, ListView):
    model = Proveedor
    template_name = 'tienda/proveedor_list.html'
    context_object_name = 'proveedores'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(nombre__icontains=q)
        return queryset

class ProveedorCreateView(LoginRequiredMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'tienda/proveedor_form.html'
    success_url = reverse_lazy('proveedor_list')

class ProveedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'tienda/proveedor_form.html'
    success_url = reverse_lazy('proveedor_list')

class ProveedorDeleteView(LoginRequiredMixin, DeleteView):
    model = Proveedor
    template_name = 'tienda/proveedor_confirm_delete.html'
    success_url = reverse_lazy('proveedor_list')

# Productos con manejo de imágenes
class ProductoListViewGest(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'tienda/producto_list.html'
    context_object_name = 'productos'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(nombre__icontains=q)
        return queryset

class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'tienda/producto_form.html'
    success_url = reverse_lazy('producto_list_gest')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['imagenes'] = ImagenProductoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['imagenes'] = ImagenProductoFormSet(instance=self.object)
        return data

class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'tienda/producto_form.html'
    success_url = reverse_lazy('producto_list_gest')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['imagenes'] = ImagenProductoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['imagenes'] = ImagenProductoFormSet(instance=self.object)
        return data

class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'tienda/producto_confirm_delete.html'
    success_url = reverse_lazy('producto_list_gest')

class VentaListView(LoginRequiredMixin, ListView):
    model = Venta
    template_name = 'tienda/venta_list.html'
    context_object_name = 'ventas'
class VentaCreateView(LoginRequiredMixin, CreateView):
    model = Venta
    form_class = VentaForm
    template_name = 'tienda/venta_form.html'
    success_url = reverse_lazy('venta_list')
class VentaUpdateView(LoginRequiredMixin, UpdateView):
    model = Venta
    form_class = VentaForm
    template_name = 'tienda/venta_form.html'
    success_url = reverse_lazy('venta_list')
class VentaDeleteView(LoginRequiredMixin, DeleteView):
    model = Venta
    template_name = 'tienda/venta_confirm_delete.html'
    success_url = reverse_lazy('venta_list')
class VentaDetailView(LoginRequiredMixin, DetailView):
    model = Venta
    template_name = 'tienda/venta_detail.html'
    context_object_name = 'venta'
