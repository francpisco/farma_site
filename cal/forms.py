from django import forms

from .models import CalDia


class CalForm(forms.ModelForm):
    class Meta:
        model = CalDia
        fields = ['farmacia_de_servico', 'info']
        labels = {'farmacia_de_servico': 'Farmácia de Serviço', 'info': 'Outra informação'}