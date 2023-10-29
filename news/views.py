from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author, Category
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives 
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.core.cache import cache
#from datetime import datetime,timedelta
#from django.utils import timezone


class NewsList (ListView): #выводит страницу со списком новостей
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context
     
class NewDetail (DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
    queryset = Post.objects.all()
    
    def get_object(self,*args,**kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


 
class Search (ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    queryset = Post.objects.order_by('-id')
    #ordering = ['-price']
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) 
        return context 
    
class PostAdd (LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'new_add.html'
    form_class = PostForm
    permission_required = ('news.add_post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm()
        return context

    # def post(self, request, *args, **kwargs):
    #     if Post.objects.filter(
    #             author=Author.objects.get(userAuthor=request.user),
    #             datatime__gte=timezone.now() - timedelta(days=1),
    #     ).count() < 3:
    #         form = self.form_class(request.POST) 
    #         if form.is_valid():
    #             obj = form.save(commit=False)
    #             obj.post_author = Author.objects.get(userAuthor = request.user.id)
    #             form.save()
    #             url = Post.objects.filter().last().get_absolute_url()
    #             category_name = form.cleaned_data.get("category")[0]
    #             category = Category.objects.get(NameCategory=category_name)
    #             title = form.cleaned_data.get('title')
    #             text_new = (form.cleaned_data.get('text'))[0:49] 
    #             subject = title + ' ' + text_new +'...'
    #             urls_posta = 'http://127.0.0.1:8000' + url
    #             for sub in category.subscribers.filter().exclude(email=''):
    #                 html_content = render_to_string( 
    #                     'mail/email_sub.html',
    #                     {
    #                         'category': category,
    #                         'title': title,
    #                         'subject': subject,
    #                         'urls_posta': urls_posta,
    #                     }
    #                 )
    #                 msg = EmailMultiAlternatives(
    #                     subject=f'Здравствуй {sub.username}. Новая статья в твоём любимом разделе!',
    #                     body = subject,
    #                     from_email='p.o.c.h.t.a.newspaper@yandex.ru',
    #                     to=[sub.email]
    #                     )
    #                 msg.attach_alternative(html_content, "text/html")
    #                 msg.send()
    #         return redirect('/news/')
    #     else:
    #         send_mail(
    #             subject=f'{request.user.username},вы пытаетесь сделать более 3 постов в день!',
    #             message='Попробуйте через сутки!',
    #             from_email= 'p.o.c.h.t.a.newspaper@yandex.ru', #settings.DEFAULT_FROM_EMAIL,
    #             recipient_list=[request.user.email]
    #         )
    #         return redirect('/news/')
            



class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'new_add.html'
    form_class = PostForm
    permission_required = ('news.change_post')
 
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
 
 
class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'new_delete.html'
    queryset = Post.objects.all()
    context_object_name = 'new'
    success_url = '/news/'
    permission_required = ('news.delete_post')


@login_required
def become_author(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
        Author.objects.create(userAuthor=request.user, ratingAuthor=0)
    return redirect("/news/")

class CategoryList (ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = "categories"
    queryset = Category.objects.all()
    
    
class CategoryDetali (DeleteView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['subscribers'] = category.subscribers.all()
        return context


@login_required
def subscribe(request, pk): 
    user = request.user
    category = Category.objects.get(id=pk)
    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
    return redirect(request.META.get('HTTP_REFERER'))

    

@login_required
def unsubscribe(request, pk): 
    user = request.user
    category = Category.objects.get(id=pk)
    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(user)
    return redirect(request.META.get('HTTP_REFERER'))
    
    


