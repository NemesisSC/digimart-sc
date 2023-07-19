from django.urls import path, include

from .views import *
urlpatterns = [
    path('register', registration_view, name="register"),
    path('register/admin', registration_view_admin),
    path('token', tokenObtainPair),
    path('token/admin', tokenObtainPairAdmin),
    path('token/verify',tokenVerify),
    path('token/refresh', tokenRefresh),
    path('user/list', getUserList),
    path('delete/<int:user_id>', userDelete),
    path('admin/list', getAdminList),
    path('user/my-profile', getMyProfile),
    path('user-accounts/user-info', getUserInfo),
    path('user-accounts/edit', userInfoEdit),
    path('change-password', changePassword),

]
