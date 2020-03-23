from django.urls import path
from youtube.views import *


urlpatterns = [
    path('videos-details-data/', GetVideosDetailsData.as_view(), name='videos-details-data'),
]