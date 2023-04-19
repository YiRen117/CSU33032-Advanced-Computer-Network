from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *
from .encryption import *
import os
from django.http import HttpResponse, Http404, StreamingHttpResponse

def createUser(name, email, password):
    check = User.objects.filter(username=name).count()
    if check == 0:
        user = User.objects.create_user(name, email, password)
        user.save()
        return True
    else:
        return False


def checkCredentials(name, password):
    user = authenticate(username=name, password=password)
    if user is not None:
        return True
    else:
        return False


def addUserFromGroup(user, group):
    groupMembers = GroupMember.objects.all()
    for membership in groupMembers:
        if membership.username == user and membership.groupName == group:
            return  # already in group
    newMembership = GroupMember(username=user, groupName=group, manager=False)
    newMembership.save()


def userInGroup(user, group):
    groupMembers = GroupMember.objects.all()
    for membership in groupMembers:
        if membership.username == user and membership.groupName == group:
            return True
    return False


def removeUserFromGroup(user, group):
    groupMembers = GroupMember.objects.all()
    for membership in groupMembers:
        if membership.username == user and membership.groupName == group:
            membership.delete()


def changeManager(new, groupName):
    addUserFromGroup(new, groupName)
    group = Group.objects.get(groupName=groupName)
    current = group.manager
    group.manager = new
    currentManager = GroupMember.objects.get(username=current, groupName=groupName)
    newManager = GroupMember.objects.get(username=new, groupName=groupName)
    currentManager.manager = False
    newManager.manager = True
    currentManager.save()
    newManager.save()
    group.save()


def createGroup(groupName, user):
    privateKey = RSA.generate(1024)
    publicKey = privateKey.publickey()
    privateKeyString = privateKey.export_key().decode()
    publicKeyString = publicKey.export_key().decode()
    group = Group(groupName=groupName, publicKey=publicKeyString, privateKey=privateKeyString, manager=user)
    manager = GroupMember(username=user, groupName=groupName, manager=True)
    group.save()
    manager.save()


def deleteGroup(groupName):
    groups = Group.objects.all()
    for group in groups:
        if groupName in group.groupName:
            group.delete()
            connections = GroupMember.objects.all()
            for membership in connections:
                if membership.groupName in group.groupName:
                    membership.delete()


def uploadFile(file, filename, groupName, uploader):
    group = Group.objects.get(groupName=groupName)
    publicKeyString = group.publicKey
    crypticContent, encrypted_key, iv = encrypt(publicKeyString, file)
    fileUpload = FileObject(filename=filename, groupName=groupName, uploader=uploader, encryptedKey=encrypted_key, iv=iv)
    fileUpload.content = crypticContent
    fileUpload.save()


def deleteFile(filename, groupName):
    file = FileObject.objects.get(filename=filename, groupName=groupName)
    file.delete()


def downloadFile(filename, groupName):
    group = Group.objects.get(groupName=groupName)
    file = FileObject.objects.get(filename=filename)
    encryptedKey = file.encryptedKey
    iv = file.iv
    ciphertext = file.content
    privateKeyString = group.privateKey
    decryptedFile = decrypt(encryptedKey, privateKeyString, ciphertext, iv)
    try:
        response = StreamingHttpResponse(open(os.path.basename(decryptedFile), 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(decryptedFile)
        return response
    except Exception:
        raise Http404
