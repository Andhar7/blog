from django.shortcuts import redirect, render
from assignments.models import About
from blog_main.forms import RegisterForm
from blogs.models import Blog 
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache


def home(request):
    # categories = Category.objects.all() # Moved to context processor
    featured_posts = Blog.objects.filter(is_featured=True, status='Published').order_by('updated_at')
    # featured_posts = Blog.objects.filter(is_featured=True)
    posts = Blog.objects.filter(is_featured=False, status='Published') 
    
    # Fetch about section content
    try:
        about = About.objects.get()
    except:
        about = None
    
    context = {
        # 'categories': categories, # Moved to context processor
        'featured_posts': featured_posts,
        'posts': posts,
        'about': about,
    }
    # print(featured_posts)
    # print(categories)
    return render(request, 'home.html', context) 

@never_cache
@csrf_protect
def register(request):
    """
    Handle user registration.
    
    Redirects authenticated users to home page.
    Processes registration form and creates new user accounts.
    """
    # Redirect if user is already authenticated
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(
                    request, 
                    f'Account created successfully! Welcome, {user.username}!'
                )
                
                # Optional: Auto-login after registration
                auth_login(request, user)
                
                # Redirect to next page or home
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('home')
                
            except Exception as e:
                messages.error(request, 'Registration failed. Please try again.')
                # Log the error for debugging (in production)
                # logger.error(f"Registration error: {e}")
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    
    context = {
        'form': form,
        'next': request.GET.get('next', ''),
    }
    return render(request, 'register.html', context)
 

@never_cache
@csrf_protect
def login(request):
    """
    Handle user authentication and login.
    
    Redirects authenticated users to home page.
    Processes login form and authenticates users.
    """
    # Redirect if user is already authenticated
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    messages.success(request, f'Welcome back, {user.username}!')
                    
                    # Redirect to next page or home
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    return redirect('home')
                else:
                    messages.error(request, 'Your account has been disabled.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form,
        'next': request.GET.get('next', ''),
    }
    return render(request, 'login.html', context)


# @login_required
# @never_cache
# def logout(request):
#     """
#     Handle user logout.
    
#     Logs out authenticated users and redirects to home page.
#     Requires user to be logged in.
#     """
#     if request.method == 'POST':
#         username = request.user.username
#         auth_logout(request)
#         messages.success(request, f'Goodbye {username}! You have been logged out successfully.')
        
#         # Redirect to next page or home
#         next_url = request.GET.get('next')
#         if next_url:
#             return redirect(next_url)
#         return redirect('home')
    
#     # If GET request, show confirmation page (optional)
#     return render(request, 'logout_confirm.html')

# Alternative: Simple logout function (most common approach)
@login_required  
@never_cache
def logout(request):
    """
    Simple logout function that works with GET requests.
    Immediately logs out the user and redirects.
    """
    username = request.user.username
    auth_logout(request)
    messages.success(request, f'Goodbye {username}! You have been logged out successfully.')
    return redirect('home')