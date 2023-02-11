from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.db.models import Q
from .models import *
# Create your views here.


def home(request):
    allPost = Article.objects.filter(status='published', visibility='public')
    context={'allPost':allPost}
    return render(request, 'index.html', context)

def newpost(request):
    if(request.method=='POST'):
        title = request.POST.get('title', None)
        content = request.POST.get('content', None)
        tags = [x.strip() for x in request.POST.get('tags', None).split(',')]
        slug = request.POST.get('slug', None)
        saveas = request.POST.get('saveas', None)
        iskecian = False
        if(request.user.email.endswith('@kongu.edu')):
            iskecian=True
        newarticle = Article(title=title, content=content, author=User.objects.get(username=request.user.username), status=saveas, slug=slug, iskecian=iskecian)
        newarticle.save()
        for tag in tags:
            newarticle.tags.add(tag)
        thome=reverse('home')
        return redirect(thome)
    allslugs = [post.slug for post in Article.objects.all()]
    print(allslugs)
    context={'allslugs':allslugs}
    return render(request, 'add_post.html', context)


def viewpost(request, slug):
    content=Article.objects.filter(slug=slug).first()
    bordercolor=''
    context={}
    followbtn=True
    if(request.user.username==content.author.username):
        followbtn=False
    if(content==None):
        context={'content':'Opps! No such content published yet... 😮'}
    elif((content.status=='published' and content.visibility=='public') or (content.status=='published' and content.visibility=='private' and content.author.username==request.user.username) or (content.status=='draft' and content.visibility!='deleted' and content.author.username==request.user.username)):
        if(content.author.email.endswith("@kongu.edu")):
            bordercolor='rgb(247, 250, 83)'
        context={'content':content, 'bordercolor':bordercolor, 'followbtn':followbtn}
    else:
        context={'content':'404 ERROR : Content not available might be removed/private 🤔'}
    return render(request, 'viewpost.html', context)

def allmypublicpost(request):
    if(request.user.is_authenticated):
        context={}
        allmypost=Article.objects.filter(author=request.user.id, visibility='public')
        context={'allmypublicpost':allmypost}
        return render(request, 'allmypublicpost.html', context)
    else:
        tlogin=reverse('login')
        return redirect(tlogin)

def allmyprivatepost(request):
    if(request.user.is_authenticated):
        context={}
        allmypost=Article.objects.filter(author=request.user.id, visibility='private')
        context={'allmyprivatepost':allmypost}
        return render(request, 'allmyprivatepost.html', context)
    else:
        tlogin=reverse('login')
        return redirect(tlogin)

def makepublicprivate(request, slug):
    if(request.user.is_authenticated):
        article=Article.objects.get(slug=slug)
        if(request.user.username==article.author.username):
            if(article.visibility=='public'):
                article.visibility='private'
                article.save()
                return redirect(reverse('allmypublicpost'))
            else:
                article.visibility='public'
                article.save()
                return redirect(reverse('allmyprivatepost'))
        else:
            return render(request, 'error.html', {'err':'You don\'t have an access to it...'})
    else:
        tlogin=reverse('login')
        return redirect(tlogin)


def deletePost(request, slug):
    if(request.user.is_authenticated):
        if(request.user.username == Article.objects.get(slug=slug).author.username):
            redirectlink=''
            curr = Article.objects.get(slug=slug)
            if(curr.status=='public'):
                redirectlink='allmypublicpost'
            else:
                redirectlink='allmyprivatepost'
            curr.visibility='deleted'
            curr.save()
            return redirect(reverse(redirectlink))
        else:
            return render(request, 'error.html', {'err':'ERROR 404 : You can\'t perform this action... 🤔'})
    else:
        tlogin = reverse('login')
        return redirect(tlogin)


def search(request):
    query = request.GET.get("q")
    if query:
        allpost = Article.objects.filter(
            Q(title__icontains=query) |
            Q(tags__name__in=[query])
        ).distinct().filter(status="published", visibility="public")
    else:
        allpost = Article.objects.none()
    print(allpost)
    return render(request, "index.html", {"allPost": allpost})


# @login_required
# def follow_unfollow(request, username):
#     user = get_object_or_404(User, username=username)
#     follow, created = Follow.objects.get_or_create(follower=request.user, followed=user)

#     if not created:
#         follow.delete()
#         action = "unfollowed"
#     else:
#         action = "followed"

#     return redirect("home")
# @login_required  
def follow(request, username):
    target_user = User.objects.get(username=username)
    Follow.objects.create(user=request.user, target=target_user)
    return redirect("home")

# @login_required  
def unfollow(request, username):
    target_user = User.objects.get(username=username)
    Follow.objects.filter(user=request.user, target=target_user).delete()
    return redirect("home")

