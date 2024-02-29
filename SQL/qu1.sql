
-- USE cricket
-- --------------------------x---------------------------
-- INSERT INTO match_details (match_id, team_a, team_b, total_run_score, total_wickets_taken, match_result)
-- VALUES
--     (1, 'PAK', 'IND', 300, 5, 'Team A won'),
--     (2, 'AUS', 'ENG', 250, 7, 'Team B won'),
--     (3, 'NZ', 'ENG', 320, 4, 'Team A won'),
-- 	(4, 'IND', 'ENG', 280, 6, 'Team A won'),
--     (5, 'AUS', 'PAK', 270, 5, 'Team B won'),
--     (6, 'NZ', 'PAK', 310, 3, 'Team A won');
-- ALTER TABLE match_details
-- ADD COLUMN match_id INT PRIMARY KEY;
-- CREATE UNIQUE INDEX idx_team_name ON tournament_matches (team_name);



-- --------------------------------x-------------------------
-- CREATE TABLE match_details (
--     match_id INT PRIMARY KEY,
--     team_a VARCHAR(50),
--     team_b VARCHAR(50),
--     total_run_score INT,
--     total_wickets_taken INT,
--     match_result VARCHAR(20),
--     FOREIGN KEY (team_a) REFERENCES tournament_matches (team_name),
--     FOREIGN KEY (team_b) REFERENCES tournament_matches (team_name)
-- );
-- ----------------------------x----------------------------------------

-- CREATE TABLE scoreboard (
--     team_name VARCHAR(50) PRIMARY KEY,
--     games_played INT,
--     total_runs_scored INT,
--     avg_run_rate FLOAT
-- );
-- -------------------------x------------------------------------

-- INSERT INTO scoreboard (team_name, games_played, total_runs_scored)
-- SELECT
--     tm.team_name,
--               COUNT(md.match_id) AS games_played,
--                SUM(md.total_run_score) AS total_runs_scored
-- FROM
--     tournament_matches tm
-- LEFT JOIN
--     match_details md ON tm.team_name = md.team_a OR tm.team_name = md.team_b
-- GROUP BY
--     tm.team_name;
-- ----------------------------------------x------------------------------------
-- Calculate the average run rate using a SELECT statement
-- SELECT
--     team_name,
--     games_played,
--     total_runs_scored,
--     total_runs_scored / games_played AS avg_run_rate
-- FROM
--     scoreboard;
-- ---------------------------x-------------------------------
UPDATE scoreboard AS s
JOIN (
    SELECT team_name, total_runs_scored / games_played AS new_avg_run_rate
    FROM scoreboard
) AS subquery ON s.team_name = subquery.team_name
SET s.avg_run_rate = subquery.new_avg_run_rate;


-- ----------------------------x---------------------------
-- CREATE TABLE team_details (
--     ID INT AUTO_INCREMENT PRIMARY KEY,
--     Team_name VARCHAR(255),
--     Player_ID INT,
--     Player_name VARCHAR(255),
--     Player_role VARCHAR(255),
--     FOREIGN KEY (Team_name) REFERENCES tournament_matches (team_name)
-- );
-- -------------------x--------------------------------
-- INSERT INTO team_details (Team_name, Player_ID, Player_name, Player_role)
-- VALUES
-- ('NZ', 1, 'Kane Williamson', 'Batsman'),
-- ('NZ', 2, 'Martin Guptill', 'Opening Batsman'),
-- ('NZ', 3, 'Devon Conway', 'Opening Batsman/Wicket-keeper'),
-- ('NZ', 4, 'Ross Taylor', 'Batsman'),
-- ('NZ', 5, 'Tom Latham', 'Batsman/Wicket-keeper'),
-- ('NZ', 6, 'James Neesham', 'All-rounder'),
-- ('NZ', 7, 'Mitchell Santner', 'All-rounder'),
-- ('NZ', 8, 'Tim Southee', 'Fast Bowler'),
-- ('NZ', 9, 'Trent Boult', 'Fast Bowler'),
-- ('NZ', 10, 'Lockie Ferguson', 'Fast Bowler'),
-- ('NZ', 11, 'Ish Sodhi', 'Spin Bowler');
-- -------------------------------X-----------------------------







