from django.shortcuts import render, redirect
from django.contrib import messages
from menu.models import MenuItem, Category
from .forms import ContactForm


def home(request):
    specials = MenuItem.objects.filter(is_special=True, is_available=True)[:6]
    categories = Category.objects.all()[:6]
    return render(request, 'core/home.html', {'specials': specials, 'categories': categories})


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks! Your message has been sent. We'll get back to you soon.")
            return redirect('core:contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})
