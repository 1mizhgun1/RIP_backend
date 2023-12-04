from .models import *
import redis
from BACKEND.settings import REDIS_HOST, REDIS_PORT


session_storage = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)


def get_session(request):
    ssid = request.COOKIES.get("session_id")
    if ssid is None:
        ssid = request.headers.get("authorization")
    return ssid


def getOrderID(request):
    session_id = get_session(request)
    if session_id is None:
        return -1

    username = session_storage.get(session_id)
    if username is None:
        return -1

    user = User.objects.get(username=session_storage.get(session_id).decode('utf-8'))
    orders = OpticOrder.objects.filter(user=user).filter(status='I')
    if orders.exists():
        return orders.first().pk
    return -1


def getCartID(user: User):
    orders = OpticOrder.objects.filter(user=user).filter(status='I')
    if orders.exists():
        return orders.first().pk
    return -1