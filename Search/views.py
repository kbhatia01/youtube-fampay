from django.db.models import Q
from rest_framework import generics
from .models import Video
from .serializers import VideoSerializer
from .constants import DEFAULT_VALUE_FOR_SORT, SORT_VALUES
from rest_framework.pagination import CursorPagination


class YoutubeVideoView(generics.ListAPIView):
    CursorPagination.ordering = DEFAULT_VALUE_FOR_SORT
    serializer_class = VideoSerializer
    pagination_class = CursorPagination

    def get_queryset(self):
        search_filter = Q()
        if 'search' in self.request.GET:
            query = self.request.GET.get('search')
            search_filter |= Q(title__icontains=query)
            search_filter |= Q(description__icontains=query)
        videos = Video.objects.filter(search_filter)
        if 'sort_by' in self.request.GET:

            sort_by = self.request.GET.get('sort_by')

            if sort_by in SORT_VALUES:
                CursorPagination.ordering = sort_by
                return videos

        return videos
