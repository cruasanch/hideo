from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Video, Comment
from django.contrib.auth import get_user_model
User = get_user_model()
from . import form
from django.template.context_processors import csrf
from django.contrib import auth

def show(request):
    content = []                  #[  [video, [(comment, name),(comment,name),()]]   ,  [video, [comments..]]     ]
    for vid in Video.objects.all():
        tmp = []
        tmp.append(vid)
        comments = Comment.objects.filter(Comment_Video_id=vid.id)
        list_users = []
        for com in comments:
            list_users.append(User.objects.get(id=com.Comment_User_id))
        tmp.append(list(zip(comments, list_users)))
        content.append(tmp)
    return render(request,'mytemplate.html', {"content":content, "user":auth.get_user(request).username})
    return render(request, 'mytemplate.html', {"name":"Bogdan"})
    return HttpResponse("Hello")


def ShowOneVideo(request, video_id):
    args = {}
    args.update(csrf(request))
    args['form'] = form.CommentForm
    args['video'] = Video.objects.get(id = video_id)
    args['user'] = auth.get_user(request).username
    comments = Comment.objects.filter(Comment_Video_id = video_id)
    Users_list = []
    for com in comments:
        Users_list.append(User.objects.get(id=com.Comment_User_id))
    args['comments'] = list(zip(comments, Users_list))
    return render(request, 'onevideo.html', args)


def addcomment(request, video_id):
    print(request.POST['id_password'])
    if request.POST:
        forma = form.CommentForm(request.POST)
        if forma.is_valid():
            comment = forma.save(commit = False)
            comment.Comment_Video = Video.objects.get(id=video_id)
            comment.Comment_User = User.objects.get(id=request.user.id)
            forma.save()
    return redirect("/games/showOne/" + str(video_id) + "/")


def sign(request):
    if request.POST:
        user = User.objects.create_user(username=request.POST.get('username', ""),
                                        email=request.POST.get('email',""),
                                        password=request.POST.get('password',""))
        if user:
            auth.login(request, user)
        return redirect('/games/')
    else:
        args = {}
        args.update(csrf(request))
        args['form'] = form.UserForm
        args['url'] = "/games/sign/"
        args['user'] = auth.get_user(request).username
        return render(request, 'sign.html', args)

def out(request):
    auth.logout(request)
    return redirect('/games/')

def inn(request):
    if request.POST:
        user = auth.authenticate(username=request.POST.get('username', ""),
                                 password=request.POST.get('password', ""))
        if user:
            auth.login(request, user)
            return redirect('/games/')
        else:
            args = {}
            args.update(csrf(request))
            args['user'] = auth.get_user(request).username
            args['form'] = form.UserFormL
            args['url'] = '/games/in/'
            args["error"] = "Такой пользователь не найден"
            return render(request, 'sign.html', args)
    else:
        args = {}
        args.update(csrf(request))
        args['user'] = auth.get_user(request).username
        args['form'] = form.UserFormL
        args['url'] = '/games/in/'
        return render(request, 'sign.html', args)


def addliketovideo(request, video_id):
    video = Video.objects.get(id = video_id)
    video.Video_likes += 1
    video.save()
    return redirect('/games/showOne/' + str(video_id))


def addliketocomment(request, comment_id):
    comment = Comment.objects.get(id = comment_id)
    comment.Comment_likes += 1
    comment.save()
    idvideo = comment.Comment_Video_id
    return redirect('/games/showOne/' + str(idvideo))


def ajax(request):
    if request.GET:
        idvideo = request.GET['addlike']
        video = Video.objects.get(id=idvideo)
        video.Video_likes += 1
        video.save()
    return HttpResponse(video.Video_likes)

def ajax1(request):
    if request.GET:
        comment_id = request.GET['addlike']
        comment = Comment.objects.get(id=comment_id)
        comment.Comment_likes += 1
        comment.save()
    return HttpResponse(comment.Comment_likes)