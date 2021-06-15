from django.urls import path
from . import views

urlpatterns =[
path('signup',views.signup),
path('login',views.login),


path('todo/completed',views.TodoCompletedList.as_view()),
path('todo/<int:pk>',views.TodoUpdateDestroyCreate.as_view()),
path('todo/<int:pk>/complete',views.TodoCompleteUpdate.as_view()),

]