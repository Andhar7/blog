from django.contrib import admin
from blogs.models import Category, Blog

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title','category', 'status', 'author', 'is_featured')
    list_filter = ('status', 'category', 'is_featured')
    search_fields = ('title', 'slug', 'short_description', 'blog_body', 'author__username', 'author__first_name', 'author__last_name', 'category__category_name', 'status')
    list_editable = ('is_featured', 'status', 'category', 'author')

admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)
