from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone


@login_required
def dashboard(request):
    user = request.user
    if user.role == 'admisi' or user.role == 'admin':
        return redirect('admisi_dashboard')
    elif user.role == 'dokter':
        return redirect('dokter_dashboard')
    return render(request, 'dashboard/home.html')
