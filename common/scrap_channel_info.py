import requests
import json
from youtube_scraper.settings import YOUTUBE_API_KEY


class GetChannelInfo():

    def __init__(self):
        # Credentials and Variables
        self.api_key = YOUTUBE_API_KEY
        self.youtube_base_api_url = "https://www.googleapis.com/youtube/v3/"
        self.youtube_channel_api_url = self.youtube_base_api_url + "channels?part=snippet,statistics&key={0}&"\
            .format(self.api_key)

        self.url_to_get_channel_info_for_name = self.youtube_channel_api_url + "forUsername={0}"
        self.url_to_get_channel_info_for_id = self.youtube_channel_api_url + "id={0}"

        self.channel_info = []
        self.logs = []

    def get_channel_info(self, channel_keywords):
        for channel_keyword in channel_keywords:
            channel_data = {}

            url_for_channel_name = self.url_to_get_channel_info_for_name.format(channel_keyword)
            url_for_channel_id = self.url_to_get_channel_info_for_id.format(channel_keyword)

            response = requests.get(url_for_channel_name).json()

            message = "Searching channel details for channel id or name: {}.".format(channel_keyword)
            self.logs.append(message)

            try:
                check_errors = response["error"]["errors"]

                if check_errors:
                    error_domain = check_errors[0]["domain"]
                    error_reason = check_errors[0]["reason"]
                    error_message = check_errors[0]["message"]

                    flag = "error"
                    self.logs.extend([error_domain, error_reason, error_message])

            except:
                try:
                    if response["pageInfo"]["totalResults"] < 1:
                        response = requests.get(url_for_channel_id).json()

                    if response["pageInfo"]["totalResults"] > 0 and response["pageInfo"]["totalResults"] == 1:
                        channel_req_res = response["items"][0]
                        channel_data['channel_id'] = channel_req_res["id"]
                        channel_data['channel_title'] = channel_req_res["snippet"]["title"]
                        channel_data['channel_description'] = channel_req_res["snippet"]["description"]
                        channel_data['channel_started_at'] = channel_req_res["snippet"]["publishedAt"]
                        channel_data['videos_count'] = channel_req_res["statistics"]["videoCount"]
                        channel_data['views_count'] = channel_req_res["statistics"]["viewCount"]
                        channel_data['subscribers_count'] = channel_req_res["statistics"]["subscriberCount"]

                        self.channel_info.append(channel_data)
                        message = "Found expected channel details for channel id or name: {}".format(channel_keyword)
                        self.logs.append(message)

                    elif response["pageInfo"]["totalResults"] > 1:
                        message = "Multiple channel id were received in the response."
                        self.logs.append(message)

                    else:
                        message = "Response received but it contains no item."
                        self.logs.append(message)
                        message = "The channel id could not be retrieved. " \
                                  "Please make sure that the channel name or id is correct."
                        self.logs.append(message)

                except Exception:
                    message = "An exception occurred while trying to retrieve the channel id."
                    self.logs.append(message)

                flag = "success"

        return self.channel_info, self.logs, flag