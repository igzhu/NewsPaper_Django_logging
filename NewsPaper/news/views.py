from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.urls import resolve
from django.shortcuts import redirect

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime

from .models import Post, Category, User
from .filters import PostFilter
from .forms import PostForm

DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL


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

    '''def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            header = form.cleaned_data.get("head")
            txt = form.cleaned_data.get('postText')  # .[:51]
            ctgries = form.cleaned_data.get("category")
            for ctgr in ctgries:
                categ = Category.objects.get(name=ctgr.name)
                cat_users = categ.subscribers.all()
                for usr in cat_users:
                    html_content = render_to_string('news/mail_in_category.html',
                       {'headr': header,
                        'catgor': categ.name,
                        'text': txt,
                        'nam': usr.username,
                        'e_mail': usr.email, }
                    )
                    msg = EmailMultiAlternatives(
                        subject=header,
                        body=txt[:51],
                        from_email=DEFAULT_FROM_EMAIL,
                        to=[usr.email, ]
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
        # form.save()
        return super().get(request, *args, **kwargs)'''


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
    # form_class = PostForm
    # form_class = PostFilter
    queryset = Post.objects.order_by('-postDatetime')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = User.objects.all()
        # context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostAdd(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'news/post_add.html'
    # context_object_name = 'posts'
    # context_object_name = 'posted_item'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        return context

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['categories'] = Category.objects.all()
    #    context['form'] = PostForm()
    #    context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
    #    return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            header = form.cleaned_data.get("head")
            txt = form.cleaned_data.get('postText')  # .[:51]
            ctgries = form.cleaned_data.get("category")
            for ctgr in ctgries:
                categ = Category.objects.get(name=ctgr.name)
                cat_users = categ.subscribers.all()
                for usr in cat_users:
                    html_content = render_to_string('news/mail_in_category.html',
                       {'headr': header,
                        'catgor': categ.name,
                        'text': txt,
                        'nam': usr.username,
                        'e_mail': usr.email, }
                    )
                    msg = EmailMultiAlternatives(
                        subject=header,
                        body=txt[:51],
                        from_email=DEFAULT_FROM_EMAIL,
                        to=[usr.email, ]
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
        # form.save()
        #return redirect(request.META.get('HTTP_REFERER'))
        #return super().get(request, *args, **kwargs)
        return redirect('/posts/')

    # def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
    #    return context


class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'news/post_add.html'
    form_class = PostForm

    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    # def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
    #    return context


class PostDelete(LoginRequiredMixin, DeleteView):
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'

    # def get_context_data(self, **kwargs):
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


@login_required
def subscribe_to_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        email = user.email
        html = render_to_string(
            'news/mail_subscribe.html',
            {'categry': category,
             "user": user}
        )
        msg = EmailMultiAlternatives(
            subject=f'{category} subscription',
            body='You are subscribed.',
            from_email=DEFAULT_FROM_EMAIL,
            to=[email, ]
        )

        msg.attach_alternative(html, 'text/html')
        try:
            msg.send()
        except Exception as e:
            print(e)
            return redirect('/posts/')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_from_category(request, pk):
    user = request.user
    c = Category.objects.get(id=pk)
    if c.subscribers.filtet(id=user.id).exists():
        c.subscribers.remove(user)
    return redirect('/posts/'
                    )


class PostCategoryView(ListView):
    model = Post
    template_name = 'news/category.html'
    context_object_name = 'posts'
    # ordering = ['-postDatetime']
    queryset = Post.objects.order_by('-postDatetime')
    paginate_by = 10

    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        ctgr = Category.objects.get(id=self.id)
        queryset = Post.objects.filter(category=ctgr).order_by('-postDatetime')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        categry = Category.objects.get(id=self.id)
        subscribed = categry.subscribers.filter(email=user.email)
        if not subscribed:
            context['ctgry'] = categry
        return context
