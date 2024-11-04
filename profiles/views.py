

from django.contrib.auth.models import User
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest
from feed.models import Post
from followers.models import Follower
from .forms import ProfileImageUploadForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProfileDetailView(DetailView):
    http_method_names = ["get"]
    template_name = "profiles/detail.html"
    model = User
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.filter(author=user).count()
        context['total_followers'] = Follower.objects.filter(following=user).count()
        if self.request.user.is_authenticated:
            context['you_follow'] = Follower.objects.filter(following=user, followed_by = self.request.user).exists()

        return context


class FollowView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()

        if "action" not in data or "username" not in data:
            return HttpResponseBadRequest("Missing data")

        try:
            other_user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return HttpResponseBadRequest("Missing user")
 
        if data['action'] == "follow":
            # Follow
            follower, created = Follower.objects.get_or_create(
                followed_by=request.user,
                following=other_user
            )
        else:
            # Unfollow
            try:
                follower = Follower.objects.get(
                    followed_by=request.user,
                    following=other_user,
                )
            except Follower.DoesNotExist:
                follower = None

            if follower:
                follower.delete()

        return JsonResponse({
            'success': True,
            'wording': "Unfollow" if data['action'] == "follow" else "Follow"
        })
class ProfileImageUploadView(View):
    def get(self, request, username):
        user = get_object_or_404(Profile, user__username=username)
        form = ProfileImageUploadForm()
        return render(request, 'profiles/upload_image.html', {'form': form, 'user': user})

    def post(self, request, username):
        user = get_object_or_404(Profile, user__username=username)
        form = ProfileImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            user.image = form.cleaned_data['image']
            user.save()
            return redirect('profiles:detail', username=username)  # Redirect to the user's detail page
        return render(request, 'profiles/upload_image.html', {'form': form, 'user': user})