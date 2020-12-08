from django.db.models import Count, Q
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
#from allauth.account.views import LoginView, LogoutView, SignupForm, email
from django.http import JsonResponse

from .models import Post, Author, PostView, Like
from .forms import CommentForm, PostForm
from marketing.forms import EmailSignupForm
from marketing.models import Signup
from taggit.models import Tag
from django.template.defaultfilters import slugify

import re


form = EmailSignupForm()

def get_author(user):

    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def get_user(user):

    qs = User.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

class SearchView(View):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(overview__icontains=query)
            ).distinct()
        context = {
            'queryset': queryset
        }
        return render(request, 'search_results.html', context)

def search(request):
    queryset = Post.objects.all().order_by('id')
    latest = Post.objects.order_by('-timestamp')[0:3]
    category_count = queryset \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    post_count = queryset.count()
    #This need be fixed for the number of records per page
    paginator = Paginator(queryset, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'paginated_queryset': paginated_queryset,
        'category_count' : category_count,
        'latest': latest,
        'post_count': post_count,
        'page_request_var': page_request_var,
    }
    return render(request, 'search_results.html', context)

def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    return queryset

class IndexView(View):
    form = EmailSignupForm()

    def get(self, request, *args, **kwargs):
        featured = Post.objects.filter(featured=True)
        latest = Post.objects.order_by('-timestamp')[0:3]

        context = {
            'object_list': featured,
            'latest': latest,
            'form': self.form,

        }
        messages.info(request, "")
        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        featured = Post.objects.filter(featured=True)
        latest = Post.objects.order_by('-timestamp')[0:3]
        #print(email)
        #STATUS = 50
        # Later check for messages info in Index.html
        if request.method == "POST":
            if checkemail(email) == 'valid':
                if ifEmailExist(email) == 'doesnotexist':
                    new_signup = Signup()
                    new_signup.email = email
                    new_signup.save()
                    sub_message = "Thanks for subscribing"
                    context = {
                        'object_list': featured,
                        'latest': latest,
                        'sub_message': sub_message,
                        'form': form,
                    }
                    return render(request, 'index.html', context)
                else:
                    sub_message = "You are already subscribed"
                    context = {
                        'object_list': featured,
                        'latest': latest,
                        'sub_message': sub_message,
                        'form': form,
                    }
                    return render(request, 'index.html', context)
            else:
                sub_message = "Enter a valid email id"
                context = {
                    'object_list': featured,
                    'latest': latest,
                    'sub_message': sub_message,
                    'form': form,
                }
                return render(request, 'index.html', context)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == "POST":
        email = request.POST['email']
        print(email)
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
    context = {
        'object_list': featured,
        'latest': latest,
        'form': form
    }
    return render(request,'index.html',context)

def checkemail(email):
    #pattern = r"\"?([-a-zA-Z0-9.`?{2-3}]+@\w+\.\w+)\"?"
    pattern = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,3}\.?$', re.IGNORECASE)  # domain

    if(re.search(pattern,email)):
        return 'valid'
    else:
        return 'notvalid'

def ifEmailExist(email):
    email_lst = Signup.objects.values_list('email')
    email_list = []
    for i in list(email_lst):
        email_list.append(i[0])
    if email in email_list:
        status = "exist"
    else:
        status = "doesnotexist"

    return status

class PostListView(ListView):
    form = EmailSignupForm()
    model = Post
    template_name = 'blog.html'
    context_object_name = 'queryset'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        latest = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['latest'] = latest
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['form'] = self.form
        return context



def post_list(request):

    category_count = get_category_count()

    queryset = Post.objects.all().order_by('id')
    latest = Post.objects.order_by('-timestamp')[0:3]
    paginator = Paginator(queryset, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)


    context ={
        'paginated_queryset': paginated_queryset,
        'latest':latest,
        'page_request_var':page_request_var,
        'category_count': category_count,
        'form': form
        }
    return render(request,'blog.html',context)


def tagged_post_list(request, tag_slug=None):
    if tag_slug:
        #print('inside slug tag')
        #try:
        #tag_slug = slugify(tag_slug)
        print(tag_slug)
        tags = Tag.objects.filter(slug=tag_slug).values_list('name', flat=True)
        print(tags)
        field_name = 'tags'
        tagged_post_list = Post.objects.filter(tags__name__in=tags)


        #common_tags = tags.most_common()[:5]
        category_count = get_category_count()

        # queryset = Post.objects.all().order_by('id')
        latest = Post.objects.order_by('-timestamp')[0:3]
        paginator = Paginator(tagged_post_list, 4)
        page_request_var = 'page'
        page = request.GET.get(page_request_var)

        try:
            tagged_post_list = paginator.page(page)
        except PageNotAnInteger:
            tagged_post_list = paginator.page(1)
        except EmptyPage:
            tagged_post_list = paginator.page(paginator.num_pages)

        context = {

            'latest': latest,
            'page_request_var': page_request_var,
            'category_count': category_count,
            'form': form,
            'tags': tags,
            'post_list': tagged_post_list,


        }

        return render(request, 'tagged_list.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    form = CommentForm()

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(
                user=self.request.user,
                post=obj
            )
        return obj

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'pk': post.pk
            }))

def post_detail(request, pk):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post = get_object_or_404(Post, id=pk)

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'pk': post.pk
            }))
    context = {
        'post': post,
        'latest': most_recent,
        'category_count': category_count,
        'form': form,

    }
    return render(request, 'post.html', context)


def likePost(request, pk):

    if request.method == 'POST':
        try:
            pk = pk
            likedpost = get_object_or_404(Post, id=pk) #getting the liked posts
            m = Like(user=request.user, post=likedpost) # Creating Like Object
            m.save()  # saving it to store in database

            return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))
        except:
            return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

    else:
        return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        #form.instance.author = get_user(self.request.user)
        form.save()
        return redirect(reverse("post-detail", kwargs={
            'pk': form.instance.pk
        }))

def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    #author = get_user(request.user)

    print(author)
    print(request.method)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            print(request.method)
            form.save()
            form.save_m2m()
            return redirect(reverse("post-detail", kwargs={
                'pk': form.instance.id
            }))

    context = {
        'title': title,
        'form': form,

    }
    return render(request, "post_create.html", context)

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse("post-detail", kwargs={
            'pk': form.instance.pk
        }))

def post_update(request, pk):
    title = 'Update'
    post = get_object_or_404(Post, id=pk)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'pk': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)

class PostDeleteView(DeleteView):
    model = Post
    success_url = '/post_list'
    template_name = 'post_confirm_delete.html'

def post_delete(request, pk):

    post = get_object_or_404(Post, id=pk)
    post.delete()
    return redirect(reverse("post-list"))

