from datetime import datetime, timedelta

from django.conf import settings
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from Youtube.celery import app
from .models import Video
import logging

from .utils import serialize_data_and_insert

logger = logging.getLogger(__name__)


@app.task
def fetch_data():

    timestamp = datetime.now() - timedelta(minutes=10)

    try:
        timestamp = Video.objects.latest('publishedAt').publishedAt
    except Video.DoesNotExist:
        logger.error(f"Using default timestamp {timestamp}")
    key_number = 0
    timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')

    is_data_fetched = False
    total_api_call_fails = 0
    response = {'items': []}

    while not is_data_fetched:
        is_data_fetched = True
        try:
            service = build(
                'youtube',
                'v3',
                developerKey=settings.YOUTUBE_API_KEY[key_number],
                cache_discovery=False
            )
            collection = service.search().list(
                maxResults=20,
                part=['id', 'snippet'],
                q='football',
                type='video',
                order='date',
                publishedAfter=timestamp
            )

            response = collection.execute()
        except HttpError as e:
            logger.error(f"error while fetching video {e}")
            key_number = key_number + 1
            total_api_call_fails = total_api_call_fails + 1

            key_number = key_number % len(settings.YOUTUBE_API_KEY)
            is_data_fetched = False

            # If all the keys used break loop
        if total_api_call_fails == len(settings.YOUTUBE_API_KEY):
            logger.error("all keys exhausted")
            break

    if len(response['items']) > 0:
        count = serialize_data_and_insert(response['items'])
        logger.info(f" inserted {count} rows")

    return False
