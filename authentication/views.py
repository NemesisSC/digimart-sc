from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, UntypedToken
from django.contrib.auth.hashers import check_password
from .serializer import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
import system_manager.views


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def tokenObtainPair(request):

    try:

        login_serializer = LoginSerializer(data=request.data)

        if login_serializer.is_valid():
            email = login_serializer.validated_data.get('email')
            password = login_serializer.validated_data.get('password')
            # if "@" in email:
            #     user_instance = User.objects.get(email=email)
            # else:
            user_instance = User.objects.get(email=email)
            if check_password(password, user_instance.password):
                refresh = RefreshToken.for_user(user_instance)
                return Response({
                    "code": status.HTTP_200_OK,
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'token_type': str(refresh.payload['token_type']),
                    'expiry': refresh.payload['exp'],
                    'user_object': UserInfoSerializer(user_instance).data,
                })
            else:
                return Response({
                    "code": status.HTTP_401_UNAUTHORIZED,
                    "message": "No active account found with the given credentials",
                    "status_code": 401,
                    "errors": [
                        {
                            "status_code": 401,
                            "message": "No active account found with the given credentials"
                        }
                    ]
                })
        else:
            return Response({
                "code": status.HTTP_401_UNAUTHORIZED,
                "message": "No active account found with the given credentials",
                "status_code": 401,
                "errors": [
                    {
                        "status_code": 401,
                        "message": "Either Phone or Password or both not given"
                    }
                ]})
    except Exception as e:
        return Response({
            "code": status.HTTP_401_UNAUTHORIZED,
            "message": str(e),
            "status_code": 401,
            "errors": [
                {
                    "status_code": 401,
                    "message": str(e)
                }
            ]
        })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def tokenObtainPairAdmin(request):
    print(request.body)
    try:

        login_serializer = LoginSerializer(data=request.data)

        if login_serializer.is_valid():
            email = login_serializer.validated_data.get('email')
            password = login_serializer.validated_data.get('password')
            # if "@" in email:
            #     user_instance = User.objects.get(email=email)
            # else:
            user_instance = User.objects.get(email=email)
            
            if not user_instance.is_staff:
                return Response({
                    "code": status.HTTP_401_UNAUTHORIZED,
                    "message": "Only admins can log in",
                    "status_code": 401,
                    "errors": [
                        {
                            "status_code": 401,
                            "message": "Only admins can log in"
                        }
                    ]
                })
            
            
            if check_password(password, user_instance.password):
                refresh = RefreshToken.for_user(user_instance)
                return Response({
                    "code": status.HTTP_200_OK,
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'token_type': str(refresh.payload['token_type']),
                    'expiry': refresh.payload['exp'],
                    'user_object': UserInfoSerializer(user_instance).data,
                    
                })
            else:
                return Response({
                    "code": status.HTTP_401_UNAUTHORIZED,
                    "message": "No active account found with the given credentials",
                    "status_code": 401,
                    "errors": [
                        {
                            "status_code": 401,
                            "message": "No active account found with the given credentials"
                        }
                    ]
                })
        else:
            return Response({
                "code": status.HTTP_401_UNAUTHORIZED,
                "message": "No active account found with the given credentials",
                "status_code": 401,
                "errors": [
                    {
                        "status_code": 401,
                        "message": "Either Phone or Password or both not given"
                    }
                ]})
    except Exception as e:
        return Response({
            "code": status.HTTP_401_UNAUTHORIZED,
            "message": str(e),
            "status_code": 401,
            "errors": [
                {
                    "status_code": 401,
                    "message": str(e)
                }
            ]
        })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def tokenRefresh(request):
    try:

        refresh = RefreshToken(token=request.data.get('refresh_token'), verify=True)

        return Response({
            "code": status.HTTP_200_OK,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'token_type': str(refresh.payload['token_type']),
            'expiry': refresh.payload['exp'],
            'user_id': refresh.payload['user_id'],
            'user_object': UserInfoSerializer(User.objects.get(id=refresh.payload['user_id'])).data,

        })
    except Exception as e:
        return Response({
            "code": status.HTTP_401_UNAUTHORIZED,
            "message": str(e),
            "status_code": 401,
            "errors": [
                {
                    "status_code": 401,
                    "message": str(e)
                }
            ]
        })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def tokenVerify(request):
    try:

        verify = UntypedToken(token=request.data.get('access_token'))

        return Response({
            "code": status.HTTP_200_OK,
            'access_token': str(verify.token),
            'token_type': str(verify.payload['token_type']),
            'expiry': verify.payload['exp'],
            'user_id': verify.payload['user_id'],
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_401_UNAUTHORIZED,
            "message": str(e),
            "status_code": 401,
            "errors": [
                {
                    "status_code": 401,
                    "message": str(e)
                }
            ]
        })



