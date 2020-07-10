  
from django.shortcuts import render ,get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    #DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post,Comment
from .form import EmailPostForm , CommentForm


def home(request):
    context = {
        'posts': Post.published.all()
    }
   
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-publish']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_query_set(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-publish')
  

"""class PostDetailView(DetailView,CommentForm):
    model = Post
    model= Comment
    success_url = 'post-detail'"""


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'body','status']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'body','status']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

"""def PostLatest(request):
    post = Post.objects.get(id=1)
    post.is_favorite = True
    return render(request, "latest.html", {'post':post })"""

def about(request):
    return render (request,'blog/about.html')

def post_share(request , post_id): # send mail
     post = get_object_or_404(Post, id=post_id , status='published')
     if request.method == 'POST':
        form = EmailPostForm(request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read"\
                f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
            f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
        # send email 
        else:
            form = EmailPostForm()
     else:
         form = EmailPostForm()
         return render(request, 'blog/share_mail.hmtl', {'post': post,'form': form})


"""def detail(request, slug):
     q = Post.objects.filter(slug__iexact=slug)
    if q.exists():
        q = q.first()
    else:
        return HttpResponse('<h1>Post Not Found</h1>')
    context = {

        'post': q
    }
    return render(request, 'posts/details.html', context)"""
def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
	comments = post.comments.filter(active=True)
	#print comments	
	# for comment in comments:
	# 	for reply in comment.replies.all():
	# 		print reply.body
	# 		# print reply.__dict__

	# rpy = Comment.objects.filter(active=True)	
	if request.method == 'POST':
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			# Assign the current post to the comment
			new_comment.post = post
			# Save the comment to the database
			new_comment.save()
	else:
		comment_form = CommentForm()

	return render(request,'blog//post_detail.html',{'post': post,'comments': comments,'comment_form': comment_form})