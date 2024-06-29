import datetime

from django.http import HttpResponseForbidden
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
                                  DeleteView, TemplateView)
from .models import Post, Category, Author
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.models import Group
from .tasks import send_mess_new_post


class PostsList(ListView):
    model = Post
    ordering = '-post_time_in'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['time_now'] = datetime.utcnow()
        news_list = Post.objects.all()
        context['news'] = news_list
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class SearchList(ListView):
    model = Post
    ordering = '-post_time_in'
    template_name = 'news_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        today = datetime.date.today()
        post_limit = Post.objects.filter(author_id=post.author_id, post_time_in__date=today).count()
        if post_limit >= 3:
            return render(self.request, 'news/post_limit.html', {'author': post.author_id})

        if self.request.path == '/news/news/create/':
            post.post_type = 'NE'
            post.save()

        elif self.request.path == '/news/articles/create/':
            post.post_type = 'AR'
            post.save()

        send_mess_new_post.delay(post.pk)
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('News.change_Post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        if (self.request.path == f'/news/{post.id}/edit/' and post.post_type != 'NE') or \
           (self.request.path == f'/articles/{post.id}/edit/' and post.post_type != 'AR'):
            return HttpResponseForbidden("Вы не можете вносить изменения в данный тип записи")
        return super().form_valid(form)


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')


class PersonalPage(LoginRequiredMixin, TemplateView):
    template_name = 'auth/personal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        if not Author.objects.filter(user=user).exists():
            Author.objects.create(user=user)
    return redirect('/')


class CategoryList(PostsList):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.category).order_by('-post_time_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_subscriber'] = self.request.user in self.category.subscribers.all()
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required()
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на категорию'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})


@login_required()
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)

    message = 'Вы успешно отписались от  категории'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})





