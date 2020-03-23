import logging
import operator
from functools import reduce

from django.db import models
from django.db.models import Q
from django.utils import timezone
from datetime import datetime

class ChannelManager(models.Manager):
    # Process youtube channel details data to save it in the related databases
    def process_channel_data(self, channel_details_data):
        for channel_data in channel_details_data:
            try:
                # request to insert youtube channel data
                channel_id = channel_data['channel_id']
                channel_title = channel_data['channel_title']
                channel_description = channel_data['channel_description']
                channel_started_at = channel_data['channel_started_at']
                videos_count = channel_data['videos_count']
                views_count = channel_data['views_count']
                subscribers_count = channel_data['subscribers_count']

                channel_details_data = {
                    'channel_id': channel_id,
                    'channel_title': channel_title,
                    'channel_description': channel_description,
                    'channel_started_at': channel_started_at,
                    'videos_count': videos_count,
                    'views_count': views_count,
                    'subscribers_count': subscribers_count,
                }

                try:
                    self.update_channel_data(channel_data=channel_details_data)
                except Channel.DoesNotExist:
                    self.insert_channel_data(channel_data=channel_details_data)

            except Exception as e:
                logging.error(e)

    # insert into database
    def insert_channel_data(self, channel_data):
        self.create(
            channel_id=channel_data['channel_id'],
            channel_title = channel_data['channel_title'],
            channel_description = channel_data['channel_description'],
            channel_started_at = channel_data['channel_started_at'],
            videos_count = channel_data['videos_count'],
            views_count = channel_data['views_count'],
            subscribers_count = channel_data['subscribers_count'],
        )

    def update_channel_data(self, channel_data):
        channel_details_obj = Channel.objects.get(channel_id=channel_data['channel_id'])

        channel_details_obj.channel_title = channel_data['channel_title']
        channel_details_obj.channel_description = channel_data['channel_description']
        channel_details_obj.videos_count = channel_data['videos_count']
        channel_details_obj.views_count = channel_data['views_count']
        channel_details_obj.subscribers_count = channel_data['subscribers_count']

        channel_details_obj.save()

    # get all channel data
    def all_channels_data(self):
        channel_ids = self.order_by('-updated_at').values('channel_id').all()
        # print(channel_ids)
        return channel_ids

    # get channel details by ID
    def get_channel_data_by_id(self, channel_id):
        return self.filter(channel_id=channel_id)

    # get channel details by ID
    def get_channel_views_median(self, channel_id):
        channel_data = self.get(channel_id=channel_id)
        channel_videos_count = float(channel_data.videos_count)
        channel_views_count = float(channel_data.views_count)
        channel_views_median = channel_views_count / channel_videos_count
        channel_views_median = round(channel_views_median, 2)

        return channel_views_median


class Channel(models.Model):
    channel_id = models.CharField(max_length=250, primary_key=True, db_index=True)
    channel_title = models.CharField(max_length=350)
    channel_description = models.TextField()
    channel_started_at = models.DateTimeField()
    videos_count = models.IntegerField()
    views_count = models.BigIntegerField()
    subscribers_count = models.BigIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ChannelManager()

    def __str__(self):
        return "Youtube channel details data inserted on {date}".format(
            date=datetime.strftime(self.created_at, "%B %d,%Y")
        )


