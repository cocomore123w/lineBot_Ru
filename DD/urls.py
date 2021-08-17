from django.urls import path
from DD import views

from django.conf.urls.static import static
from django.conf import settings
##呼叫函數
urlpatterns = [
    path('callback/', views.callback)
]
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)