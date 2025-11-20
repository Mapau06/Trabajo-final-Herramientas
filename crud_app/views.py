from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Cita, CarritoItem, Orden, DetalleOrden, Review
from .forms import CitaForm, CheckoutForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, DecimalField
from decimal import Decimal
from django.utils import timezone
from django.db.models import Q
from itertools import groupby
from django.contrib import messages
from django.db import IntegrityError


# Lista global de productos usada por las vistas
PRODUCTS = [
    {'id': 1, 'nombre': 'Alimento para perros y gatos', 'descripcion': 'Incluye comida seca, húmeda y dietas especializadas para necesidades médicas específicas', 'precio': 85000, 'imagen': 'https://cdn.shopify.com/s/files/1/0560/3241/files/Kibble-01_grande.jpg?13060827728408065915'},
    {'id': 2, 'nombre': 'Juguetes', 'descripcion': 'Pelotas, mordederas, juguetes interactivos y de inteligencia para mantener a las mascotas activas y entretenidas', 'precio': 15000, 'imagen': 'https://exitocol.vtexassets.com/arquivos/ids/23797481/kit-x6-juguetes-para-perros-diversion-y-bienestar-asegurados.jpg?v=638573663040400000'},
    {'id': 3, 'nombre': 'Collar antipulgas', 'descripcion': 'Protección por 6 meses', 'precio': 30000, 'imagen': 'https://kanu.pet/cdn/shop/files/PRODUCTOSKANU2_16_c94acc70-5d8c-41b9-8da0-c6e627f15dd3.png?v=1748370922'},
    {'id': 4, 'nombre': 'Correas y arneses', 'descripcion': 'Articulos basicos para paseos y sujecion, disponilbes en diferentes tamaños', 'precio': 10000, 'imagen': 'https://petopet.com.co/cdn/shop/products/LPM-080_ARNES_TONO_PASTEL12_600x600.jpg?v=1642883115'},
    {'id': 5, 'nombre': 'Camas y mantas', 'descripcion': 'Comodidad para el hogar, incluyendo camas ortopedicas para perros mayores', 'precio': 35000, 'imagen': 'https://cdn1.totalcommerce.cloud/homesentry/product-zoom/es/cama-perro-clark-39272-azul-claro-comedero~cobija~juguete~panal-1.webp'},
    {'id': 6, 'nombre': 'Transportador y jaulas', 'descripcion': 'Para viajes, visitas al veterinario o como espacios de descanso seguro', 'precio': 20000, 'imagen': 'https://images-na.ssl-images-amazon.com/images/I/81fDUndc8-L._AC_UL375_SR375,375_.jpg'},
    {'id': 7, 'nombre': 'Collares', 'descripcion': 'Collares con placas grabables para asegurar que las mascotas perdidas puedan ser identificadas y devueltas', 'precio': 9000, 'imagen': 'https://m.media-amazon.com/images/I/715nt0hD9rL.jpg'},
    {'id': 8, 'nombre': 'Accesorios de alimentacion', 'descripcion': 'Comederos y bebederos, incluyendo opciones para perros glotones o fuentes automáticas de agua', 'precio': 15000, 'imagen': 'https://resources.claroshop.com/medios-plazavip/mkt/5f93d54256df0_210m-3-csjpg.jpg'},
    {'id': 9, 'nombre': 'Suplementos y vitaminas', 'descripcion': 'Complementos para apoyar la salud general, el crecimiento o condiciones específicas de las articulaciones', 'precio': 30000, 'imagen': 'https://www.agrocampo.com.co/media/catalog/product/cache/d51e0dc10c379a6229d70d752fc46d83/5/8/5858658605860001742-min.jpg'},
    {'id': 10, 'nombre': 'Productos de higiene', 'descripcion': 'Champús, cepillos, cortaúñas, y productos para la higiene bucal', 'precio': 20000, 'imagen': 'https://http2.mlstatic.com/D_NQ_NP_952113-MCO81371804686_122024-O.webp'},
]

