from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('lobby/', views.lobby_view, name='lobby'),
    path('logout/', views.logout_view, name='logout'),
    path('productos/', views.productos_view, name='productos'),
    path('citas/', views.listar_citas, name='listar_citas'),
    path('agendar/', views.agendar_cita, name='agendar_cita'),
    path('grupo/', views.grupo_view, name='grupo'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/add/<int:producto_id>/', views.agregar_a_carrito, name='agregar_a_carrito'),
    path('carrito/remove/<int:item_id>/', views.eliminar_de_carrito, name='eliminar_de_carrito'),
    path('citas/remove/<int:cita_id>/', views.eliminar_cita, name='eliminar_cita'),
    path('citas/remove_cumplidas/', views.eliminar_citas_cumplidas, name='eliminar_citas_cumplidas'),
    path('citas/cancel/<int:cita_id>/', views.cancelar_cita, name='cancelar_cita'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('historial/', views.historial_compras_view, name='historial_compras'),
    path('reviews/delete/<int:review_id>/', views.delete_review, name='delete_review'),

]
