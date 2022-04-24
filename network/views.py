from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required
from .models import User , Posts,Follow,Like
import json
from django.conf import settings
from django.core.paginator import Paginator

def index(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    getallposts = Posts.objects.order_by("-timestamp").all()


    if not getallposts:
        return render(request, "network/index.html",{"userpostlike":None,"posts":None , "page_obj":None})

    paginator = Paginator(getallposts, 10)

    getPage = int(request.GET.get('p', 1))


    page_obj = paginator.get_page(getPage)




    getuserpostlike = [Like.objects.filter(post=postid,like=request.user.id).values("post") for postid in getallposts]
    userpostlike = []

    for i in range(len(getuserpostlike)):


        try:
            userpostlike.append(getuserpostlike[i][0])
        except IndexError as error:
            print(error)


    return render(request, "network/index.html",{"userpostlike":userpostlike,"posts":getallposts , "page_obj":page_obj})

def profile(request,userid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    try:
        getUser = User.objects.get(id=userid)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))


    nbfollowers = Follow.objects.filter(follow=userid).count()
    nbfollowing = Follow.objects.filter(useradmin=userid).count()



    if userid == request.user.id:
        checkfollow = 2#hide follow
    else:
        checkfollow = getUser.userfollow.filter(useradmin=request.user.id).count()




    getuserposts = Posts.objects.filter(owner=userid).order_by("-timestamp").all()




    getuserpostlike = [Like.objects.filter(post=postid,like=request.user.id).values("post") for postid in getuserposts]

    userpostlike = []

    for i in range(len(getuserpostlike)):


        try:
            userpostlike.append(getuserpostlike[i][0])
        except IndexError as error:
            print(error)


    return render(request, "network/user.html",{"username":getUser.username,"userid":userid,"posts":getuserposts,"userpostlike":userpostlike,"followers":nbfollowers,"following":nbfollowing,"checkfollow":checkfollow})

def following(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    getFollowing = Follow.objects.filter(useradmin=request.user.id).values("follow")


    follownigidIN = []
    for follownigid in getFollowing:
        follownigidIN.append(follownigid["follow"])


    getfollowingpost = Posts.objects.filter(owner__in=follownigidIN).order_by("-timestamp")

    #OLDgetfollowingpost = None
    #OLDgetfollowingpost = [Posts.objects.filter(owner=follownigid["follow"]).values("body") for follownigid in getFollowing]


    getuserpostlike = [Like.objects.filter(post=postid,like=request.user.id).values("post") for postid in getfollowingpost]

    userpostlike = []

    for i in range(len(getuserpostlike)):
        try:
            userpostlike.append(getuserpostlike[i][0])
        except IndexError as error:
            print(error)


    return render(request, "network/following.html",{"posts":getfollowingpost,"userpostlike":userpostlike})


@csrf_exempt
def follow(request):


    if request.method == "PUT":
        data = json.loads(request.body)

        getIdProfile = data.get("id")

        if getIdProfile == request.user.id:
            return JsonResponse({"error": "You are following your self :p "})

        follow = 0
        try:
            profile = Follow.objects.get(useradmin=request.user.id,follow=getIdProfile)
        except Follow.DoesNotExist:
            follow = 1

        addremove = None
        valuefollow = None

        userProfile = User.objects.get(id=getIdProfile)
        if follow == 1 :
            profile = Follow(useradmin=request.user.id,follow=userProfile)
            addremove = "remove"
            valuefollow = "Unfollow"
            profile.save()
        else:
            profile=Follow.objects.filter(useradmin=request.user.id,follow=userProfile).delete()
            addremove = "add"
            valuefollow = "Follow"


        return JsonResponse({"addremove":addremove,"valuefollow":valuefollow})

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

@csrf_exempt
def like(request):
    if request.method == "PUT":
        data = json.loads(request.body)

        getIdPost = int(data.get("postid"))




        try:
            getPost = Posts.objects.get(id=getIdPost)
        except Posts.DoesNotExist:
            return JsonResponse({"error": "Post not found."})

        like_dislike = None



        like = 1
        try:
            likeBDD = Like.objects.get(post=getPost,like=request.user)
        except Like.DoesNotExist:
            like=0

        if like == 0 :
            postlike = Like(post=getPost,like=request.user)


            getPost.like = getPost.like+1

            like_dislike = "dislike"
            postlike.save()
            getPost.save()
        else:
            postlike=Like.objects.filter(post=getPost,like=request.user).delete()
            getPost.like = getPost.like-1
            getPost.save()
            like_dislike = "like"

        return JsonResponse({"likedislike":like_dislike})

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)
@csrf_exempt
def newpost(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)

    setnewpost = Posts(
      owner=request.user,
      body=data.get("posttxt")
    )
    setnewpost.save()

    return JsonResponse({"error":0 ,"userid":request.user.id,"username":request.user.username , "id": setnewpost.id ,"date":setnewpost.timestamp.strftime("%b %d %Y, %I:%M %p")})

@csrf_exempt
@login_required(login_url='/login')
def editpost(request):

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login!"}, status=400)


    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)


    try:
        seteditpost = Posts.objects.get(id=data.get("postid"),owner=request.user)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    seteditpost.body = data.get("posttxt")
    seteditpost.save()

    return JsonResponse({"error":0 ,"userid":request.user.id,"username":request.user.username , "id": seteditpost.id ,"date":seteditpost.timestamp.strftime("%b %d %Y, %I:%M %p") , "like":seteditpost.like})

@csrf_exempt
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

        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
