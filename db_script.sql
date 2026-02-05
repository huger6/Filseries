-- This script was never used to create the database
-- It's only meant to resemble what it looks like in a more readable way
-- Keep in mind we have to create the database manually before starting the application
-- To do so, use: CREATE DATABASE filseries;

CREATE TABLE `users` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) UNIQUE,
  `username` varchar(50) UNIQUE NOT NULL,
  `pass_hash` varchar(255) NOT NULL,
  `pfp` MEDIUMBLOB
  `created_at` timestamp default CURRENT_TIMESTAMP
  `updated_at` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
);

CREATE TABLE `notifications` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int,
  `type` varchar(50),
  `message` text,
  `target_url` varchar(255),
  `is_read` boolean DEFAULT false,
  `created_at` timestamp default CURRENT_TIMESTAMP
);

CREATE TABLE `user_series_progress` (
  `user_id` int,
  `api_serie_id` int,
  `last_season_seen` int DEFAULT 1,
  `status` varchar(255),
  `user_rating` float,
  `updated_at` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`, `api_serie_id`)
);

CREATE TABLE `user_movies_seen` (
  `user_id` int,
  `api_movie_id` int,
  `user_rating` float,
  `updated_at` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`, `api_movie_id`)
);

CREATE TABLE `user_movies_watchlist` (
  `user_id` int,
  `api_movie_id` int,
  `updated_at` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`, `api_movie_id`)
);

CREATE TABLE `user_series_watchlist` (
  `user_id` int,
  `api_serie_id` int,
  `updated_at` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`, `api_serie_id`)
);

ALTER TABLE `notifications` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

ALTER TABLE `user_series_progress` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

ALTER TABLE `user_movies_seen` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

ALTER TABLE `user_movies_watchlist` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

ALTER TABLE `user_series_watchlist` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;


-- Indexes

-- Movies seen: for pagination queries (ORDER BY updated_at DESC, api_movie_id DESC)
CREATE INDEX idx_user_movies_seen_pagination ON user_movies_seen (user_id, updated_at DESC, api_movie_id DESC);

-- Movies watchlist: for pagination queries
CREATE INDEX idx_user_movies_watchlist_pagination ON user_movies_watchlist (user_id, updated_at DESC, api_movie_id DESC);

-- Series progress: for pagination queries
CREATE INDEX idx_user_series_progress_pagination ON user_series_progress (user_id, updated_at DESC, api_serie_id DESC);

-- Series watchlist: for pagination queries
CREATE INDEX idx_user_series_watchlist_pagination ON user_series_watchlist (user_id, updated_at DESC, api_serie_id DESC);

-- Notifications: for fetching user notifications (unread first, by date)
CREATE INDEX idx_notifications_user_read_date ON notifications (user_id, is_read, created_at DESC);