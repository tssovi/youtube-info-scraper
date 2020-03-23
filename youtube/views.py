from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from youtube.models import Videos
from youtube.serializers import VideosSerializer
from common.status_code import *


class GetVideosDetailsData(APIView):
    def get(self, request, *args, **kwargs):
        tags = request.GET.get('tags')
        performance = request.GET.get('performance')
        if tags:
            tags = tags.split(',')

        try:
            if tags and performance:
                print('From Tags and Performance')
                videos_data = Videos.objects.get_videos_details_by_tags_and_performance(tags, performance)
            elif tags:
                print('From Tags')
                videos_data = Videos.objects.get_videos_details_by_tags(tags)
            else:
                print('From Performance')
                videos_data = Videos.objects.get_videos_details_by_performance(performance)

            videos_data_serializer = VideosSerializer(videos_data, many=True)
            data = videos_data_serializer.data

            if len(data) > 0:
                return Response(
                    {
                        'data': data,
                        'message': "Get Requested Videos Details",
                        'response_code': VIDEO_DETAILS_FOUND
                    }, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'data': data,
                        'message': "No Videos Details Found For Your Query",
                        'response_code': VIDEO_DETAILS_NOT_FOUND
                    }, status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            print(e)
            return Response({'error_code': INVALID_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

