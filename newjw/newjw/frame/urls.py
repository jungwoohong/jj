from django.urls import path

from newjw.frame.views import frameViewReg

urlpatterns = [
    path('reg/', frameViewReg.as_view() ),
]