@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def registration_view(request):
    if request.method == 'POST':
        print(request.data['gender'])
        serializer = RegistrationSerializers(data=request.data)

        account_data = {
            'gender': request.data['gender'],
            'phone_no': request.data['phone_no'],
            'address': request.data['address'],
            'city': request.data['city']
        }

        serializer2 = AccountSerializer(data=account_data)

        if serializer.is_valid() and serializer2.is_valid():
            user = serializer.save()
            account = serializer2.save(user=user)
            return Response({
                'code': status.HTTP_200_OK,
                'response': "successfully registered user",
                'email': user.email,
                'username': user.username,
                'gender': account.gender,
                'phone_no': account.phone_no,
                'address': account.address,
                'city': account.city
            })
        else:
            return Response({
                'code':status.HTTP_400_BAD_REQUEST,
                'message': "Error Occured",
                'error':serializer.errors
            })
                     

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def registration_view_admin(request):
    if request.method == 'POST':
        print(request.data['gender'])
        serializer = RegistrationSerializers(data=request.data)

        account_data = {
            'gender': request.data['gender'],
            'phone_no': request.data['phone_no'],
            'address': request.data['address'],
            'city': request.data['city']
        }

        serializer2 = AccountSerializer(data=account_data)

        if serializer.is_valid() and serializer2.is_valid():
            user = serializer.save()
            user.is_staff = True
            user.save()
            account = serializer2.save(user=user)
            return Response({
                'code': status.HTTP_200_OK,
                'response': "successfully registered user",
                'email': user.email,
                'username': user.username,
                'gender': account.gender,
                'phone_no': account.phone_no,
                'address': account.address,
                'city': account.city
            })
        else:
            return Response({
                'code':status.HTTP_400_BAD_REQUEST,
                'message': "Error Occured",
                'error':serializer.errors
            })


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def getUserList(request):
    try:
        user_list= User.objects.filter(~Q(is_staff=True))
        user_serializer= UserInfoSerializer(user_list, many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Data Successfully",
            "data": user_serializer.data
        })

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })
        
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
#@permission_required(['product.delete_category'], raise_exception=True)
def userDelete(request, user_id):
    try:
        User.objects.filter(id=user_id).delete()
        
        return Response({
            'code': status.HTTP_200_OK,
            'response': "User deleted successfully!",
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "User delete failed!",
            "error": str(e)
        })


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def getAdminList(request):
    try:
        admin_list= User.objects.filter(is_staff=True)
        user_serializer= UserInfoSerializer(admin_list, many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Data Successfully",
            "data": user_serializer.data
        })

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_classes([])
def getMyProfile(request):
    try:
        user = request.user
        
        user_serializer= UserInfoSerializer(user)
        
        return Response({
            'code': status.HTTP_200_OK,
            'response': "My Profile Data Received Successfully",
            "data": user_serializer.data
        })

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })
        
        
@api_view(['POST'])
@login_required
def changePassword(request):
    try:
        data = request.data
        serializer = ChangePasswordSerializer(data=data)

        if serializer.is_valid():
            print(serializer.data.get('old_password'))
            print(serializer.data.get('new_password1'))

            if not request.user.check_password(serializer.data.get('old_password')):
                return Response({
                    'response': ["Wrong password."],
                    'code': status.HTTP_400_BAD_REQUEST,
                    
                })

            request.user.set_password(serializer.data.get('new_password1'))
            
            request.user.save()
            return Response({
                "response": ["Password updated successfully."],
                'code': status.HTTP_200_OK,
                'data': serializer.data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })
        
        
@api_view(['GET'])
@login_required
# @permission_required['auth.view_employeeattendance'], raise_exception=True)
@permission_classes([IsAuthenticated]) 
def getUserInfo(request):
    try:
        user_instance =  request.user
        account_info = {}
        account_info_instance = Account.objects.filter(user_id=user_instance.id)
        account_info = AccountSerializer(account_info_instance, many=True).data

        return Response({
            "code": status.HTTP_200_OK,
            'response': "User Info Retrieved Successfully!",
            'user_object': UserInfoSerializer(user_instance).data,
            'additional_info': account_info,
        })

    except Exception as e:
        system_manager.views.log(request.path, e)
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Error in Data!",
            "error": str(e)

        })

@api_view(['POST'])
@login_required
# @permission_required['auth.change_group'], raise_exception=True)
def userInfoEdit(request):
    try:
        
        user = request.user
        
        serializer = UserInfoUpdateSerializer(user, data=request.data)

        account_data = {
            'gender': request.data['gender'],
            'phone_no': request.data['phone_no'],
            'address': request.data['address'],
            'city': request.data['city']
        }
        
        user_info_instance = Account.objects.get(user=user.id)
        
        user_info_serializer = AccountSerializer(user_info_instance, data=account_data, partial=True)
        
        if serializer.is_valid() and user_info_serializer.is_valid():
            
            user = serializer.save()
            account = user_info_serializer.save(user=user)
            
            return Response({
                'code': status.HTTP_200_OK,
                'response': "User Additional Info updated Successfully",
                "data": serializer.data,
                "addiotional data": user_info_serializer.data

            })
        else:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'response': "User Additional info update Failed",
                "error": str(user_info_serializer.errors)

            })

    except Exception as e:
        system_manager.views.log(request.path, e)
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "User update Failed",
            "error": str(e)

        })