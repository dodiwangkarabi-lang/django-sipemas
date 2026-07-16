from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny

from django.db import transaction

from drf_spectacular.utils import extend_schema

# ----- models -----
from accounts.models import (
    Masyarakat
)
from django.contrib.auth.models import User

# ----- serializer -----
from . import serializers

# ----- service -----
from accounts.services import services

# ----- daftar -----
@extend_schema(
    tags=["User"],
    summary="Daftar User",
    responses=serializers.UserSerializer,
    request=serializers.DaftarAkunMasyarakat
)
class DaftarMasyarakatAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = serializers.DaftarAkunMasyarakat(data=request.data)
        serializer_valid = serializer.is_valid()
        
        if serializer_valid:
            # user = serializer.save()
            data = serializer.validated_data
            user_obj = services.daftar_akun(
                alamat=data['alamat'],
                email=data['email'],
                password=data['password'],
                username=data['username'],
                nik=data['nik'],
                nama=data['nama'],
                no_hp=data['no_hp']
            )
            
            user_serializer = serializers.UserSerializer(user_obj)
            
            return Response({
                "is_success": True,
                "message": "berhasil daftar akun masyarakat",
                "data": user_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "is_success": False,
            "message": "gagal daftar akun masyarakat",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# ----- ubah password -----
@extend_schema(
    tags=["User"],
    summary="Ubah Password",
    responses=serializers.UserUpdateProfileSerialzer,
    request=serializers.ChangePasswordSerializer
)
class UbahPasswordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer_valid = serializer.is_valid()
        
        if serializer_valid:
            data = serializer.validated_data
            user = request.user
            
            user.set_password(data['new_password'])
            user.save()
            
            return Response({
                "is_success": True,
                "message": "berhasil ubah password",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            "is_success": False,
            "message": "gagal ubah password",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    tags=["User"],
    summary="User Update Profile + Masyarakat Update Profile",
    responses=serializers.UserUpdateProfileSerialzer,
    request=serializers.UserUpdateProfileSerialzer
)
class UpdateProfileMasyarakatAPIView(APIView):
    
    @transaction.atomic
    def patch(self, request):
        request_serializer = serializers.UserUpdateProfileSerialzer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        
        data = request_serializer.validated_data
        
        # update user
        user_serializer = serializers.UserUpdateSerializer(request.user, data=data, partial=True)
        user_valid = user_serializer.is_valid()
        
        masyarakat_serializer = serializers.MasyarakatSerializer(request.user.masyarakat, data=data, partial=True)
        masyarakat_valid = masyarakat_serializer.is_valid()
        
        if not user_valid or not masyarakat_valid:
            user_erros = user_serializer.errors
            masyarakat_erros = masyarakat_serializer.errors
            all_errors = {
                **user_erros,
                **masyarakat_erros
            }
            return Response({
                "data": all_errors,
                "is_success": False,
                "message": "gagal update data"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # simpan
        user_serializer.save()
        masyarakat_serializer.save()
        
        return Response({
            "data": request_serializer.data,
            "is_success": True,
            "message": "berhasil update data"
        }, status=status.HTTP_200_OK)
        
        # ----- validasi -----
        # if user_serializer.is_valid() and masyarakat_serializer.is_valid():
        #     user_serializer.save()
        #     masyarakat_serializer.save()
            
        #     return Response({
        #         "data": user_serializer.data,
        #         "is_success": True
        #     }, status=status.HTTP_200_OK)
        # else:
        #     return Response({
        #         "data": user_serializer.errors,
        #         "is_success": False
        #     }, status=status.HTTP_400_BAD_REQUEST)
    
    

class MasyarakatListView(APIView):
    def get(self, request, format=None):
        masyarakat_qs = Masyarakat.objects.select_related('user').all()
        serializer = serializers.MasyarakatSerializer(masyarakat_qs, many=True)
        
        return Response(serializer.data)
    
@extend_schema(
    tags=["User"],
    summary="User Detail + Masyarakat Detail",
    responses=serializers.UserSerializer
)
class AccountView(APIView):
    
    def get(self, request):
        user = request.user
        serializer = serializers.UserSerializer(user)
        
        return Response(serializer.data)
    
@extend_schema(
    tags=["User"],
    summary="User Detail",
    description="Detail User",
)
class UserDetailView(APIView):
    def get(self, request):
        user = request.user
        serializer = serializers.UserSerializer(user)
        
        return Response(serializer.data)

@extend_schema(
    tags=["Masyarakat"],
    summary="Masyarakat Detail",
    description="Detail Masyarakat",
)
class MasyarakatDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, masyarakat_id, format=None):
        masyarakat = Masyarakat.objects.get(id=masyarakat_id)
        serializer = serializers.MasyarakatSerializer(masyarakat)
        
        return Response(serializer.data)