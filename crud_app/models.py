from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Cita(models.Model):
    nombre_cliente = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    documento = models.CharField(max_length=20)
    nombre_mascota = models.CharField(max_length=100)
    tipo_mascota = models.CharField(max_length=50)
    fecha_cita = models.DateField()
    hora_cita = models.TimeField()
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_mascota} - {self.fecha_cita} {self.hora_cita}"

class Orden(models.Model):
    """Representa una orden de compra completada."""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_orden = models.DateTimeField(default=timezone.now)
    total_orden = models.DecimalField(max_digits=10, decimal_places=2)
    direccion_envio = models.TextField(blank=True, null=True)

    # Datos de contacto (duplicados para la historia de la orden)
    nombre_cliente = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    documento = models.CharField(max_length=20)

    def __str__(self):
        return f"Orden #{self.id} de {self.usuario.username}"

class DetalleOrden(models.Model):
    """Detalle de los productos dentro de una orden."""
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='detalles')
    nombre_producto = models.CharField(max_length=255) # Simulado
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.precio_unitario * self.cantidad
    
    def __str__(self):
        return f"{self.cantidad} x {self.nombre_producto} en Orden #{self.orden.id}"

class CarritoItem(models.Model):
    """Representa un producto en el carrito de un usuario."""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    # Campos que simulan un Producto
    producto_id = models.IntegerField() # Usaremos el índice del diccionario como ID
    # Campos añadidos para persistir nombre, precio y cantidad en el carrito
    nombre_producto = models.CharField(max_length=255, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.nombre_producto} (usuario={self.usuario.username})"

class Review(models.Model):
    """Representa una reseña de un cliente."""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    calificacion = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Reseña de {self.usuario.username} - {self.calificacion}⭐"

# Create your models here.
