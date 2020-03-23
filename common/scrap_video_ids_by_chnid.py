import requests
import json
from youtube_scraper.settings import YOUTUBE_API_KEY


class GetVideoIds():

    def __init__(self):
        # Credentials and Variables
        self.api_key = YOUTUBE_API_KEY
        self.youtube_base_api_url = "https://www.googleapis.com/youtube/v3/"
        self.youtube_search_api_url = self.youtube_base_api_url + "search?key={0}&part=id&order=date&type=video" \
                                                                  "&maxResults=50&".format(self.api_key)

        self.url_to_get_video_ids = self.youtube_search_api_url + "channelId={0}&pageToken={1}"

        self.video_ids = []
        self.logs = []


    def get_all_video_ids(self, channel_id):
        next_page_token = ""
        flag = ""

        url = self.url_to_get_video_ids.format(channel_id, next_page_token)

        response = requests.get(url).json()

        try:
            check_errors = response["error"]["errors"]

            if check_errors:
                error_domain = check_errors[0]["domain"]
                error_reason = check_errors[0]["reason"]
                error_message = check_errors[0]["message"]

                flag = "error"
                self.logs.extend([error_domain, error_reason, error_message])

                return self.video_ids, self.logs, flag

        except:
            message = "Searching video id(s) for channel id: {0}.".format(channel_id)
            self.logs.append(message)
            while True:
                response = requests.get(url).json()
                items = response["items"]

                for item in items:
                    if item["id"]["kind"] == "youtube#video":
                        video_id = item["id"]["videoId"]
                        self.video_ids.append(video_id)

                try:
                    next_page_token = response["nextPageToken"]
                    url = self.url_to_get_video_ids.format(channel_id, next_page_token)
                except:
                    if len(self.video_ids) > 0:
                        message = "All possible video id(s) are acquired."
                        self.logs.append(message)
                    else:
                        message = "Either no video for this {} channel is uploaded or provided an invalid channel id."\
                                  .format(channel_id)
                        self.logs.append(message)
                    break
            # Get and return only unique video id(s)
            video_ids_set = set(self.video_ids)
            self.video_ids = list(video_ids_set)
            flag = "success"
            return self.video_ids, self.logs, flag