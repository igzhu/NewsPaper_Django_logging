from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.shortcuts import redirect

from .models import Post, Category, User
from .filters import PostFilter
from .forms import PostForm
# Create your views here.


class PostsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    form_class = PostForm
    queryset = Post.objects.order_by('-postDatetime')
    paginate_by = 10


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        return context


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save
        return super().get(request, *args, **kwargs)


class PostDetails(DetailView):
    template_name = 'news/post_detail.html'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostSearch(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'posts'
    #form_class = PostForm
    #form_class = PostFilter
    queryset = Post.objects.order_by('-postDatetime')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = User.objects.all()
        #context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostAdd(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'news/post_add.html'
    #context_object_name = 'posts'
    form_class = PostForm

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
    #    return context

class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'news/post_add.html'
    form_class = PostForm
    #login_url = '/login/'
    #redirect_field_name = 'redirect_to'
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
    #    return context

class PostDelete(LoginRequiredMixin, DeleteView):
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
    #    return context



@login_required
def upgrade_me_to_author(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/posts/')
