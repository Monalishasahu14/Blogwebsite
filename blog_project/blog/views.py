from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import BlogPost, UserProfile
from .forms import BlogPostForm, UserRegisterForm, UserProfileForm
from django.contrib import messages
from django.db.models import F

def home(request):
    blogs = BlogPost.objects.all().select_related('author')
    return render(request, 'home.html', {'blogs': blogs})

def blog_detail(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)
    # Increment view count safely
    BlogPost.objects.filter(pk=blog.pk).update(view_count=F('view_count') + 1)
    blog.refresh_from_db()
    return render(request, 'blog_detail.html', {'blog': blog})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create empty profile
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        form.fields['username'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Username'})
        form.fields['password'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Password'})
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    blogs = BlogPost.objects.filter(author=request.user)
    return render(request, 'dashboard.html', {'blogs': blogs})

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'profile.html', {'form': form, 'profile': profile})

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()  # Slug is generated on save
            messages.success(request, "Blog created successfully!")
            return redirect('dashboard')
    else:
        form = BlogPostForm()
    return render(request, 'create_blog.html', {'form': form, 'title': 'Create Blog'})

@login_required
def edit_blog(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)
    if blog.author != request.user:
        messages.error(request, "You serve no authority here!")
        return redirect('home')
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog updated successfully!")
            return redirect('dashboard')
    else:
        form = BlogPostForm(instance=blog)
    return render(request, 'create_blog.html', {'form': form, 'title': 'Edit Blog'})

@login_required
def delete_blog(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)
    if blog.author == request.user:
        blog.delete()
        messages.success(request, "Blog deleted successfully!")
    else:
        messages.error(request, "You cannot delete this blog.")
    return redirect('dashboard')
