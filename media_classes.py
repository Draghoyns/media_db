from dataclasses import dataclass


@dataclass
class QuickMedia:
    title: str
    type: str  # movie, anime, manga, tvshow, book
    release_year: int
    status: str  # completed, ongoing


@dataclass
class Media(QuickMedia):
    language: str | None = None  # ISO language code (3 letters)
    seen: bool = False
    rating: int | None = None
    last_watch_date: str | None = None
    times_consumed: int = 0
    comment: str = ""

    def __init__(self, **kwargs):
        for field in self.__dataclass_fields__:
            setattr(self, field, kwargs.get(field))


@dataclass
class Movie(Media):
    duration: int = 100
    director: list[str] | None = None
    belonging: str = "single"


@dataclass
class Manga(Media):
    volumes: int = 0
    authors: list[str] | None = None
    adapted_to_anime: bool = False


@dataclass
class Book(Media):
    pages: int = 0
    authors: list[str] | None = None
    belonging: str = "single"


@dataclass
class TVshow(Media):
    ep_duration_min: int = 30
    seasons: int | None = None
    total_episodes: int | None = None


@dataclass
class Anime(TVshow):
    ep_duration_min: int = 24
    belonging: str = "single"


def create_media_instance(
    media_type: str, **kwargs
) -> Movie | Anime | Manga | TVshow | Book:
    """
    Create an instance of a media class based on the media type.

    Parameters:
    - media_type (str): The type of media ('movie', 'anime', 'manga', 'tvshow', 'book').
    - kwargs: The attributes required to instantiate the media class.

    Returns:
    - An instance of the corresponding media class.
    """
    media_classes = {
        "movie": Movie,
        "anime": Anime,
        "manga": Manga,
        "tvshow": TVshow,
        "book": Book,
    }

    media_class = media_classes.get(media_type.lower().strip())
    if not media_class:
        raise ValueError(f"Unsupported media type: '{media_type}'")

    return media_class(**kwargs)
