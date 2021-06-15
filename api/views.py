from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import TodoSerializer, TodoCompleteSerializer
from posts.models import Post
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(data['username'], password=data['password'])
            user.save()
            token = Token.objects.create(user=user)
            login(request,user)
            return JsonResponse({"token":str(token)},status=201)
        except IntegrityError:
            return JsonResponse({"error":'dummytoken not created'},status=400)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = authenticate(request,user=data['username'],password=data['password'])
            if user is None:
                return JsonResponse({"error":"could not login"})
            else:
                try:
                    token = Token.objects.get(user=user)
                except:
                    token = Token.objects.create(user=user)
                return JsonResponse({"token":str(token)},status=201)
        except IntegrityError:
            return JsonResponse({"error":'dummytoken not created'},status=400)


class  TodoCompletedList(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(user=user).order_by('-created')
    
    def perform_create(self,serializer):
        serializer.save(user= self.request.user)

class TodoUpdateDestroyCreate(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(user=user)

class  TodoCompleteUpdate(generics.UpdateAPIView):
    #make some only readonly change serializer
    serializer_class = TodoCompleteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.instance.datecomplete = timezone.now()
        serializer.save()


