
from . import chatfiltr
from loader import dp
from .chatfiltr import IsGroup


if __name__ == "filters":
    dp.filters_factory.bind(IsGroup)

