from django.shortcuts import redirect, render
from .models import MusicFile
from .forms import MusicFileForm, UserRegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_music = MusicFile.objects.filter(user=request.user)
    public_music = MusicFile.objects.filter(upload_type='public')
    # private_music = MusicFile.objects.filter(upload_type='private')
    protected_music = MusicFile.objects.filter(upload_type='protected').filter(
        allowed_emails__contains=request.user.email)

    context = {'user_files': user_music, 'public_files': public_music,
               'protected_files': protected_music}
    return render(request, 'music_app/home.html', context)


def login_user(request):
    if request.method == 'POST':
        # Handle login form submission
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            authenticated_user = authenticate(
                request, username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')

        pass
    return render(request, 'music_app/login.html')


def logout_user(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':
        # Handle register form submission
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
        else:
            messages.error(request, 'An error occurred during registration')
    else:
        form = UserRegisterForm()

    return render(request, 'music_app/register.html', {'form': form})


def upload(request):
    if request.method == 'POST':
        form = MusicFileForm(request.POST, request.FILES)
        if form.is_valid():
            music_file = form.save(commit=False)
            music_file.user = request.user  # Set the current user
            music_file.url = music_file.file.url
            music_file.save()
            # Handle successful form submission (e.g., redirect to a success page)
            return redirect('home')
        else:
            errors = form.errors.values()
            print(errors)
            # form = MusicFileForm()  # Create a new form instance to render in the template
            # error_message = ", ".join(list(errors))
            # return render(request, 'music_app/upload.html', {'form': form, 'error_message': error_message})

    else:
        form = MusicFileForm()

    return render(request, 'music_app/upload.html', {'form': form})
