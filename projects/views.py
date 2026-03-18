from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Project, Category, Technology, Comment, Like, Bookmark
from .forms import ProjectForm, CommentForm

class HomeView(ListView):
    model = Project
    template_name = 'home.html'
    context_object_name = 'projects'
    
    def get_queryset(self):
        return Project.objects.filter(status__in=['approved', 'featured']).order_by('-created_at')[:6]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_projects'] = Project.objects.filter(status='featured')[:3]
        context['categories'] = Category.objects.annotate(
            project_count=Count('projects', filter=Q(projects__status__in=['approved', 'featured']))
        )
        context['total_projects'] = Project.objects.filter(status__in=['approved', 'featured']).count()
        context['total_students'] = Project.objects.filter(
            status__in=['approved', 'featured']
        ).values('author').distinct().count()
        return context

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Project.objects.filter(status__in=['approved', 'featured'])
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(author__username__icontains=search)
            )
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by technology
        tech = self.request.GET.get('tech')
        if tech:
            queryset = queryset.filter(technologies__slug=tech)
        
        # Filter by year
        year = self.request.GET.get('year')
        if year:
            queryset = queryset.filter(author__year=year)
        
        # Sorting
        sort = self.request.GET.get('sort', '-created_at')
        if sort == 'popular':
            queryset = queryset.annotate(like_count=Count('likes')).order_by('-like_count')
        elif sort == 'views':
            queryset = queryset.order_by('-views_count')
        elif sort == 'oldest':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['technologies'] = Technology.objects.all()
        context['current_category'] = self.request.GET.get('category', '')
        context['current_tech'] = self.request.GET.get('tech', '')
        context['current_sort'] = self.request.GET.get('sort', '-created_at')
        context['search_query'] = self.request.GET.get('search', '')
        return context

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_admin_user or self.request.user.is_faculty:
                return Project.objects.all()
            return Project.objects.filter(
                Q(status__in=['approved', 'featured']) | Q(author=self.request.user)
            )
        return Project.objects.filter(status__in=['approved', 'featured'])
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Increment view count
        self.object.views_count += 1
        self.object.save(update_fields=['views_count'])
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()[:20]
        context['related_projects'] = Project.objects.filter(
            category=self.object.category,
            status__in=['approved', 'featured']
        ).exclude(pk=self.object.pk)[:4]
        
        if self.request.user.is_authenticated:
            context['is_liked'] = Like.objects.filter(
                project=self.object, user=self.request.user
            ).exists()
            context['is_bookmarked'] = Bookmark.objects.filter(
                project=self.object, user=self.request.user
            ).exists()
        
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Project submitted successfully! It will be reviewed by admin.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('my_projects')

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    
    def test_func(self):
        project = self.get_object()
        return self.request.user == project.author or self.request.user.is_admin_user
    
    def form_valid(self, form):
        # Reset to pending if student edits
        if not self.request.user.is_admin_user:
            form.instance.status = 'pending'
        messages.success(self.request, 'Project updated successfully!')
        return super().form_valid(form)

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('my_projects')
    
    def test_func(self):
        project = self.get_object()
        return self.request.user == project.author or self.request.user.is_admin_user
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Project deleted successfully!')
        return super().delete(request, *args, **kwargs)

@login_required
def my_projects(request):
    projects = Project.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'projects/my_projects.html', {'projects': projects})

@login_required
def bookmarked_projects(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('project')
    projects = [b.project for b in bookmarks]
    return render(request, 'projects/bookmarked_projects.html', {'projects': projects})

@login_required
def toggle_like(request, pk):
    project = get_object_or_404(Project, pk=pk)
    like, created = Like.objects.get_or_create(project=project, user=request.user)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'count': project.likes.count()
    })

@login_required
def toggle_bookmark(request, pk):
    project = get_object_or_404(Project, pk=pk)
    bookmark, created = Bookmark.objects.get_or_create(project=project, user=request.user)
    
    if not created:
        bookmark.delete()
        bookmarked = False
    else:
        bookmarked = True
    
    return JsonResponse({'bookmarked': bookmarked})

@login_required
def add_comment(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added!')
    
    return redirect('project_detail', slug=project.slug)

# Admin/Faculty Views
@login_required
def pending_projects(request):
    if not (request.user.is_admin_user or request.user.is_faculty):
        messages.error(request, 'Access denied!')
        return redirect('home')
    
    projects = Project.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'projects/pending_projects.html', {'projects': projects})

@login_required
def approve_project(request, pk):
    if not (request.user.is_admin_user or request.user.is_faculty):
        messages.error(request, 'Access denied!')
        return redirect('home')
    
    project = get_object_or_404(Project, pk=pk)
    project.status = 'approved'
    project.save()
    messages.success(request, f'Project "{project.title}" approved!')
    return redirect('pending_projects')

@login_required
def reject_project(request, pk):
    if not (request.user.is_admin_user or request.user.is_faculty):
        messages.error(request, 'Access denied!')
        return redirect('home')
    
    project = get_object_or_404(Project, pk=pk)
    project.status = 'rejected'
    project.save()
    messages.warning(request, f'Project "{project.title}" rejected!')
    return redirect('pending_projects')

@login_required
def feature_project(request, pk):
    if not request.user.is_admin_user:
        messages.error(request, 'Access denied!')
        return redirect('home')
    
    project = get_object_or_404(Project, pk=pk)
    project.status = 'featured'
    project.save()
    messages.success(request, f'Project "{project.title}" is now featured!')
    return redirect('project_detail', slug=project.slug)

@login_required
def dashboard(request):
    if not (request.user.is_admin_user or request.user.is_faculty):
        messages.error(request, 'Access denied!')
        return redirect('home')
    
    context = {
        'total_projects': Project.objects.count(),
        'pending_count': Project.objects.filter(status='pending').count(),
        'approved_count': Project.objects.filter(status='approved').count(),
        'featured_count': Project.objects.filter(status='featured').count(),
        'recent_projects': Project.objects.order_by('-created_at')[:10],
        'top_categories': Category.objects.annotate(
            project_count=Count('projects')
        ).order_by('-project_count')[:5],
    }
    return render(request, 'projects/dashboard.html', context)
