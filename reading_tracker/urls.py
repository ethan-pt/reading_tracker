from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import ReaderLogin, ReaderRegister, ReaderCreate, ReaderList, ReaderUpdate, ReaderDelete



urlpatterns = [
    path('', ReaderList.as_view(), name='reader'),
    path('login/', ReaderLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', ReaderRegister.as_view(), name='register'),
    path('book-create/', ReaderCreate.as_view(), name='book-create'),
    path('book-update/<int:pk>/', ReaderUpdate.as_view(), name='book-update'),
    path('book-delete/<int:pk>/', ReaderDelete.as_view(), name='book-delete'),
]