class VideosManager(models.Manager):
    # Process youtube channel details data to save it in the related databases
    def process_videos_details_data(self, videos_details_data):
        channel_info = {}
        for video_data in videos_details_data:
            try:
                # process video details data
                channel_id = video_data['channel_id']
                video_id = video_data['video_id']
                video_title = video_data['video_title']
                video_description = video_data['video_description']
                video_tags = video_data['video_tags']
                video_published_at = video_data['video_published_at']
                video_duration = video_data['video_duration']
                views_count = video_data['views_count']
                likes_count = video_data['likes_count']
                dislikes_count = video_data['dislikes_count']
                comment_count = video_data['comment_count']

                video_tags = ", ".join(video_tags)
                video_duration = video_duration.replace('PT', '').replace('H', ' Hours ').replace('M', ' Minutes ')\
                                 .replace('S', ' Seconds ')
                video_url = "https://www.youtube.com/watch?v={}".format(video_id)

                if channel_id not in channel_info:
                    channel_views_median = Channel.objects.get_channel_views_median(channel_id)
                    channel_info.update({channel_id: {'channel_views_median': channel_views_median}})

                channel_views_median = float(channel_info[channel_id]['channel_views_median'])

                video_performance = float(views_count) / channel_views_median
                video_performance = round(video_performance, 2)

                video_details_data = {
                    'channel_id': channel_id,
                    'video_id': video_id,
                    'video_title': video_title,
                    'video_description': video_description,
                    'video_tags': video_tags,
                    'video_published_at': video_published_at,
                    'video_duration': video_duration,
                    'video_url': video_url,
                    'views_count': views_count,
                    'likes_count': likes_count,
                    'dislikes_count': dislikes_count,
                    'comment_count': comment_count,
                    'video_performance': video_performance,
                }
                try:
                    self.update_video_details_data(video_details_data=video_details_data)
                except Videos.DoesNotExist:
                    self.insert_video_details_data(video_details_data=video_details_data)

            except Exception as e:
                print('video_id:', video_id)
                logging.error(e)

    # insert into database
    def insert_video_details_data(self, video_details_data):
        self.create(
            channel=Channel.objects.get(channel_id=video_details_data['channel_id']),
            video_id=video_details_data['video_id'],
            video_title=video_details_data['video_title'],
            video_description=video_details_data['video_description'],
            video_tags=video_details_data['video_tags'],
            video_published_at=video_details_data['video_published_at'],
            video_duration=video_details_data['video_duration'],
            video_url=video_details_data['video_url'],
            views_count=video_details_data['views_count'],
            likes_count=video_details_data['likes_count'],
            dislikes_count=video_details_data['dislikes_count'],
            comment_count=video_details_data['comment_count'],
            video_performance=video_details_data['video_performance'],
        )

    def update_video_details_data(self, video_details_data):
        video_details_obj = Videos.objects.get(video_id=video_details_data['video_id'])

        video_details_obj.video_title = video_details_data['video_title']
        video_details_obj.video_description = video_details_data['video_description']
        video_details_obj.video_tags = video_details_data['video_tags']
        video_details_obj.video_duration = video_details_data['video_duration']
        video_details_obj.video_url = video_details_data['video_url']
        video_details_obj.views_count = video_details_data['views_count']
        video_details_obj.likes_count = video_details_data['likes_count']
        video_details_obj.dislikes_count = video_details_data['dislikes_count']
        video_details_obj.comment_count = video_details_data['comment_count']
        video_details_obj.video_performance = video_details_data['video_performance']

        video_details_obj.save()

    # get all videos data
    def all_video_details_data(self):
        all_videos_data = self.order_by('-updated_at').all()
        return all_videos_data

    # get filtered videos details by tags
    def get_videos_details_by_tags(self, tags):
        tags_filter = reduce(operator.and_, (Q(video_tags__contains=tag) for tag in tags))
        filte_videos = self.filter(tags_filter)
        return filte_videos

    # get filtered videos details by performance
    def get_videos_details_by_performance(self, performance):
        filte_videos = self.filter(video_performance__gte=performance, video_performance__lte=performance)
        return filte_videos

    # get filtered videos details tags and performance
    def get_videos_details_by_tags_and_performance(self, tags, performance):
        tags_filter = reduce(operator.and_, (Q(video_tags__contains = tag) for tag in tags))
        filte_videos = self.filter(tags_filter, video_performance__gte=performance, video_performance__lte=performance)
        return filte_videos

    # get video details by ID
    def get_video_details_data_by_id(self, video_id):
        return self.filter(id=video_id)

    # get all unique channel ids
    # def get_unique_channel_id(self):
    #     channel_ids = self.order_by().values('channel__channel_id').distinct()
    #     print(channel_ids)
    #     return channel_ids


class Videos(models.Model):
    video_id = models.CharField(max_length=250, primary_key=True, db_index=True)
    video_title = models.CharField(max_length=350)
    video_description = models.TextField()
    video_tags = models.TextField()
    video_published_at = models.DateTimeField()
    video_duration = models.CharField(max_length=250)
    video_url = models.CharField(max_length=250)
    views_count = models.BigIntegerField()
    likes_count = models.BigIntegerField()
    dislikes_count = models.BigIntegerField()
    comment_count = models.BigIntegerField()
    video_performance = models.DecimalField(max_digits=10, decimal_places=2)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = VideosManager()

    def __str__(self):
        return "Youtube video details data inserted on {date}".format(
            date=datetime.strftime(self.created_at, "%B %d,%Y")
        )

