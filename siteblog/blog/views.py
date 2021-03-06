from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag
from django.db.models import F
import paho.mqtt.client as mqtt
import json

# Create your views here.


class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'classic blog'
        return context


class PostsByCategory(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class GetPost(DetailView):
    model = Post
    template_name = 'blog/single.html'
    context_object_name = 'post'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # прибавляем +1 в поле views(кол-во просмотров)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


class PostsByTag(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 1
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'записи по тегу' + \
            str(Tag.objects.get(slug=self.kwargs['slug']))
        return context


class Search(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context


def some_json(request):
    jsonDict = {"status": "success", "message": "everything's fine"}

    return HttpResponse(json.dumps(jsonDict))
