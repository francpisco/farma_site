from django import forms

from .models import Entry


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'image', 'text']
        labels = {'title': 'Título', 'image': 'Foto', 'text': 'Texto'}
        # widgets = {
        #     'title': forms.TextInput(),
        #     'image': forms.FileInput(attrs={'id': 'image_field'}),
        #     'text': forms.Textarea()
        # }


class ContactForm(forms.Form):
    name = forms.CharField(label='Nome', required=True)
    phone_number = forms.CharField(label='tlf', required=False)
    from_email = forms.EmailField(label='e-mail', required=True)
    subject = forms.CharField(label='assunto', required=True)
    message = forms.CharField(label='mensagem', widget=forms.Textarea, required=True)