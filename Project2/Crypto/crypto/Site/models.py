from django.db import models


class GroupMember(models.Model):
    username = models.CharField(max_length=50)
    groupName = models.CharField(max_length=50)
    manager = models.BooleanField()


class FileObject(models.Model):
    filename = models.CharField(max_length=500)
    groupName = models.CharField(max_length=50)
    uploader = models.CharField(max_length=50)
    content = models.CharField(max_length=10000)
    encryptedKey = models.CharField(max_length=10000)
    iv = models.CharField(max_length=10000)


class Group(models.Model):
    groupName = models.CharField(max_length=50)
    publicKey = models.CharField(max_length=10000)
    privateKey = models.CharField(max_length=10000)
    manager = models.CharField(max_length=50)


class Control(models.Model):
    fileCounter = models.PositiveIntegerField()
