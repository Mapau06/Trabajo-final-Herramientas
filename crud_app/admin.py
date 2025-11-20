from django.contrib import admin
from .models import Cita, Orden, DetalleOrden, CarritoItem, Review


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombre_mascota', 'nombre_cliente', 'fecha_cita', 'hora_cita')
	search_fields = ('nombre_mascota', 'nombre_cliente', 'telefono', 'documento')
	list_filter = ('fecha_cita', 'tipo_mascota')


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
	list_display = ('id', 'usuario', 'fecha_orden', 'total_orden')
	search_fields = ('usuario__username', 'nombre_cliente', 'documento')
	list_filter = ('fecha_orden',)


@admin.register(DetalleOrden)
class DetalleOrdenAdmin(admin.ModelAdmin):
	list_display = ('id', 'orden', 'nombre_producto', 'precio_unitario', 'cantidad')
	search_fields = ('nombre_producto',)


@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
	list_display = ('id', 'usuario', 'nombre_producto', 'precio', 'cantidad')
	search_fields = ('usuario__username', 'nombre_producto')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ('id', 'usuario', 'calificacion', 'fecha_creacion')
	search_fields = ('usuario__username', 'contenido')
	list_filter = ('calificacion', 'fecha_creacion')
