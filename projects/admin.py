from django.contrib import admin
from .models import Category, Technology, Project, ProjectImage, Comment, Like, Bookmark

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']
    prepopulated_fields = {'slug': ('name',)}

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'views_count', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'description', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
    actions = ['approve_projects', 'reject_projects', 'feature_projects']
    
    def approve_projects(self, request, queryset):
        queryset.update(status='approved')
    approve_projects.short_description = "Approve selected projects"
    
    def reject_projects(self, request, queryset):
        queryset.update(status='rejected')
    reject_projects.short_description = "Reject selected projects"
    
    def feature_projects(self, request, queryset):
        queryset.update(status='featured')
    feature_projects.short_description = "Feature selected projects"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['project', 'author', 'created_at']
    list_filter = ['created_at']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['project', 'user', 'created_at']

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['project', 'user', 'created_at']
