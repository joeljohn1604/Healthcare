from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, AddressForm, BlogPostForm
from .models import User, BlogPost, Category
from django.utils.text import slugify

def signup(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST, request.FILES)
        address_form = AddressForm(request.POST)
        
        if user_form.is_valid() and address_form.is_valid():
            user = user_form.save()
            address = address_form.save(commit=False)
            address.user = user
            address.save()
            
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            return redirect('dashboard')
    else:
        user_form = UserRegistrationForm()
        address_form = AddressForm()
    
    return render(request, 'authentication/signup.html', {
        'user_form': user_form,
        'address_form': address_form
    })

def user_login(request):  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'authentication/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'authentication/login.html')

@login_required
def dashboard(request):
    user = request.user
    context = {
        'user': user,
        'address': user.address if hasattr(user, 'address') else None
    }
    
    if user.is_patient():
        return render(request, 'authentication/patient_dashboard.html', context)
    elif user.is_doctor():
        return render(request, 'authentication/doctor_dashboard.html', context)



def home(request):
    return render(request, 'authentication/home.html')

@login_required
def create_blog_post(request):
    if not request.user.is_doctor():
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('my_blog_posts')
    else:
        form = BlogPostForm()
    
    return render(request, 'authentication/create_blog_post.html', {'form': form})

@login_required
def my_blog_posts(request):
    if not request.user.is_doctor():
        return redirect('dashboard')
    
    blog_posts = BlogPost.objects.filter(author=request.user)
    for post in blog_posts:
        if not post.slug:
            post.slug = slugify(post.title)
            post.save()
    return render(request, 'authentication/my_blog_posts.html', {'blog_posts': blog_posts})

def blog_posts_by_category(request, category_slug=None):
    categories = Category.objects.all()
    blog_posts = BlogPost.objects.filter(status='published')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        blog_posts = blog_posts.filter(category=category)
    else:
        category = None
    
    return render(request, 'authentication/blog_list.html', {
        'categories': categories,
        'blog_posts': blog_posts,
        'selected_category': category
    })

@login_required
def blog_post_detail(request, slug):
    blog_post = get_object_or_404(BlogPost, slug=slug)
    
    # Only allow access if published or if user is the author
    if blog_post.status != 'published' and request.user != blog_post.author:
        return redirect('blog_list')
    
    return render(request, 'authentication/blog_detail.html', {'blog_post': blog_post})