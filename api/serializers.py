from rest_framework import serializers
from posts.models import Post


class  TodoSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    datecompleted = serializers.ReadOnlyField()
    class Meta:
        model = Post
        fields = ['title','url','poster']


class  TodoCompleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id']
        read_only_fields = ['title','url','poster']