-- =========================
-- Cricbuzz LiveStats MySQL Schema (FINAL FIXED)
-- =========================

-- VENUES
CREATE TABLE IF NOT EXISTS venues (
    venue_id INT AUTO_INCREMENT PRIMARY KEY,
    venue_name VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    capacity INT
);

-- TEAMS
CREATE TABLE IF NOT EXISTS teams (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL UNIQUE,
    country VARCHAR(100),
    team_short_name VARCHAR(10)
);

-- PLAYERS
CREATE TABLE IF NOT EXISTS players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(255) NOT NULL,
    country VARCHAR(100),
    batting_style VARCHAR(100),
    bowling_style VARCHAR(100),
    role VARCHAR(50)
);

-- SERIES
CREATE TABLE IF NOT EXISTS series (
    series_id INT AUTO_INCREMENT PRIMARY KEY,
    series_name VARCHAR(255) NOT NULL,
    season VARCHAR(50),
    format VARCHAR(50)
);

-- MATCHES
CREATE TABLE IF NOT EXISTS matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    match_title VARCHAR(255),
    team1_id INT,
    team2_id INT,
    venue_id INT,
    series_id INT,
    match_date DATE,
    match_status VARCHAR(100),
    winning_team_id INT,
    win_margin VARCHAR(100),
    player_of_match VARCHAR(255),

    FOREIGN KEY (team1_id) REFERENCES teams(team_id),
    FOREIGN KEY (team2_id) REFERENCES teams(team_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
    FOREIGN KEY (series_id) REFERENCES series(series_id)
);

-- BATTING STATS
CREATE TABLE IF NOT EXISTS batting_stats (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT,
    match_id INT,
    format VARCHAR(50),
    runs INT DEFAULT 0,
    balls_faced INT DEFAULT 0,
    fours INT DEFAULT 0,
    sixes INT DEFAULT 0,
    strike_rate FLOAT,
    dismissal_type VARCHAR(100),

    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);

-- BOWLING STATS
CREATE TABLE IF NOT EXISTS bowling_stats (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT,
    match_id INT,
    format VARCHAR(50),
    wickets INT DEFAULT 0,
    overs DECIMAL(5,1),
    runs_conceded INT,
    maidens INT,
    economy_rate FLOAT,

    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);

-- CAREER STATS
CREATE TABLE IF NOT EXISTS career_stats (
    player_id INT PRIMARY KEY,
    matches INT DEFAULT 0,
    runs INT DEFAULT 0,
    wickets INT DEFAULT 0,
    batting_average FLOAT,
    batting_strike_rate FLOAT,
    bowling_average FLOAT,
    centuries INT DEFAULT 0,
    half_centuries INT DEFAULT 0,
    five_wickets INT DEFAULT 0,

    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

-- =========================
-- SAMPLE DATA
-- =========================

INSERT INTO teams (team_name, country, team_short_name) VALUES
('India', 'India', 'IND'),
('Australia', 'Australia', 'AUS'),
('England', 'England', 'ENG'),
('Pakistan', 'Pakistan', 'PAK'),
('New Zealand', 'New Zealand', 'NZ'),
('South Africa', 'South Africa', 'SA');

INSERT INTO venues (venue_name, city, country, capacity) VALUES
('Eden Gardens', 'Kolkata', 'India', 68000),
('Wankhede Stadium', 'Mumbai', 'India', 33000),
('M. Chinnaswamy Stadium', 'Bangalore', 'India', 40000),
("Lord's", 'London', 'England', 30000),
('MCG', 'Melbourne', 'Australia', 100024),
('Gaddafi Stadium', 'Lahore', 'Pakistan', 27000);

INSERT INTO players (player_name, country, batting_style, bowling_style, role) VALUES
('Virat Kohli', 'India', 'Right-hand bat', 'Right-arm medium', 'Batsman'),
('Rohit Sharma', 'India', 'Right-hand bat', 'Right-arm offbreak', 'Batsman'),
('Jasprit Bumrah', 'India', 'Right-hand bat', 'Right-arm fast', 'Bowler'),
('Ravindra Jadeja', 'India', 'Left-hand bat', 'Left-arm orthodox', 'All-rounder'),
('Pat Cummins', 'Australia', 'Right-hand bat', 'Right-arm fast', 'Bowler'),
('Joe Root', 'England', 'Right-hand bat', 'Right-arm offbreak', 'Batsman');

INSERT INTO career_stats (player_id, matches, runs, wickets, batting_average, batting_strike_rate, centuries, half_centuries)
VALUES
(1, 265, 12898, 4, 57.32, 93.45, 46, 65),
(2, 243, 9825, 2, 48.63, 89.92, 30, 48),
(3, 120, 150, 148, 12.34, 45.67, 0, 0),
(4, 156, 2856, 220, 32.45, 85.67, 1, 12),
(5, 89, 765, 242, 22.45, 67.89, 0, 0),
(6, 130, 8522, 0, 49.83, 86.45, 21, 45);