from django.core.management.base import BaseCommand
from common.data_loader import data_loader


class Command(BaseCommand):
    help = 'Scrap and Seed Data From Youtube API'

    def handle(self, *args, **kwargs):
        print("Input Example: aaaaaaaaa,bbbbbbbbb,ccccccccc")
        channel_keywords = input("Provide your desire one or more YouTube channel names or ids separated by comma(,): ")
        channel_keywords = channel_keywords.split(',')
        flag = data_loader(channel_keywords)
        if flag:
            print("Data Loaded Successfully")


