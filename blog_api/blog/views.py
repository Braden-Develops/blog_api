from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, parser_classes
from blog.models import Post
from blog.serializers import PostSerializer
import time

# Create your views here.


class BlogPosts(APIView):
    """
    View to list all blog posts in the system
    """
    
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            print(request.data)
            serializer = PostSerializer(data=request.data)
        except Exception as e:
            return HttpResponseBadRequest(e)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return HttpResponseBadRequest(serializer.errors)
