-- SELECT * FROM  tournament_matches;
INSERT INTO tournament_matches (ID,team_name, matches_played)
VALUES
    (1,'PAK', 5),
    (2,'IND', 6),
    (3,'AUS', 4),
    (4,'ENG', 5),
    (5,'NZ', 4);
-- CREATE TABLE match_details (
--     match_id INT PRIMARY KEY,
--     team_a VARCHAR(50),
--     team_b VARCHAR(50),
--     total_runs_scored INT,
--     total_wickets_taken INT,
--     match_result VARCHAR(20)
-- );
INSERT INTO match_details (match_id, team_a, team_b, total_runs_scored, total_wickets_taken, match_result)
VALUES
    (1, 'PAK', 'IND', 300, 5, 'Team A won'),
    (2, 'AUS', 'ENG', 250, 7, 'Team B won'),
    (3, 'NZ', 'ENG', 320, 4, 'Team A won'),
	(4, 'IND', 'ENG', 280, 6, 'Team A won'),
    (5, 'AUS', 'PAK', 270, 5, 'Team B won'),
    (6, 'NZ', 'PAK', 310, 3, 'Team A won');
-- CREATE TABLE team_scoreboard (
--     team_name VARCHAR(50) PRIMARY KEY,
--     total_games_played INT,
--     total_runs_scored INT,
--     average_run_rate DECIMAL(10, 2)
-- );
-- Insert sample data into the team_scoreboard table
-- INSERT INTO team_scoreboard (team_name, total_games_played, total_runs_scored, average_run_rate)
-- VALUES
--     ('PAK', 5, 1200, 6.78),
--     ('IND', 6, 1500, 7.89),
--     ('AUS', 4, 1000, 6.25),
--     ('ENG', 5, 1300, 7.00),
--     ('NZ', 4, 950, 6.12);

INSERT INTO team_scoreboard (team_name, total_games_played)
SELECT tm.team_name, COUNT(*) as total_games_played
FROM tournament_matches tm
GROUP BY tm.team_name
ON DUPLICATE KEY UPDATE
    total_games_played = total_games_played + VALUES(total_games_played);


