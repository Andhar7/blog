from django.shortcuts import render
from blogs.models import Blog, Category


def home(request):
    # categories = Category.objects.all() # Moved to context processor
    featured_posts = Blog.objects.filter(is_featured=True, status='Published').order_by('updated_at')
    # featured_posts = Blog.objects.filter(is_featured=True)
    posts = Blog.objects.filter(is_featured=False, status='Published') 
    context = {
        # 'categories': categories, # Moved to context processor
        'featured_posts': featured_posts,
        'posts': posts
    }
    # print(featured_posts)
    # print(categories)
    return render(request, 'home.html', context) 