from django import forms
from .models import Post, Category, PostImages, Comment, Fact

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your comment here...'}),
        }
        labels = {
            'body': '',
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title', 'caption', )

class FactForm(forms.ModelForm):
    class Meta:
        model = Fact
        fields = ['question', 'answer', 'img', 'category']
        labels = '__all__'

class PostForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    slug = forms.SlugField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    intro = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    featured = forms.BooleanField(
    widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    required=False
    )
    image = forms.ImageField(
        widget=forms.FileInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    status = forms.ChoiceField(
        choices=Post.CHOICES_STATUS,
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=True
    )

    class Meta:
        model = Post
        fields = [
            'title',
            'slug', 
            'intro', 
            'body', 
            'featured', 
            'image', 
            'status', 
            'category'
        ]

class FactForm(forms.ModelForm):
    question = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    answer = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    img = forms.ImageField(
        widget=forms.FileInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=False
    )

    class Meta:
        model = Fact
        fields = [
            'question', 
            'answer', 
            'img', 
            'category'
        ]

class CategoryForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    caption = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    slug = forms.SlugField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )

    class Meta:
        model = Category
        fields = [
            'title', 
            'caption', 
            'slug'
        ]

