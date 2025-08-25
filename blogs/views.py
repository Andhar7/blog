# # from django.http import HttpResponse
# from django.shortcuts import redirect, render
# from blogs.models import Blog, Category

# def posts_by_category(request, category_id):
#     posts = Blog.objects.filter(status='Published', category=category_id)
#     # category = Category.objects.get(pk=category_id)
#     # Use try/except to handle the case where the category does not exist
#     try:
#         category = Category.objects.get(pk=category_id)
#     except:
#         # redirect the user to home page if category does not exist
#         return redirect('home')
#         # return render(request, '404.html')
#     # Use get_object_or_404 to fetch the category or return a 404 error if not found
#     context = {
#         'posts': posts,
#         'category': category     
#     }
    
#     return render(request, 'posts_by_category.html', context)
 
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from blogs.models import Blog, Category
from django.db.models import Q

def posts_by_category(request, category_id):
    """
    Display published blog posts filtered by category with pagination.
    
    Args:
        request: HTTP request object
        category_id: Primary key of the category
        
    Returns:
        Rendered template with posts and category context
        
    Raises:
        Http404: If category does not exist
    """
    # Get category or return 404 if not found
    category = get_object_or_404(Category, pk=category_id)
    
    # Filter posts by category and status, order by newest first
    posts = Blog.objects.filter(
        status='Published', 
        category=category
    ).select_related('category', 'author').order_by('-created_at')
    
    # Add pagination (12 posts per page)
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts': page_obj,
        'category': category,
        'page_obj': page_obj,
    }
    
    return render(request, 'posts_by_category.html', context)

def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status='Published')
    context = {
        'single_blog': single_blog, 
    }
    return render(request, 'blogs.html', context)

def search(request):
    keyword = request.GET.get('keyword')
    # print('keyword:', keyword)
    blogs = Blog.objects.filter(Q(title__icontains=keyword) | 
                                Q(short_description__icontains=keyword) | 
                                Q(blog_body__icontains=keyword), 
                                status='Published')
    context = {
        'blogs': blogs, 
        'keyword': keyword,
    }
    return render(request, 'search.html', context)