from django.utils.timezone import make_aware

from .models import Video
import logging
import datetime

# Get an instance of a logger
logger = logging.getLogger(__name__)


def add_video_data(vid, data=None):
    timestamp = datetime.datetime.strptime(data['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
    timestamp = make_aware(timestamp)
    try:
        video = Video.objects.create(
            id=vid,
            title=data['title'],
            description=data['description'],
            channelTitle=data['channelTitle'],
            publishedAt=timestamp
        )

    except Exception as e:
        logger.error("unable to add video {}".format(e))
        return None

    return video


def serialize_data_and_insert(videoRaw):
    count = 0
    for item in videoRaw:
        video = add_video_data(item['id']['videoId'], item['snippet'])
        if video is not None:
            count = count + 1
    return count
