from django.views.generic import TemplateView

from .forms import PostForm
from .models import Post

from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from django.core import serializers

from Accounts.views import get_user_type


# Create the new bulletin posts
class CreatePostView(TemplateView):
    template_name = 'bulletin/base.html'

    def get(self, request, *args, **kwargs):
        form = PostForm()
        user = get_user_type(request)
        args = {'form': form, 'obj': user['obj'], 'user_type': user['user_type']}
        return render(request, self.template_name, args)

    # Save newly created post information to database
    def post(self, request):
        if request.method == "POST":
            form = PostForm(request.POST)
            # check if post is submitted
            if request.POST.get("submitbutton"):
                if form.is_valid():
                    post = form.save(commit=False)
                    post.author = request.user
                    post.author_updated = request.user
                    post.release_date = timezone.now()
                    post.update_date = timezone.now()
                    post.status = True  # post is published for everyone to view
                    post.save()
                    return redirect('all_posts')


# view the details of each published and created post
def PostDetailView(request, pk):
    context = {}

    if request.method == 'POST' and request.is_ajax():
        post_id = request.POST.get('post_id')
        print(post_id)

        post = Post.objects.get(pk=post_id)
        serialized_post = serializers.serialize('json', [post])
        return JsonResponse({'post': serialized_post}, safe=False)


def AllPosts(request):
    posts = Post.objects.filter(status=True).order_by('-release_date')
    user = get_user_type(request)
    args = {'posts': posts, 'obj': user['obj'], 'user_type': user['user_type']}
    return render(request, 'bulletin/allPosts.html', args)
