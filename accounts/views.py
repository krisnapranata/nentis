from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from accounts.forms import UserForm
from accounts.models import User


def is_admin(user):
    return user.role == 'admin'


@login_required
@user_passes_test(is_admin, login_url='/accounts/login/')
def user_list(request):
    users = User.objects.all().order_by('role', 'username')
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required
@user_passes_test(is_admin, login_url='/accounts/login/')
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            else:
                user.set_unusable_password()
            user.save()
            messages.success(request, f'User "{user.username}" berhasil ditambahkan.')
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Tambah User'})


@login_required
@user_passes_test(is_admin, login_url='/accounts/login/')
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            messages.success(request, f'User "{user.username}" berhasil diperbarui.')
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'accounts/user_form.html', {
        'form': form, 'title': 'Edit User', 'edit_user': user,
    })


@login_required
@user_passes_test(is_admin, login_url='/accounts/login/')
def user_toggle(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.id == request.user.id:
        messages.error(request, 'Anda tidak bisa menonaktifkan akun sendiri.')
        return redirect('user_list')
    user.is_active = not user.is_active
    user.save()
    state = 'diaktifkan' if user.is_active else 'dinonaktifkan'
    messages.success(request, f'User "{user.username}" {state}.')
    return redirect('user_list')
