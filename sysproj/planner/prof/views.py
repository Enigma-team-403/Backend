from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import UserProfile
from .forms import UserProfileForm, UserForm, PasswordChangeForm

from rest_framework import viewsets
from .serializers import UserProfileSerializer

class UserProfileViewSet(viewsets.ModelViewSet): 
    queryset = UserProfile.objects.all() 
    serializer_class = UserProfileSerializer

@login_required
def view_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'prof/view_profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('view_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    return render(request, 'prof/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            if not request.user.check_password(old_password):
                form.add_error('old_password', "Old password is incorrect.")
            else:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)  # مهم برای حفظ لاگین کاربر
                return redirect('view_profile')
    else:
        form = PasswordChangeForm()
    return render(request, 'prof/change_password.html', {'form': form})
