from rest_framework import serializers

# from rest_framework.exceptions import ValidationError

from django.core.exceptions import ValidationError

# ----- models -----
from accounts.models import (
    Masyarakat, Petugas
)
from django.contrib.auth.models import User, Group

from django.contrib.auth.password_validation import validate_password

class DaftarAkunMasyarakat(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=True, error_messages={"required": "Username harus diisi"})
    email = serializers.EmailField(max_length=254, required=True, error_messages={"required": "Email harus diisi"})
    password = serializers.CharField(max_length=128, required=True, error_messages={"required": "Password harus diisi"})
    
    nik = serializers.CharField(max_length=16, required=True, error_messages={"required": "NIK harus diisi"})
    nama = serializers.CharField(max_length=100, required=True, error_messages={"required": "Nama harus diisi"})
    alamat = serializers.CharField(max_length=255, required=True, error_messages={"required": "Alamat harus diisi"})
    no_hp = serializers.CharField(max_length=20, required=True, error_messages={"required": "Nomor HP harus diisi"})
    
    def validate_username(self, value):
        
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username sudah terdaftar")
        
        
        return value
    
    def validate_no_hp(self, value):
        if len(value) != 12:
            raise serializers.ValidationError("Nomor HP harus terdiri dari 12 karakter")
        
        if not value.isdigit():
            raise serializers.ValidationError("Nomor HP harus berupa angka")
        
        if Masyarakat.objects.filter(no_hp=value).exists():
            raise serializers.ValidationError("Nomor HP sudah terdaftar")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email sudah terdaftar")
        return value
    
    def validate_nik(self, value):
        # panjang nik
        if len(value) != 16:
            raise serializers.ValidationError("NIK harus terdiri dari 16 karakter")
        
        # nik harus angka
        if not value.isdigit():
            raise serializers.ValidationError("NIK harus berupa angka")
        
        if Masyarakat.objects.filter(nik=value).exists():
            raise serializers.ValidationError("NIK sudah terdaftar")
        
        return value

# serializer ubah password
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Password lama tidak sesuai")
        return value
    
    def validate_new_password(self, value):
        user = self.context['request'].user
        
        # Validasi sesuai AUTH_PASSWORD_VALIDATORS
        try:
            validate_password(value, user)
        except ValidationError as e:
            errors = []

            for message in e.messages:
                if message == "This password is too short. It must contain at least 8 characters.":
                    errors.append("Password minimal 8 karakter.")
                elif message == "This password is too common.":
                    errors.append("Password terlalu umum.")
                elif message == "This password is entirely numeric.":
                    errors.append("Password tidak boleh hanya terdiri dari angka.")
                elif message == "The password is too similar to the username.":
                    errors.append("Password terlalu mirip dengan username.")
                else:
                    errors.append(message)

            raise serializers.ValidationError(errors)
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] == attrs['old_password']:
            raise serializers.ValidationError("Password baru tidak boleh sama dengan password lama")
        return attrs

class UserUpdateProfileSerialzer(serializers.Serializer):
    nik = serializers.CharField(required=False)
    nama = serializers.CharField(required=False)
    alamat = serializers.CharField(required=False)
    no_hp = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class MasyarakatSerializer(serializers.ModelSerializer):
    # read only user
    # user = UserSerializer(read_only=True)
    
    class Meta:
        model = Masyarakat
        # fields = ['id', 'nik', 'nama', 'alamat', 'no_hp']
        exclude = ['user']
        
class PetugasSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Petugas
        # exclude user
        exclude = ['user']
        # fields = ['id', 'user', 'jabatan', 'no_hp']
        

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'profile']
        
    def get_role(self, obj) -> str:
        group = obj.groups.first()
        return group.name if group else None
    
    def get_profile(self, obj) -> dict | None:
        if hasattr(obj, "masyarakat"):
            return MasyarakatSerializer(obj.masyarakat).data

        if hasattr(obj, "petugas"):
            return PetugasSerializer(obj.petugas).data

        return None
    
# =====================================================
# response kepeluan doc
# =====================================================\
class UpdateProfileResponseSerializer(serializers.Serializer):
    data = UserSerializer()
    is_success = serializers.BooleanField()