# ------------------ LOGIN ------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('lobby')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})

    return render(request, 'login.html')


# ------------------ REGISTRO ------------------
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Las contraseñas no coinciden.'})

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return redirect('lobby')
        except IntegrityError:
            return render(request, 'register.html', {'error': 'El usuario o email ya existe.'})
        except Exception:
            return render(request, 'register.html', {'error': 'Ocurrió un error al crear el usuario.'})

    return render(request, 'register.html')


# ------------------ LOBBY ------------------
@login_required
def lobby_view(request):
    reviews = Review.objects.all()[:5]  # Get last 5 reviews
    review_form = None
    
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.usuario = request.user
            review.save()
            messages.success(request, '¡Gracias por tu reseña!')
            return redirect('lobby')
    else:
        review_form = ReviewForm()
        
    context = {
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'lobby.html', context)


# ------------------ RESEÑAS ------------------
@login_required
def delete_review(request, review_id):
    """Permite al autor de la reseña o al staff eliminar una reseña.
    Solo acepta POST para evitar eliminaciones por GET.
    """
    review = Review.objects.filter(id=review_id).first()
    if not review:
        messages.error(request, 'La reseña no existe.')
        return redirect('lobby')

    # Permiso: autor o staff
    if not (request.user == review.usuario or request.user.is_staff):
        messages.error(request, 'No tienes permiso para eliminar esta reseña.')
        return redirect('lobby')

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Reseña eliminada correctamente.')
    return redirect('lobby')



# ------------------ LOGOUT ------------------
def logout_view(request):
    logout(request)
    return redirect('login')


# ------------------ PRODUCTOS ------------------
@login_required
def productos_view(request):
    # Usar la lista global PRODUCTS
    productos = PRODUCTS.copy()

    query = request.GET.get('q', '').strip()
    if query:
        productos = [p for p in productos if query.lower() in p['nombre'].lower()]

    context = {'productos': productos, 'query': query}
    return render(request, 'productos.html', context)


# ------------------ GRUPO ------------------
@login_required
def grupo_view(request):
    return render(request, 'grupo.html')

@login_required
def agendar_cita(request):
    # Mostrar formulario y, además, una lista compacta de citas ya cumplidas para eliminar
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_citas')
    else:
        form = CitaForm()

    # Determinar citas pasadas (cumplidas)
    now = timezone.localtime()
    today = now.date()
    current_time = now.time()

    past_citas = Cita.objects.filter(Q(fecha_cita__lt=today) | (Q(fecha_cita=today) & Q(hora_cita__lt=current_time))).order_by('-fecha_cita', '-hora_cita')

    return render(request, 'agendar_cita.html', {'form': form, 'past_citas': past_citas})

@login_required
def listar_citas(request):
    """
    Muestra las citas agrupadas por fecha (ascendente) y ordenadas por hora.
    También indica si existen citas cumplidas (pasadas) para ofrecer opción de eliminación.
    """
    # Orden ascendente por fecha y hora
    citas_qs = Cita.objects.all().order_by('fecha_cita', 'hora_cita')

    # Agrupar por fecha
    grouped = []
    now = timezone.localtime()
    today = now.date()
    current_time = now.time()

    for fecha, group in groupby(citas_qs, key=lambda c: c.fecha_cita):
        group_list = []
        for c in list(group):
            is_past = (c.fecha_cita < today) or (c.fecha_cita == today and c.hora_cita < current_time)
            group_list.append({'cita': c, 'is_past': is_past})
        grouped.append((fecha, group_list))

    # Determinar si hay citas pasadas (cumplidas)
    has_past = any(any(item['is_past'] for item in group_list) for _, group_list in grouped)

    return render(request, 'listar_citas.html', {'grouped_citas': grouped, 'has_past': has_past})


@login_required
def eliminar_cita(request, cita_id):
    # Elimina una cita por su id y redirige a la lista
    Cita.objects.filter(id=cita_id).delete()
    return redirect('listar_citas')

