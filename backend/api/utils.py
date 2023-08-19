from users.models import Subscription


def get_is_subscribed(obj, request):
    if request.user.is_anonymous:
        return False

    return Subscription.objects.filter(
        author=obj, subscriber=request.user
    ).exists()
