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
from collections import defaultdict, Counter

from .models import Post, Author, PostView, Like
from .forms import CommentForm, PostForm
from marketing.forms import EmailSignupForm
from marketing.models import Signup
from taggit.models import Tag
from django.template.defaultfilters import slugify
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import (SearchQuery, SearchRank, SearchVector,TrigramSimilarity,)
from django.db.models import Value
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
        #search_result = Post.objects.all()
        txt = request.GET.get('q')
        page_request_var = 'page'

        search_query = SearchQuery(txt, config='english')
        search_vectors = (SearchVector('title', weight='A', config='english') \
                              + SearchVector('overview', weight='B', config='english') \
                              + SearchVector('post_content', weight='D', config='english'))
        search_rank = SearchRank(search_vectors, search_query)
        trigram_similarity = TrigramSimilarity("title", txt)
        search_result = Post.objects.annotate(
                search=search_vectors).filter(featured=True,
                                              search=search_query).annotate(
                rank=search_rank + trigram_similarity).order_by("-rank")
        #search_count = search_result.count()
        # paginator = Paginator(search_result, 4)
        # page = self.request.GET.get(page_request_var)
        # try:
        #    search_result = paginator.page(page)
        # except PageNotAnInteger:
        #    search_result = paginator.page(1)
        # except EmptyPage:
        #    search_result = paginator.page(paginator.num_pages)

        context = {
            'queryset': search_result,
            'page_request_var': page_request_var,

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
        tag_frequency = defaultdict(int)

        for item in featured:
            for tag in item.tags.all():
                tag_frequency[tag.name] += 1

        tag_freq = Counter(tag_frequency).most_common()
        print(tag_freq)
        context = {
            'object_list': featured,
            'latest': latest,
            'tag_frequency': tag_freq,
            'form': self.form,

        }
        messages.info(request, "")
        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        featured = Post.objects.filter(featured=True)
        latest = Post.objects.order_by('-timestamp')[0:3]
        tag_frequency = defaultdict(int)

        for item in featured:
            for tag in item.tags.all():
                tag_frequency[tag.name] += 1

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
                        'tag_frequency': Counter(tag_frequency).most_common(),
                        'sub_message': sub_message,
                        'form': form,
                    }
                    return render(request, 'index.html', context)
                else:
                    sub_message = "You are already subscribed"
                    context = {
                        'object_list': featured,
                        'latest': latest,
                        'tag_frequency': Counter(tag_frequency).most_common(),
                        'sub_message': sub_message,
                        'form': form,
                    }
                    return render(request, 'index.html', context)
            else:
                sub_message = "Enter a valid email id"
                context = {
                    'object_list': featured,
                    'latest': latest,
                    'tag_frequency': Counter(tag_frequency).most_common(),
                    'sub_message': sub_message,
                    'form': form,
                }
                return render(request, 'index.html', context)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    tag_frequency = defaultdict(int)

    for item in featured:
        for tag in item.tags.all():
            tag_frequency[tag.name] += 1

    if request.method == "POST":
        email = request.POST['email']
        print(email)
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
    context = {
        'object_list': featured,
        'latest': latest,
        'tag_frequency': Counter(tag_frequency).most_common(),
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
    ordering = ['-timestamp']
    paginate_by = 4

    def get_queryset(self):
        new_context = Post.objects.filter(
            featured=True
        ).order_by('-timestamp')
        return new_context

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        latest = Post.objects.filter(
            featured=True
        ).order_by('-timestamp')[:3]
        tag_frequency = defaultdict(int)
        featured = Post.objects.filter(
            featured=True
        )
        for item in featured:
            for tag in item.tags.all():
                tag_frequency[tag.name, tag.slug] += 1

        context = super().get_context_data(**kwargs)
        context['latest'] = latest
        context['page_request_var'] = "page"
        context['tag_frequency'] = list(Counter(tag_frequency).most_common())
        context['category_count'] = category_count
        context['form'] = self.form
        return context



def post_list(request):

    category_count = get_category_count()
    #post_list = Post.objects.all()
    post_list = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)


    context ={
        'queryset': paginated_queryset,
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
        #tag_slug = slugify(tag_name)
        print(tag_slug)
        tags = Tag.objects.filter(slug=tag_slug).values_list('name', flat=True)
        print(tags)
        field_name = 'tags'
        tagged_post_list = Post.objects.filter(tags__name__in=tags)


        #common_tags = tags.most_common()[:5]
        category_count = get_category_count()

        # queryset = Post.objects.all().order_by('id')
        latest = Post.objects.filter(featured=True).order_by('-timestamp')[0:3]
        paginator = Paginator(tagged_post_list, 4)
        page_request_var = 'page'
        page = request.GET.get(page_request_var)

        tag_frequency = defaultdict(int)
        featured = Post.objects.filter(
            featured=True
        )
        for item in featured:
            for tag in item.tags.all():
                tag_frequency[tag.name, tag.slug] += 1

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
            'tag_frequency' : Counter(tag_frequency).most_common(),
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
        most_recent = Post.objects.filter(featured=True).order_by('-timestamp')[:3]
        tag_frequency = defaultdict(int)
        featured = Post.objects.filter(
            featured=True
        )
        for item in featured:
            for tag in item.tags.all():
                tag_frequency[tag.name, tag.slug] += 1

        print("Inside Detailview" + tag_frequency)
        context = super().get_context_data(**kwargs)
        context['latest'] = most_recent
        context['page_request_var'] = "page"
        context['tag_frequency'] = Counter(tag_frequency).most_common()
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
    most_recent = Post.objects.filter(featured=True).order_by('-timestamp')[:3]
    post = get_object_or_404(Post, id=pk)

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)

    tag_frequency = defaultdict(int)
    featured = Post.objects.filter(
        featured=True
    )
    for item in featured:
        for tag in item.tags.all():
            tag_frequency[tag.name, tag.slug] += 1
    tag_list = Counter(tag_frequency).most_common()
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
        'tag_frequency': tag_list,
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

        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        form.save_m2m()
        return redirect(reverse("post-detail", kwargs={
            'pk': form.instance.pk
        }))

def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    user = request.user
    #author = get_user(request.user)

    print(user)
    print(request.method)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = user
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
    template_name = 'post_update.html'
    form_class = PostForm

    print("Inside update post before")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user

        obj.save()
        form.save_m2m()

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
    user = request.user
    if request.method == "POST":
        if form.is_valid():
            obj = form.save(commit=False)
            data = form['tags'].value()
            print("Inside update post post_update " + data)
            data = obj.cleaned_data
            print(data['id_tags'])
            obj.user = self.request.user
            # form.instance.author = get_user(self.request.user)
            obj.save()
            form.save_m2m()
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

