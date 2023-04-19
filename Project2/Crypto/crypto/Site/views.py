import os

from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from . import system
from . import models


def index(request):
    return render(request, 'login.html')


def submit(request):
    name = str(request.POST.get('uname'))
    password = str(request.POST.get('psw'))
    request.session['name'] = name
    request.session['password'] = password
    if system.checkCredentials(name, password):
        return HttpResponseRedirect('home')
    else:
        return HttpResponseRedirect('badcredentials')


def badcredentials(request):
    template = loader.get_template('badcredentials.html')
    return HttpResponse(template.render())


def home(request):
    allmygroups = models.GroupMember.objects.all()
    allExistingGroups = models.Group.objects.all()
    users = User.objects.all()
    allFiles = models.FileObject.objects.all()
    otherUsers = []
    mygroups = []
    allGroups = []
    userList = []
    adminGroups = []
    fileList = []
    for user in users:
        if user != request.session['name']:
            otherUsers.append(user)
    for group in allmygroups:
        if group.username == request.session['name']:
            mygroups.append(group.groupName)
            if group.manager is True:
                adminGroups.append(group.groupName)
    otherGroups = [group for group in mygroups if group not in adminGroups]
    for group in allExistingGroups:
        allGroups.append(group.groupName)
    for user in users:
        userList.append(user.username)
    for file in allFiles:
        if file.groupName in mygroups:
            fileList.append(file.filename)
    context = {
        'groups': mygroups,
        'allGroups': allGroups,
        'users': userList,
        'adminGroups': adminGroups,
        'otherGroups': otherGroups,
        'otherUsers': otherUsers,
        'files': fileList
    }
    return render(request, 'home.html', context)


def createuser(request):
    return render(request, 'create.html')


def submitcreate(request):
    name = str(request.POST.get('uname'))
    password = str(request.POST.get('psw'))
    request.session['name'] = name
    request.session['password'] = password
    attempt = system.createUser(name, None, password)
    if attempt:
        return HttpResponseRedirect('home')
    else:
        return HttpResponseRedirect('badcredentials')


def upload(request):
    fileUpload = request.FILES.get('fileUpload')
    if fileUpload:
        filename = fileUpload.name
        postGroup = request.POST.get('postGroup')
        system.uploadFile(fileUpload, filename, postGroup, request.session['name'])
    return HttpResponseRedirect('files')


def add(request):
    user = request.GET['addUser']
    group = request.GET['addGroup']
    system.addUserFromGroup(user, group)
    return HttpResponseRedirect('home')


def remove(request):
    user = request.GET['removeUser']
    group = request.GET['removeGroup']
    system.removeUserFromGroup(user, group)
    return HttpResponseRedirect('home')


def exit(request):
    user = request.session['name']
    group = request.GET['exitGroup']
    system.removeUserFromGroup(user, group)
    return HttpResponseRedirect('home')


def create(request):
    groupName = request.GET['createGroup']
    user = request.session['name']
    system.createGroup(groupName, user)
    system.addUserFromGroup(user, groupName)
    return HttpResponseRedirect('home')


def delete(request):
    groupName = request.GET['deleteGroup']
    system.deleteGroup(groupName)
    return HttpResponseRedirect('home')


def change(request):
    groupName = request.GET['changedGroup']
    newManager = request.GET['newManager']
    system.changeManager(newManager, groupName)
    return HttpResponseRedirect('home')


def deletefile(request, group, fileDelete):
    groupName = group
    system.deleteFile(fileDelete, groupName)
    return HttpResponseRedirect('/files')


def download(request, fileDownload, group):
    filename = fileDownload
    groupName = group
    system.downloadFile(filename, groupName)
    return HttpResponseRedirect('/files')


def files(request):
    allmygroups = models.GroupMember.objects.all()
    allExistingGroups = models.Group.objects.all()
    users = User.objects.all()
    allFiles = models.FileObject.objects.all()
    otherUsers = []
    mygroups = []
    allGroups = []
    userList = []
    adminGroups = []
    fileList = []
    for user in users:
        if user != request.session['name']:
            otherUsers.append(user)
    for group in allmygroups:
        if group.username == request.session['name']:
            mygroups.append(group.groupName)
            if group.manager is True:
                adminGroups.append(group.groupName)
    otherGroups = [group for group in mygroups if group not in adminGroups]
    for group in allExistingGroups:
        allGroups.append(group.groupName)
    for user in users:
        userList.append(user.username)
    for file in allFiles:
        if file.groupName in mygroups:
            fileList.append(file)
    context = {
        'groups': mygroups,
        'allGroups': allGroups,
        'users': userList,
        'adminGroups': adminGroups,
        'otherGroups': otherGroups,
        'otherUsers': otherUsers,
        'files': fileList
    }
    return render(request, 'files.html', context)
