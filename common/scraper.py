from common.scrap_channel_info import GetChannelInfo
from common.scrap_video_ids_by_chnid import GetVideoIds
from common.scrap_video_details_by_vdoid import GetVideosDetails


def scrap_channel_info(channel_keywords):
    scraper = GetChannelInfo()
    channel_data, logs, flag = scraper.get_channel_info(channel_keywords)
    if flag == "error":
        print("\nChannel Info Scraping Log(s):\n-----------------------------------\n{}".format("\n".join(logs)))
    else:
        if channel_data:
            print("\nChannel Info Scraping Log(s):\n-----------------------------------\n{}".format("\n".join(logs)))
            print("\nChannel Details Data:\n-----------------------------------\n{}".format(channel_data))
        else:
            print("\nChannel Info Scraping Log(s):\n-----------------------------------\n{}".format("\n".join(logs)))

    return channel_data


def scrap_video_ids(channel_id):
    scraper = GetVideoIds()
    video_ids, logs, flag = scraper.get_all_video_ids(channel_id)
    if flag == "error":
        print("\nVideo Id(s) Scraping Log(s):\n-----------------------------------\n{}".format("\n".join(logs)))
    else:
        if video_ids:
            print("\nVideo Id(s) Scraping Log(s):\n-----------------------------------\n{}".format("\n".join(logs)))
            print("\nScraped Video Id(s):\n-----------------------------------\n{}".format(video_ids))
        else:
            print("\nVideo Id(s) Scraping Log(s):\n-----------------------------------\n{}".format("\n".join(logs)))

    return video_ids


def scrap_videos_details(video_ids):
    scraper = GetVideosDetails()
    videos_details, logs, flag = scraper.get_all_videos_details(video_ids)
    if flag == "error":
        print("\nVideo(s) Details Scraping Log(s):\n-----------------------------------\n{}".format("\n".join(logs)))
    else:
        if videos_details:
            print("\nVideo(s) Details Scraping Log(s):\n-----------------------------------\n{}".format("\n".join(logs)))
            print("\nScraped Video(s) Details:\n-----------------------------------\n{}".format(videos_details))
        else:
            print("\nVideo(s) Details Scraping Log(s):\n-----------------------------------\n{}".format("\n".join(logs)))

    return videos_details

