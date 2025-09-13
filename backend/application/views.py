from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.views import APIView
from .models import Scholarship

from .models import *
from .serializers import *
class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.filter(is_superuser=False).order_by('-id')
    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        return Response({'message': 'User created successfully'})
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data["user"] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff, 
            "is_superuser": user.is_superuser, 
        }
        return data
    
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
class ScholarshipCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ScholarshipSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
class ScholarshipListView(generics.ListAPIView):
    queryset = Scholarship.objects.all()
    serializer_class = ScholarshipSerializer
    permission_classes = [permissions.IsAuthenticated]

class ScholarshipUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Scholarship.objects.all()
    serializer_class = ScholarshipSerializer
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_scholarship(request, scholarship_id):
    user = request.user
    try:
        scholarship = Scholarship.objects.get(pk=scholarship_id)
    except Scholarship.DoesNotExist:
        return Response({'error': 'Scholarship not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Prevent duplicate application
    if ScholarshipApplication.objects.filter(student=user, scholarship=scholarship).exists():
        return Response({'error': 'Already applied to this scholarship.'}, status=status.HTTP_400_BAD_REQUEST)

    application = ScholarshipApplication.objects.create(student=user, scholarship=scholarship)
    serializer = ScholarshipApplicationSerializer(application)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_applications(request):
    user = request.user
    applications = ScholarshipApplication.objects.filter(student=user).select_related('scholarship')
    data = [
        {
            'id': app.id,
            'title': app.scholarship.title,
            'provider': app.scholarship.provider,
            'amount': app.scholarship.amount,
            'deadline': app.scholarship.application_deadline,
            'academic_level': app.scholarship.academic_level,
            'status': app.status,
            'applied_on': app.application_date,
        }
        for app in applications
    ]
    return Response(data)


@api_view(['GET'])
def all_applications(request):
    applications = ScholarshipApplication.objects.select_related('student', 'scholarship')
    data = [
        {
            'id': app.id,
            'student_name': app.student.username,
            'student_email': app.student.email,
            'title': app.scholarship.title,
            'provider': app.scholarship.provider,
            'amount': app.scholarship.amount,
            'status': app.status,
            'applied_on': app.application_date,
        }
        for app in applications
    ]
    return Response(data)

@api_view(['PATCH'])
def update_application_status(request, pk):
    try:
        app = ScholarshipApplication.objects.get(id=pk)
    except ScholarshipApplication.DoesNotExist:
        return Response({'error': 'Application not found'}, status=404)

    new_status = request.data.get('status')
    if new_status not in dict(ScholarshipApplication.STATUS_CHOICES):
        return Response({'error': 'Invalid status'}, status=400)

    app.status = new_status
    app.save()
    return Response({'success': True, 'status': app.status})