from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from tienda.models import Proveedor, Producto, ImagenProducto
import os
from pathlib import Path

class Command(BaseCommand):
    help = 'Carga datos de prueba con imágenes en la base de datos'

    def handle(self, *args, **options):
        # Crear proveedores
        proveedor1, _ = Proveedor.objects.get_or_create(
            nombre='TechStore',
            defaults={
                'empresa': 'TechStore Inc.',
                'telefono': '123456789',
                'email': 'contacto@techstore.com'
            }
        )
        
        proveedor2, _ = Proveedor.objects.get_or_create(
            nombre='ElectrónicaMax',
            defaults={
                'empresa': 'ElectrónicaMax SRL',
                'telefono': '987654321',
                'email': 'info@electronicamax.com'
            }
        )
        
        self.stdout.write(self.style.SUCCESS('Proveedores creados'))
        
        # Rutas de imágenes estáticas
        static_images_dir = Path(__file__).resolve().parent.parent.parent.parent / 'static' / 'images'
        
        productos_data = [
            {
                'nombre': 'Laptop Gaming',
                'descripcion': 'Potente laptop para gaming con procesador de última generación',
                'precio': 1500.00,
                'stock': 10,
                'proveedor': proveedor1,
                'imagen': 'oferta1.jpg'
            },
            {
                'nombre': 'Monitor 4K',
                'descripcion': 'Monitor de 27 pulgadas con resolución 4K y frecuencia de 144Hz',
                'precio': 450.00,
                'stock': 15,
                'proveedor': proveedor2,
                'imagen': 'oferta2.jpg'
            },
            {
                'nombre': 'Mouse Inalámbrico',
                'descripcion': 'Mouse inalámbrico de alta precisión para gaming',
                'precio': 75.00,
                'stock': 50,
                'proveedor': proveedor1,
                'imagen': 'oferta3.jpg'
            },
            {
                'nombre': 'Teclado Mecánico',
                'descripcion': 'Teclado mecánico RGB para gaming profesional',
                'precio': 120.00,
                'stock': 30,
                'proveedor': proveedor2,
                'imagen': 'tienda.jpg'
            },
        ]
        
        for prod_data in productos_data:
            imagen_archivo = prod_data.pop('imagen')
            imagen_path = static_images_dir / imagen_archivo
            
            producto, created = Producto.objects.get_or_create(
                nombre=prod_data['nombre'],
                defaults=prod_data
            )
            
            if created and imagen_path.exists():
                with open(imagen_path, 'rb') as f:
                    producto.imagen_principal.save(
                        imagen_archivo,
                        ContentFile(f.read()),
                        save=True
                    )
                self.stdout.write(f'Producto creado: {producto.nombre}')
        
        self.stdout.write(self.style.SUCCESS('Datos cargados exitosamente'))
