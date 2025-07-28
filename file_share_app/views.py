from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UploadFileForm, ProfileForm
from .models import UploadedFile, Profile
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'file_share_app/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.uploader = request.user
            upload.save()
            form.save_m2m()
            return redirect('dashboard')
    else:
        form = UploadFileForm()
    files = UploadedFile.objects.filter(uploader=request.user) | UploadedFile.objects.filter(shared_with=request.user)
    return render(request, 'file_share_app/dashboard.html', {'form': form, 'files': files})

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'file_share_app/profile.html', {'form': form, 'profile': profile})

@login_required
def search_users(request):
    query = request.GET.get('q')
    users = User.objects.filter(username__icontains=query) if query else []
    return render(request, 'file_share_app/user_search.html', {'users': users})

@login_required
def shared_files(request):
    files = UploadedFile.objects.filter(shared_with=request.user)
    return render(request, 'file_share_app/shared_files.html', {'files': files})
