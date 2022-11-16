from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect

from farma_site.settings import MEDIA_URL

from .models import Entry, Servico
from .forms import EntryForm, ContactForm



def index(request):
    """The home page."""
    entries = Entry.objects.order_by('-date_added')[:3]
    servicos = Servico.objects.order_by('id')
    context = {'entries': entries, 'servicos': servicos}
    return render(request, 'farma_site_app/index.html', context)

def blog(request):
    """The blog page."""
    object_list = Entry.objects.order_by('-date_added')
    paginator = Paginator(object_list, 10)  # 10 posts in each page
    page = request.GET.get('page')
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        # If page not an integer deliver the first page
        entries = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        entries = paginator.page(paginator.num_pages)
    context = {'entries': entries, 'page': page}
    return render(request, 'farma_site_app/blog.html', context)

def entry(request, entry_id):
    """Show a single entry(entrada)."""
    entry = Entry.objects.get(id=entry_id)
    context = {'entry': entry}
    return render(request, 'farma_site_app/entry.html', context)

@login_required
def new_entry(request):
    """Add a new entry to the blog."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('farma_site_app:blog')
    
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'farma_site_app/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit and existing entry."""
    entry = Entry.objects.get(id=entry_id)
    if request.method != 'POST':
        # Initial request; pre-fill form with current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('farma_site_app:blog')
    
    context = {'entry': entry, 'form': form}
    return render(request, 'farma_site_app/edit_entry.html', context)


def contacto(request):
    """Contacto page"""
    if request.method != 'POST':
        form = ContactForm()
    else:
        form = ContactForm(data=request.POST)
        if form.is_valid():
            subject = (form.cleaned_data['subject'] 
                       + ', Nome: ' + form.cleaned_data['name'] 
                       + ', tlf: ' + form.cleaned_data['phone_number'])
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ["franciscopiscoalmeida@gmail.com"])
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            return redirect('farma_site_app:sucesso')
    return render(request, 'farma_site_app/contacto.html', {'form': form})


def sucesso(request):
    return render(request, 'farma_site_app/sucesso.html')
    # return HttpResponse("Sucesso! Obrigado pela sua mensagem.")