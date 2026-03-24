import traceback
from django.shortcuts import get_object_or_404, redirect
from django.core.cache import cache
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import URL
from .serializers import URLSerializer
from .utils import generate_short_code
# Create your views here.

@api_view(['POST'])
def shorten_url(request):

    serializer = URLSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({"error": "URL not valid!"})

    original_url = serializer.validated_data["url"]

    while True:
        try:
            url, created = URL.objects.get_or_create(
                original_url=original_url,
                defaults={"short_code": generate_short_code()}
            )
            break

        except IntegrityError:
            continue

    return Response({
        "short_url": f"http://127.0.0.1:8000/{url.short_code}"
    })


def redirect_url(request, short_code):

    cached_url = cache.get(short_code)

    if cached_url:
        return redirect(cached_url)

    url = get_object_or_404(URL, short_code=short_code)
    cache.set(short_code, url.original_url, timeout=86400)
    url.click_count += 1
    url.save()
    return redirect(url.original_url)

@api_view(['GET'])
def stats(request, short_code):
    url = get_object_or_404(URL, short_code=short_code)

    return Response({
        "original_url": url.original_url,
        "clicks": url.click_count,
        "created_at": url.created_at
    })