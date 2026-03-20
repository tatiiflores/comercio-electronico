from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Cliente, Proveedor, Producto, Venta, ImagenProducto
from .forms import ClienteForm, ProveedorForm, ProductoForm, VentaForm, ImagenProductoFormSet

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
