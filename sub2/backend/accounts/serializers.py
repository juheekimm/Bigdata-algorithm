from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from rest_framework.authtoken.models import Token
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.registration.views import RegisterView
from accounts.models import Profile
from rest_auth.views import LoginView
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('id','nickname', 'gender', 'age')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    user = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = User
        # fields = ('username', 'email', 'password', 'firstname', 'last name')
        fields = '__all__'

class CustomRegistrationSerializer(RegisterSerializer):

  def custom_signup(self, request, user):
      print("custom_signup")
      user_id = user.id
      gender = request.POST['gender']
      age = request.POST['age']
      nickname = request.POST['nickname']
      data = Profile(user_id=user_id, gender = gender, age=age, nickname=nickname)
      data.save()

class CustomRegistrationView(RegisterView):
  serializer_class = CustomRegistrationSerializer

class CustomLoginView(LoginView):

    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': self.user,
                'token': self.token
            }
            serializer = serializer_class(instance=data,
                                          context={'request': self.request})
        else:
            serializer = serializer_class(instance=self.token,
                                          context={'request': self.request})

        profile = Profile.objects.get(user_id=self.user.pk)

        
        profileSerializer = ProfileSerializer(profile)
        serializer.data['user']['profile'] = profileSerializer.data
        response = Response(serializer.data, status=status.HTTP_200_OK)
        
        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_jwt.settings import api_settings as jwt_settings
            if jwt_settings.JWT_AUTH_COOKIE:
                from datetime import datetime
                expiration = (datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,
                                    self.token,
                                    expires=expiration,
                                    httponly=True)
        return response

# class RegisterSerializer(serializers.Serializer):
#     username = serializers.CharField(
#         max_length=get_username_max_length(),
#         min_length=allauth_settings.USERNAME_MIN_LENGTH,
#         required=allauth_settings.USERNAME_REQUIRED
#     )
#     email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
#     password1 = serializers.CharField(write_only=True)
#     password2 = serializers.CharField(write_only=True)

#     def validate_username(self, username):
#         username = get_adapter().clean_username(username)
#         return username

#     def validate_email(self, email):
#         email = get_adapter().clean_email(email)
#         if allauth_settings.UNIQUE_EMAIL:
#             if email and email_address_exists(email):
#                 raise serializers.ValidationError(
#                     _("A user is already registered with this e-mail address."))
#         return email

#     def validate_password1(self, password):
#         return get_adapter().clean_password(password)

#     def validate(self, data):
#         if data['password1'] != data['password2']:
#             raise serializers.ValidationError(_("The two password fields didn't match."))
#         return data

#     def custom_signup(self, request, user):
#         pass

#     def get_cleaned_data(self):
#         return {
#             'username': self.validated_data.get('username', ''),
#             'password1': self.validated_data.get('password1', ''),
#             'email': self.validated_data.get('email', '')
#         }

#     def save(self, request):
#         adapter = get_adapter()
#         user = adapter.new_user(request)
#         self.cleaned_data = self.get_cleaned_data()
#         adapter.save_user(request, user, self)
#         self.custom_signup(request, user)
#         setup_user_email(request, user, [])
#         print("############")
#         print(user)
#         return user
