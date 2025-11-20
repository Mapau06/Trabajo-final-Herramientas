from django import forms
from .models import Cita, Review

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['nombre_cliente', 'telefono', 'documento', 'nombre_mascota', 'tipo_mascota', 'fecha_cita', 'hora_cita', 'descripcion']
        widgets = {
            'nombre_cliente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono de contacto'}),
            'documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Documento de identidad'}),
            'nombre_mascota': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la mascota'}),
            'tipo_mascota': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Perro, Gato, etc.'}),
            'fecha_cita': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_cita': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'style': 'resize: none;', 'placeholder': 'Motivo de la cita'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['contenido', 'calificacion']
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Comparte tu experiencia en VetCare...'}),
            'calificacion': forms.Select(attrs={'class': 'form-select'})
        }

class CheckoutForm(forms.Form):
    nombre_cliente = forms.CharField(
        max_length=100,
        label='Nombre Completo',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    telefono = forms.CharField(
        max_length=20,
        label='Teléfono de Contacto',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    documento = forms.CharField(
        max_length=20,
        label='Documento de Identidad',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    direccion_envio = forms.CharField(
        label='Dirección de Envío',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'style': 'resize: none;',
            'placeholder': 'Ingrese su dirección completa'
        })
    )
    
    PAYMENT_CHOICES = [
        ('card', 'Tarjeta de crédito'),
        ('nequi', 'Nequi (transferencia)'),
        ('applepay', 'Apple Pay'),
        ('paypal', 'PayPal'),
    ]

    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect, label='Método de Pago')

    # Campos opcionales para tarjeta (se requieren solo si payment_method == 'card')
    card_number = forms.CharField(max_length=19, required=False, label='Número de Tarjeta')
    card_expiry = forms.CharField(max_length=7, required=False, label='Fecha de expiración (MM/AA)')
    card_cvv = forms.CharField(max_length=4, required=False, label='CVV')

    def clean(self):
        cleaned = super().clean()
        method = cleaned.get('payment_method')

        if method == 'card':
            card_number = cleaned.get('card_number')
            card_expiry = cleaned.get('card_expiry')
            card_cvv = cleaned.get('card_cvv')

            if not card_number or not card_expiry or not card_cvv:
                raise forms.ValidationError('Para pagar con tarjeta, complete los datos de la tarjeta.')

            # Validaciones simples
            digits = ''.join(ch for ch in card_number if ch.isdigit())
            if len(digits) < 13 or len(digits) > 19:
                self.add_error('card_number', 'Número de tarjeta inválido')

            if len(card_cvv) not in (3, 4) or not card_cvv.isdigit():
                self.add_error('card_cvv', 'CVV inválido')

            # expiry simple MM/YY
            try:
                mm, yy = card_expiry.replace('/', ' ').split()
                mm = int(mm)
                yy = int(yy)
                if mm < 1 or mm > 12:
                    self.add_error('card_expiry', 'Mes inválido')
            except Exception:
                self.add_error('card_expiry', 'Formato de expiración inválido (MM/AA)')

        return cleaned
