from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

from .models import User, POST, USERPROFILE


def index(request):
    if request.method == 'POST':
        post = request.POST['post']
        if post != "":
            post_save = POST.objects.create(USERNAME = request.user,POST=post)
            post_save.save()
            return HttpResponseRedirect(reverse('index'))
    posts = POST.objects.order_by('-id').all()
    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'network/index.html',{'page_obj':page_obj})

def profile(request,user):
    userr = User.objects.get(username = user)
    userr2 = User.objects.get(username = request.user)

    # FOLLOW AND UNFOLLOW
    userprofile = USERPROFILE.objects.get(USERNAME=userr)
    loggeduserprofile = USERPROFILE.objects.get(USERNAME=request.user)

    loggeduser = User.objects.get(username=request.user)
    userr = User.objects.get(username = user)

    if 'follow' in request.POST:
        userprofile.FOLLOWERS.add(loggeduser)
        loggeduserprofile.FOLLOWING.add(userr)
    if 'unfollow' in request.POST:
        userprofile.FOLLOWERS.remove(loggeduser)
        loggeduserprofile.FOLLOWING.remove(userr)
    profilefollowers = userprofile.FOLLOWERS.all()

    posts = POST.objects.filter(USERNAME = userr).order_by('-id')
    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request,'network/Profile.html',{'page_obj':page_obj,'userprofile':userprofile ,'profilefollowers':profilefollowers,'userr':userr,'userr2':userr2,'logged':loggeduser})

def following(request):
    loggeduser = USERPROFILE.objects.get(USERNAME = request.user)
    loggeduser_following = loggeduser.FOLLOWING.all()
    posts = POST.objects.filter(USERNAME__in= loggeduser_following).order_by('-id')
    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'network/following.html',{'page_obj':page_obj})

@csrf_exempt
def post_like(request, like_id):
    try:
        post = POST.objects.get(id = like_id)
        if request.method == 'POST':
            if request.user in post.LIKES.all():
                btn_class = "bi-heart"
                post.LIKES.remove(request.user)
                post.save()
            else:
                btn_class = "bi-heart-fill"
                post.LIKES.add(request.user)
                post.save()
        return JsonResponse({'status':0,'count':post.LIKES.count(),'btn_class':btn_class})
    except:
        return JsonResponse({'error':'error with liking post'})
    
@csrf_exempt
def edit(request, edit_id):
    try:
        post = POST.objects.get(pk=edit_id)
    except POST.DoesNotExist:
        return JsonResponse({"error": "post not found."}, status=404)     

    if request.method == "POST":
        data = json.loads(request.body)
        if data.get("POST") is not None:
            post.POST = data["POST"]
        post.save()
        return HttpResponse(status=204)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            login(request, user)
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        a1 = USERPROFILE.objects.create(USERNAME = request.user)
        a1.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
