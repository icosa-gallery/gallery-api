from api.models import PUBLIC, Asset

from django.shortcuts import render


def home(request):
    template = "home.html"

    context = {
        "assets": Asset.objects.filter(visibility=PUBLIC).order_by("-id"),
        "hero": Asset.objects.filter(visibility=PUBLIC, curated=True)
        .order_by("?")
        .first(),
    }
    return render(
        request,
        template,
        context,
    )