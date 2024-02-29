-- SELECT Team_name, Player_ID, COUNT(*) AS Count
-- FROM team_details
-- GROUP BY Team_name, Player_ID
-- HAVING Count > 1;
-- UPDATE team_details t1
-- JOIN (
--     SELECT Team_name, Player_ID, MIN(id) AS MinID
--     FROM team_details
--     GROUP BY Team_name, Player_ID
-- ) t2 ON t1.Team_name = t2.Team_name AND t1.Player_ID = t2.Player_ID
-- SET t1.Player_ID = t2.MinID;
-- ALTER TABLE team_details
-- ADD UNIQUE INDEX idx_Player_ID (Player_ID);
-- ------------------------------x-----------------------------
-- Sample data for match performance in Match_ID 3 (AUS vs. ENG)

-- Sample data for match performance in Match_ID 4 (IND vs. NZ)

-- Sample data for match performance in Match_ID 5 (AUS vs. PAK)

-- Sample data for match performance in Match_ID 7 (ENG vs. NZ)

-- INSERT INTO match_performance (Match_Details_ID, Player_ID, Runs_Scored, Wickets_Taken, Balls_Faced, Overs_Bowled, catches, Match_Result)
-- VALUES 
-- (7, 45, 70, 0, 80, 0.0, 0, 'Team B won'),   -- Kane Williamson's performance
-- (7, 46, 60, 0, 70, 0.0, 0, 'Team B won'),   -- Martin Guptill's performance
-- (7, 47, 40, 0, 50, 0.0, 0, 'Team B won'),   -- Devon Conway's performance
-- (7, 48, 30, 1, 40, 0.0, 1, 'Team B won'),   -- Ross Taylor's performance
-- (7, 49, 25, 0, 30, 0.0, 0, 'Team B won'),   -- Tom Latham's performance
-- (7, 50, 0, 2, 5, 4.0, 2, 'Team B won'),     -- James Neesham's performance
-- (7, 51, 0, 3, 6, 4.2, 3, 'Team B won'),     -- Mitchell Santner's performance
-- (7, 52, 0, 1, 6, 4.2, 1, 'Team A won'),     -- Tim Southee's performance
-- (7, 53, 10, 0, 15, 0.0, 0, 'Team A won'),   -- Trent Boult's performance
-- (7, 54, 5, 1, 10, 0.0, 0, 'Team A won'),   -- Lockie Ferguson's performance
-- (7, 55, 0, 0, 0, 0.0, 0, 'Team A won'),    -- Ish Sodhi's performance
-- (7, 37, 85, 0, 100, 0.0, 0, 'Team A won'), -- Joe Root's performance
-- (7, 35, 70, 0, 80, 0.0, 0, 'Team A won'),  -- Jason Roy's performance
-- (7, 36, 60, 0, 70, 0.0, 0, 'Team A won'),  -- Jonny Bairstow's performance
-- (7, 38, 45, 1, 50, 0.0, 1, 'Team A won'),  -- Jos Buttler's performance
-- (7, 39, 35, 0, 40, 0.0, 0, 'Team A won'),  -- Ben Stokes's performance
-- (7, 40, 0, 2, 5, 4.0, 2, 'Team A won'),    -- Moeen Ali's performance
-- (7, 41, 0, 1, 6, 4.2, 1, 'Team A won');    -- Jofra Archer's performance
-- -------------------------------------x------------------------------------
WITH BatsmanRuns AS (
    SELECT
        td.Team_name,
        mp.Player_ID,
        td.Player_name,
        SUM(mp.Runs_Scored) AS Total_Runs
    FROM
        match_performance mp
    JOIN
        team_details td ON mp.Player_ID = td.Player_ID
    WHERE
        td.Player_role LIKE '%Batsman%'
    GROUP BY
        td.Team_name, mp.Player_ID, td.Player_name
),
RankByRuns AS (
    SELECT
        Team_name,
        Player_ID,
        Player_name,
        Total_Runs,
        ROW_NUMBER() OVER (PARTITION BY Team_name ORDER BY Total_Runs DESC) AS PlayerRank
    FROM
        BatsmanRuns
)
SELECT
    Team_name,
    Player_ID,
    Player_name,
    Total_Runs
FROM
    RankByRuns
WHERE
    PlayerRank = 1;
-- Calculate bowling performance scores for each player in losing matches
WITH LosingMatches AS (
    SELECT
        Match_ID,
        Player_ID,
        Wickets_Taken,
        Overs_Bowled
    FROM
        match_performance
    WHERE
        Match_Result = 'Team B won'
)

-- Calculate bowling performance score for each player
SELECT
    lp.Player_ID,
    t.Team_name,
    SUM(lp.Wickets_Taken) AS Total_Wickets,
    SUM(lp.Overs_Bowled) AS Total_Overs
FROM
    LosingMatches lp
JOIN
    team_details t ON lp.Player_ID = t.Player_ID
GROUP BY
    lp.Player_ID, t.Team_name
ORDER BY
    Total_Wickets DESC, Total_Overs ASC
;
-- ------------------------------x----------------------------
WITH TeamGames AS (
    SELECT
        Team_name,
        COUNT(*) AS TotalGames,
        SUM(CASE WHEN Match_Result = 'Team A won' THEN 1 ELSE 0 END) AS GamesWon
    FROM
        match_performance mp
    JOIN
        team_details td ON mp.Player_ID = td.Player_ID
    GROUP BY
        Team_name
)

SELECT
    Team_name,
    IFNULL(GamesWon, 0) AS GamesWon,
    TotalGames,
    (IFNULL(GamesWon, 0) / 8.0) * 100 AS WinningPercentage
FROM
    TeamGames
ORDER BY
    WinningPercentage DESC;


















