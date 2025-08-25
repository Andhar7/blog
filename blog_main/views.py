from django.shortcuts import render
from assignments.models import About
from blogs.models import Blog 


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