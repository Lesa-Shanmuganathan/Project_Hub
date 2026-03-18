from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('projects/<slug:slug>/edit/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('projects/<slug:slug>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
    
    path('my-projects/', views.my_projects, name='my_projects'),
    path('bookmarks/', views.bookmarked_projects, name='bookmarked_projects'),
    
    path('api/projects/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('api/projects/<int:pk>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('projects/<int:pk>/comment/', views.add_comment, name='add_comment'),
    
    # Admin/Faculty
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pending/', views.pending_projects, name='pending_projects'),
    path('projects/<int:pk>/approve/', views.approve_project, name='approve_project'),
    path('projects/<int:pk>/reject/', views.reject_project, name='reject_project'),
    path('projects/<int:pk>/feature/', views.feature_project, name='feature_project'),
]
