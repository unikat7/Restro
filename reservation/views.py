from django.shortcuts import render, redirect
from .forms import ReservationForm


def reservation_create(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservation:reservation_done')
    else:
        form = ReservationForm()
    return render(request, 'reservation/reservation_form.html', {'form': form})


def reservation_done(request):
    return render(request, 'reservation/reservation_done.html')
