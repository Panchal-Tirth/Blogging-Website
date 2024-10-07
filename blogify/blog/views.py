from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
# Create your views here.

# posts=Post.objects.all()

def home(request):
    context={
        "posts":Post.objects.all()
    }
    return render(request,"blog/home.html",context)

class PostListView(ListView):
    model = Post
    template_name='blog/home.html'
    context_object_name="posts"
    ordering=['-date_posted']
    paginate_by=5
    # <app>/<model>_<viewtype>.html
    
class UserPostListView(ListView):
    model = Post
    template_name='blog/user_posts.html'
    context_object_name="posts"
    paginate_by=5
    
    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    # <app>/<model>_<viewtype>.html
    
class PostDetailView(DetailView):
    model = Post
    
    # <app>/<model>_<viewtype>.html

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields=['title','content']
    
    def form_valid(self,form):
         form.instance.author=self.request.user
         return super().form_valid(form)     
    # <app>/<model>_<viewtype>.html

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView ):
    model = Post
    fields=['title','content']

    def form_valid(self,form):
         form.instance.author=self.request.user
         return super().form_valid(form)     
    # <app>/<model>_<viewtype>.html
    
    def test_func(self):
        post = self.get_object()
        
        if self.request.user==post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url='/'
    def test_func(self):
        post = self.get_object()
        
        if self.request.user==post.author:
            return True
        return False
    # <app>/<model>_<viewtype>.html


def about(request):
    return render(request,"blog/about.html",{'title':'About'})