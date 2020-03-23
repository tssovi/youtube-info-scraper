import requests
import json
from youtube_scraper.settings import YOUTUBE_API_KEY


class GetVideosDetails():

    def __init__(self):
        # Credentials and Variables
        self.api_key = YOUTUBE_API_KEY
        self.youtube_base_api_url = "https://www.googleapis.com/youtube/v3/"
        self.youtube_video_api_url = self.youtube_base_api_url + "videos?part=snippet,contentDetails,statistics" \
                                                                 "&key={0}&".format(self.api_key)

        self.url_to_get_video_details_for_id = self.youtube_video_api_url + "id={0}"

        self.videos_details = []
        self.logs = []

    def get_all_videos_details(self, video_ids):
        for video_id in video_ids:
            video_data = {}

            url_for_video_details = self.url_to_get_video_details_for_id.format(video_id)

            response = requests.get(url_for_video_details).json()

            message = "Searching video details for video id: {}.".format(video_id)
            self.logs.append(message)

            try:
                check_errors = response["error"]["errors"]

                if check_errors:
                    error_domain = check_errors[0]["domain"]
                    error_reason = check_errors[0]["reason"]
                    error_message = check_errors[0]["message"]

                    flag = "error"
                    self.logs.extend([error_domain, error_reason, error_message])

                    return self.videos_details, self.logs, flag

            except:
                try:
                    if response["pageInfo"]["totalResults"] > 0 and response["pageInfo"]["totalResults"] == 1:
                        video_details_res = response["items"][0]
                        video_data['channel_id'] = video_details_res["snippet"]["channelId"]
                        video_data['video_id'] = video_details_res["id"]
                        video_data['video_title'] = video_details_res["snippet"]["title"]
                        video_data['video_description'] = video_details_res["snippet"]["description"]
                        video_data['video_published_at'] = video_details_res["snippet"]["publishedAt"]
                        video_data['video_duration'] = video_details_res["contentDetails"]["duration"]
                        video_data['views_count'] = video_details_res["statistics"]["viewCount"]
                        video_data['likes_count'] = video_details_res["statistics"]["likeCount"]
                        video_data['dislikes_count'] = video_details_res["statistics"]["dislikeCount"]
                        video_data['comment_count'] = video_details_res["statistics"]["commentCount"]

                        try:
                            tags = video_details_res["snippet"]["tags"]
                            tags = list(map(lambda x:x.lower(), tags))
                            video_data['video_tags'] = tags
                        except:
                            video_data['video_tags'] = []

                        self.videos_details.append(video_data)
                        message = "Found expected video details for video id: {}".format(video_id)
                        self.logs.append(message)

                    elif response["pageInfo"]["totalResults"] > 1:
                        message = "Multiple channel id were received in the response."
                        self.logs.append(message)

                    else:
                        message = "Response received but it contains no item."
                        self.logs.append(message)
                        message = "The video details could not be retrieved. " \
                                  "Please make sure that the video id is correct."
                        self.logs.append(message)

                except Exception:
                    message = "An exception occurred while trying to retrieve the channel id."
                    self.logs.append(message)

                flag = "success"

        return self.videos_details, self.logs, flag