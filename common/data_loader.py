from common.scraper import scrap_channel_info, scrap_video_ids, scrap_videos_details
from youtube.models import Channel, Videos

def data_loader(channel_keywords):
    flag = False
    if channel_keywords == []:
        channel_keywords = Channel.objects.all_channels_data()
        channel_keywords = list(map(lambda x: x['channel_id'], channel_keywords))

    channel_data = scrap_channel_info(channel_keywords)

    if channel_data:
        Channel.objects.process_channel_data(channel_data)
        channel_ids = list(map(lambda x: x['channel_id'], channel_data))
        video_ids = []

        for channel_id in channel_ids:
            video_id_list = scrap_video_ids(channel_id)
            video_ids.extend(video_id_list)

        if video_ids:
            videos_details = scrap_videos_details(video_ids)
            Videos.objects.process_videos_details_data(videos_details)
        flag = True

    return flag