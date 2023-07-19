from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account

class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'



class LoginSerializer(ModelSerializer):
    email = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)

    class Meta:
        model = User
        fields = [
            'email',
            'password'
        ]


class UserInfoSerializer(ModelSerializer):
    additional_info= serializers.SerializerMethodField('get_additional_info')
    
    def get_additional_info(self, instance):
        user_info_instance= Account.objects.get(user=instance.id)
        return AccountSerializer(user_info_instance).data
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'last_login', 'is_active', 'additional_info')


class UserReadInfoSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'last_login', 'is_active')


class UserInfoUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username')


class ChangePasswordSerializer(ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class RegistrationSerializers(ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        model._meta.get_field('email')._unique = True
        fields = ['email', 'username', 'last_name', 'first_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True}
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            last_name=self.validated_data['last_name'],
            first_name=self.validated_data['first_name'],
        )
        # if User.objects.filter(email=user.email).exists():
        #     raise serializers.ValidationError("Email exists")
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({password: "Passwords Must Match"})
        user.set_password(password)
        user.save()

        return user
