-- Inserting Artists (3rd & 4th Gen K-pop)
INSERT INTO Artists (artist_id, name, account_id, created_at, updated_at) VALUES
(1, 'Stray Kids', NULL, NOW(), NOW()),
(2, 'ATEEZ', NULL, NOW(), NOW()),
(3, 'ITZY', NULL, NOW(), NOW()),
(4, 'TXT', NULL, NOW(), NOW()),
(5, 'BLACKPINK', NULL, NOW(), NOW()),
(6, 'TWICE', NULL, NOW(), NOW()),
(7, 'NCT 127', NULL, NOW(), NOW()),
(8, 'ENHYPEN', NULL, NOW(), NOW()),
(9, 'TREASURE', NULL, NOW(), NOW());

-- Inserting Albums with at least 3 songs per album
INSERT INTO Albums (id, title, artist_id, released_at, created_at, updated_at) VALUES
(1, 'Go Live', 1, '2020-06-17', NOW(), NOW()),
(2, 'All In', 1, '2020-11-04', NOW(), NOW()),
(3, 'ZERO: FEVER Part.2', 2, '2021-03-01', NOW(), NOW()),
(4, 'Guess Who', 3, '2021-04-30', NOW(), NOW()),
(5, 'The Chaos Chapter: Freeze', 4, '2021-05-31', NOW(), NOW()),
(6, 'THE ALBUM', 5, '2020-10-02', NOW(), NOW()),
(7, 'Formula of Love: O+T=<3', 6, '2021-11-12', NOW(), NOW()),
(8, 'Sticker', 7, '2021-09-17', NOW(), NOW()),
(9, 'DIMENSION : DILEMMA', 8, '2021-10-12', NOW(), NOW()),
(10, 'THE FIRST STEP: TREASURE EFFECT', 9, '2021-01-11', NOW(), NOW());

-- Inserting Songs (linked to Albums and Artists)
INSERT INTO Songs (id, title, artist_id, album_id, genre, duration, released_at, created_at, updated_at) VALUES
(1, 'God\'s Menu', 1, 1, 'Hip-hop', 3.0, '2020-06-17', NOW(), NOW()),
(2, 'Easy', 1, 1, 'Hip-hop', 2.58, '2020-06-17', NOW(), NOW()),
(3, 'Blueprint', 1, 1, 'Pop', 3.16, '2020-06-17', NOW(), NOW()),
(4, 'All In', 1, 2, 'Hip-hop', 3.1, '2020-11-04', NOW(), NOW()),
(5, 'FAM', 1, 2, 'Hip-hop', 2.9, '2020-11-04', NOW(), NOW()),
(6, 'One Day', 1, 2, 'Ballad', 3.3, '2020-11-04', NOW(), NOW()),

(7, 'Fireworks (I\'m the One)', 2, 3, 'Hip-hop', 3.12, '2021-03-01', NOW(), NOW()),
(8, 'Celebrate', 2, 3, 'Pop', 3.25, '2021-03-01', NOW(), NOW()),
(9, 'Take Me Home', 2, 3, 'Pop', 3.22, '2021-03-01', NOW(), NOW()),

(10, 'Mafia in the Morning', 3, 4, 'Hip-hop', 3.2, '2021-04-30', NOW(), NOW()),
(11, 'Sorry Not Sorry', 3, 4, 'Pop', 2.58, '2021-04-30', NOW(), NOW()),
(12, 'Kidding Me', 3, 4, 'Pop', 3.18, '2021-04-30', NOW(), NOW()),

(13, '0X1=LOVESONG', 4, 5, 'Rock', 3.5, '2021-05-31', NOW(), NOW()),
(14, 'Magic', 4, 5, 'Pop', 3.4, '2021-05-31', NOW(), NOW()),
(15, 'Frost', 4, 5, 'Pop', 3.1, '2021-05-31', NOW(), NOW()),

(16, 'How You Like That', 5, 6, 'Hip-hop', 3.1, '2020-10-02', NOW(), NOW()),
(17, 'Lovesick Girls', 5, 6, 'Pop', 3.2, '2020-10-02', NOW(), NOW()),
(18, 'Pretty Savage', 5, 6, 'Hip-hop', 3.2, '2020-10-02', NOW(), NOW()),

(19, 'SCIENTIST', 6, 7, 'Pop', 3.0, '2021-11-12', NOW(), NOW()),
(20, 'ICON', 6, 7, 'Pop', 3.18, '2021-11-12', NOW(), NOW()),
(21, 'MOONLIGHT', 6, 7, 'Pop', 3.05, '2021-11-12', NOW(), NOW()),

(22, 'Sticker', 7, 8, 'Hip-hop', 3.5, '2021-09-17', NOW(), NOW()),
(23, 'Lemonade', 7, 8, 'Pop', 3.1, '2021-09-17', NOW(), NOW()),
(24, 'Magic Carpet Ride', 7, 8, 'Pop', 3.3, '2021-09-17', NOW(), NOW()),

(25, 'Tamed-Dashed', 8, 9, 'Pop', 3.3, '2021-10-12', NOW(), NOW()),
(26, 'Upper Side Dreamin\'', 8, 9, 'Pop', 3.2, '2021-10-12', NOW(), NOW()),
(27, 'Just A Little Bit', 8, 9, 'Pop', 3.12, '2021-10-12', NOW(), NOW()),

(28, 'MY TREASURE', 9, 10, 'Pop', 3.18, '2021-01-11', NOW(), NOW()),
(29, 'GOING CRAZY', 9, 10, 'Pop', 3.08, '2021-01-11', NOW(), NOW()),
(30, 'SLOWMOTION', 9, 10, 'Pop', 3.25, '2021-01-11', NOW(), NOW());
