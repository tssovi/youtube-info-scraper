from rest_framework import serializers
from youtube.models import Videos


class VideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        exclude = ('created_at', 'updated_at')
