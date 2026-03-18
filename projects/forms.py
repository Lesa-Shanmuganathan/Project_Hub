from django import forms
from .models import Project, ProjectImage, Comment

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'detailed_description', 'category', 
                  'technologies', 'github_link', 'live_demo_link', 'video_link',
                  'dataset_link', 'documentation_link', 'thumbnail']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'detailed_description': forms.Textarea(attrs={'rows': 6}),
            'technologies': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'technologies':
                field.widget.attrs['class'] = 'form-control'

class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image', 'caption']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Write your comment...',
                'class': 'form-control'
            })
        }
