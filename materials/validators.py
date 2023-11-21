import re
from rest_framework.serializers import ValidationError


class UrlsValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile(r"^((https?://)?(www.)?(youtube.com/watch[?]v=)[a-zA-Z0-9_-]+)")
        link = dict(value).get(self.field)
        if link is None:
            return None
        elif not bool(reg.search(link)):
            raise ValidationError('Видео может быть только с YouTube')