@login_required
def cancelar_cita(request, cita_id):
    """Cancela una cita pendiente antes de su fecha programada"""
    cita = Cita.objects.filter(id=cita_id).first()
    if cita:
        # Verificar que la cita sea futura
        now = timezone.localtime()
        if cita.fecha_cita > now.date() or (cita.fecha_cita == now.date() and cita.hora_cita > now.time()):
            cita.delete()
    return redirect('listar_citas')


@login_required
def eliminar_citas_cumplidas(request):
    # Elimina todas las citas que ya pasaron (fecha anterior o hoy con hora anterior)
    now = timezone.localtime()
    today = now.date()
    current_time = now.time()

    Cita.objects.filter(Q(fecha_cita__lt=today) | (Q(fecha_cita=today) & Q(hora_cita__lt=current_time))).delete()
    return redirect('listar_citas')

# crud_app/views.py (AÑADIR ESTAS VISTAS AL FINAL)

# ------------------ CARRITO ------------------

@login_required
def agregar_a_carrito(request, producto_id):
    # Buscar el producto dentro de la lista global PRODUCTS
    try:
        producto_seleccionado = next(p for p in PRODUCTS if p['id'] == producto_id)

        # Convertir precio a Decimal para el campo DecimalField del modelo
        precio_decimal = Decimal(str(producto_seleccionado['precio']))

        # Intenta encontrar el ítem en el carrito del usuario
        item = CarritoItem.objects.filter(
            usuario=request.user, 
            producto_id=producto_id
        ).first()

        if item:
            item.cantidad += 1
            item.save()
        else:
            CarritoItem.objects.create(
                usuario=request.user,
                producto_id=producto_id,
                nombre_producto=producto_seleccionado['nombre'],
                precio=precio_decimal,
                cantidad=1
            )
            
        messages.success(request, 'Producto agregado al carrito exitosamente')
        return redirect('productos')
    
    except StopIteration:
        messages.error(request, 'El producto no existe')
        return redirect('productos')

@login_required
def ver_carrito(request):
    items = CarritoItem.objects.filter(usuario=request.user)
    # Calcula el total del carrito
    total = items.aggregate(total=Sum(F('precio') * F('cantidad'), output_field=DecimalField()))['total'] or 0
    
    return render(request, 'carrito.html', {'items': items, 'total': total})

@login_required
def eliminar_de_carrito(request, item_id):
    CarritoItem.objects.filter(id=item_id, usuario=request.user).delete()
    return redirect('ver_carrito')


# ------------------ CHECKOUT Y ORDENES ------------------

@login_required
def checkout_view(request):
    items = CarritoItem.objects.filter(usuario=request.user)
    if not items.exists():
        return redirect('ver_carrito') # No se puede hacer checkout con carrito vacío

    total = items.aggregate(total=Sum(F('precio') * F('cantidad'), output_field=DecimalField()))['total'] or 0

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # 1. Crear la Orden
            orden = Orden.objects.create(
                usuario=request.user,
                total_orden=total,
                nombre_cliente=form.cleaned_data['nombre_cliente'],
                telefono=form.cleaned_data['telefono'],
                documento=form.cleaned_data['documento'],
                direccion_envio=form.cleaned_data['direccion_envio']
            )

            # 2. Mover Items del Carrito a DetalleOrden
            for item in items:
                DetalleOrden.objects.create(
                    orden=orden,
                    nombre_producto=item.nombre_producto,
                    precio_unitario=item.precio,
                    cantidad=item.cantidad
                )
            
            # 3. Vaciar el Carrito
            items.delete()

            # 4. Redirigir al historial (o a una página de confirmación)
            return redirect('historial_compras')
    else:
        form = CheckoutForm()

    context = {
        'items': items,
        'total': total,
        'form': form
    }
    return render(request, 'checkout.html', context)


@login_required
def historial_compras_view(request):
    ordenes = Orden.objects.filter(usuario=request.user).order_by('-fecha_orden')
    return render(request, 'historial_compras.html', {'ordenes': ordenes})



