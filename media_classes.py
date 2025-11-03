from dataclasses import dataclass


@dataclass
class Media:
    title: str
    release_year: int
    comment: str
    language: str  # ISO language code (3 letters)
    status: str  # completed, ongoing
    type: str  # movie, anime, manga, tvshow, book
    seen: bool
    rating: int | None
    rating: int | None
    last_watch_date: str | None
    times_consumed: int | None

    def __init__(self, **kwargs):
        for field in self.__dataclass_fields__:
            setattr(self, field, kwargs.get(field))


@dataclass
class Movie(Media):
    duration: int
    director: list[str]
    belonging: str  # 'series', 'single','universe'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.director = kwargs.get("authors", [])
        self.belonging = kwargs.get("belonging", "")
        self.duration = kwargs.get("duration", 0)


@dataclass
class Manga(Media):
    volumes: int
    adapted_to_anime: bool
    authors: list[str]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.authors = kwargs.get("authors", [])
        self.volumes = kwargs.get("volumes", 0)
        self.adapted_to_anime = kwargs.get("adapted_to_anime", False)


@dataclass
class TVshow(Media):
    total_episodes: int
    seasons: int
    ep_duration_min: int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total_episodes = kwargs.get("total_episodes", 0)
        self.seasons = kwargs.get("seasons", 0)
        self.ep_duration_min = kwargs.get("ep_duration_min", 0)


@dataclass
class Anime(TVshow):
    belonging: str  # 'series', 'single','universe'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.belonging = kwargs.get("belonging", "")


@dataclass
class Book(Media):
    pages: int
    belonging: str  # 'series', 'single','universe'
    authors: list[str]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.authors = kwargs.get("authors", [])
        self.pages = kwargs.get("pages", 0)
        self.belonging = kwargs.get("belonging", "")


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
