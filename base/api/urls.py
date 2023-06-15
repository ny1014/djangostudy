from django.urls import URLPattern, path
from .import views

urlpatterns = [

    path('', views.getRountes),
    path('rooms/',views.getRooms)
]