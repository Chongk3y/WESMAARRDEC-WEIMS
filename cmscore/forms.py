from django.forms import ModelForm
from django import forms
from .models import *
from cmsblg.models import *
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory
from django.shortcuts import render
from django.utils.html import format_html
# from django.forms import widgets

# class ImageSelect(widgets.Select):
#     def render_option(self, selected_choices, option_value, option_label):
#         option_data = self.choices.queryset.get(pk=option_value)
#         return '<option value="%s">%s<img src="%s" alt="%s"></option>' % (
#             option_value, option_label, option_data.images.url, option_label)

def generate_unique_slug(model, title):
    slug = slugify(title)
    unique_slug = slug
    num = 1
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{num}"
        num += 1
    return unique_slug


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            selected_images = self.instance.image.all()
            self.fields['image'].queryset = PostImages.objects.all()
            self.fields['image'].widget.attrs['selected_images'] = [str(image.pk) for image in selected_images]

    class Meta:
        model = Post
        fields = ['category', 'title', 'intro', 'body', 'image']
        labels = {
            'title': 'Title',
            'category': 'Category',
            'intro': 'Introduction',
            'body': 'Content',
            'image': 'Image',
        }

    def form_valid(self, form):
        form.instance.author = self.request.user
        slug = slugify(form.cleaned_data['title'])
        count = 1
        while Post.objects.filter(slug=slug).exists():
            slug = f"{slug}-{count}"
            count += 1
        form.instance.slug = slug
        return super().form_valid(form)


class SearchForm(forms.Form):
     query = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Search...'}))

class SlideForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    detail = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    image = forms.FileField(
        widget=forms.FileInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )

    class Meta:
        model = Slide
        fields = ['name', 'detail', 'image']