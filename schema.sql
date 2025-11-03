CREATE TABLE IF NOT EXISTS media (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    type TEXT CHECK(type IN ('movie', 'anime', 'manga', 'tvshow', 'book')) NOT NULL,
    release_year YEAR,
    origin_lang TEXT(3), -- ISO language code
    status TEXT CHECK(status IN ('completed', 'ongoing')),
    comment TEXT

);

CREATE TABLE IF NOT EXISTS user_activity (
    id INTEGER PRIMARY KEY,
    media_id INTEGER REFERENCES media(id),
    rating INTEGER CHECK(rating IS NULL OR (rating > 0 AND rating < 6)),
    last_watch_date DATE,
    times_consumed INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS info_movie (
	media_id INTEGER PRIMARY KEY REFERENCES media(id),
	duration_min INTEGER,
	director TEXT,
	status TEXT CHECK (status IN ('series', 'single','universe'))
	);
	
CREATE TABLE IF NOT EXISTS info_manga (
	media_id INTEGER PRIMARY KEY REFERENCES media(id),
	volumes INTEGER,
	authors TEXT, -- list is made by comma separated elt : 'hi,hello,bonjour'
	adapted_anime_id JSON
	);
	
CREATE TABLE IF NOT EXISTS info_anime (
	media_id INTEGER PRIMARY KEY REFERENCES media(id),
	seasons INTEGER,
	ep_duration_min INTEGER,
	total_episodes INTEGER,
	status TEXT CHECK (status IN ('series', 'single','universe'))
	);	
	
CREATE TABLE IF NOT EXISTS info_tvshow (
	media_id INTEGER PRIMARY KEY REFERENCES media(id),
	seasons INTEGER,
	ep_duration_min INTEGER,
	total_episodes INTEGER
	);
	
CREATE TABLE IF NOT EXISTS info_book (
	media_id INTEGER PRIMARY KEY REFERENCES media(id),
	pages INTEGER,
	authors TEXT,
	status TEXT CHECK (status IN ('series', 'single','universe'))
	);
