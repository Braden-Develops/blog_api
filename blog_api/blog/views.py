from datetime import datetime
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, parser_classes
from rest_framework.exceptions import AuthenticationFailed
from blog.models import Post, User
from blog.serializers import PostSerializer, UserSerializer
import datetime
import jwt
import os


class BlogPosts(APIView):
    """
    View to list all blog posts in the system
    """

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    # @todo Protect this endpoint
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


class RegisterUser(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)

        except Exception as e:
            return HttpResponseBadRequest(serializer.errors)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class Login(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        # (datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(0)).total_seconds() * 1000
        # int(time.time())

        payload = {
            'id': user.id,
            'exp': str((datetime.datetime.utcnow() + datetime.timedelta(minutes=60)).isoformat()),
            'iat': datetime.datetime.utcnow().isoformat()
        }
        datetime.datetime.tim

        token = jwt.encode(payload, os.getenv('JWTSECRET'), algorithm='HS256')
        # token = jwt.decode(token, os.getenv('JWTSECRET'), algorithms=['HS256'])

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Authentication failed')

        try:
            payload = jwt.decode(token, os.getenv(
                'JWTSECRET'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class Logout(APIView):
    def post(self, request):
        response = Response()

        response.delete_cookie('jwt')

        response.data = {
            'message': 'success'
        }

        return response
