from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, RegisterSerializer


def register_page(request):
    if request.method == 'POST':
        data = {'username': request.POST.get('username'), 'email': request.POST.get('email'), 'password': request.POST.get('password')}
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return redirect('home')
        for error in serializer.errors.values():
            messages.error(request, str(error[0]))
    return render(request, 'users/register.html')


def login_page(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Login yoki parol noto‘g‘ri.')
    return render(request, 'users/login.html')


def logout_page(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    return render(request, 'users/profile.html', {'reviews': request.user.reviews.select_related('book').all()})


class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = RefreshToken.for_user(serializer.validated_data['user'])
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
