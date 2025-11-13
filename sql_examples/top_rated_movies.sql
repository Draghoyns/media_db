SELECT m.id, m.title, u.rating
FROM info_movie m
JOIN user_activity u ON m.id = u.media_id
ORDER BY u.rating DESC
LIMIT 10;
