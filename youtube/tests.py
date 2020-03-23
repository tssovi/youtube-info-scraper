import json
from rest_framework import status
from django.test import TestCase, Client
from common.data_loader import data_loader


# initialize the APIClient app
client = Client()


class YoutubeVideosDetailsTest(TestCase):
    """ Test module for GET all key value API """

    def setUp(self):
        channel_keywords = ['jawed']
        flag = data_loader(channel_keywords)
        if flag:
            print("Data Loaded Successfully")

    def test_get_valid_key(self):
        # get API response for tags and performance
        response = client.get('/yutube-info/api/v1/videos/videos-details-data/?tags=zoo&performance=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get API response for tags
        response = client.get('/yutube-info/api/v1/videos/videos-details-data/?tags=zoo')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get API response for performance
        response = client.get('/yutube-info/api/v1/videos/videos-details-data/?performance=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_key(self):
        # get API response for tags and performance
        response = client.get('/yutube-info/api/v1/videos/videos-details-data/?tags=zookeeper&performance=11')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # get API response for tags
        response = client.get('/yutube-info/api/v1/videos/videos-details-data/?tags=zookeeper')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # get API response for performance
        response = client.get('/yutube-info/api/v1/videos/videos-details-data/?performance=11')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

