# 📘 Data Dictionary

This document describes the schema and column definitions for the four datasets used in the Multi-Agent NFL Analytics System.

> 📌 **Scope:**
> All datasets are based on the **2018 NFL regular season**. Week Data is limited to Week 11 tracking information.
---

## 🏈 Games Dataset
Metadata for each NFL game.

| Column            | Description                                  |
|-------------------|----------------------------------------------|
| `gameId`          | Unique identifier for each game (numeric)    |
| `gameDate`        | Date of the game (mm/dd/yyyy)                |
| `gameTimeEastern` |Start time of the game in EST (HH:MM:SS)      |
|`homeTeamAbbr`     | Home team abbreviation (text)                | 
|`visitorTeamAbbr`  | Visiting team abbreviation (text)            |
| `week`            | Week number of the game (numeric)            |

---

## 🧍 Players Dataset
Biographical and physical attributes of NFL players.

| Column         | Description                                                 |
|----------------|-------------------------------------------------------------|
| `nflId`        | Unique player identifier (numeric)                          |
| `height`       | Player height (text)                                        |
| `weight`       | Player weight (numeric)                                     |
| `birthDate`    | Date of birth (YYYY-MM-DD)                                  |
| `collegeName`  | College attended (text)                                     |
| `position`     | Player position (text)                                      |
| `displayName`  | Player name (text)                                          |

---

## 📊 Plays Dataset
Detailed information about each play.

| Column                   | Description                                                 |
|--------------------------|-------------------------------------------------------------|
| `gameId`                 | Game identifier (numeric)                                   |
| `playId`                 | Play identifier (numeric)                                   |
| `playDescription`        | Description of the play (text)|                             |
|`quarter`                 | Quarter of the game (numeric)                               |
| `down`                   | Down number (numeric)                                       |
| `yardsToGo`              | Yards needed for a first down (numeric)                     |
| `possessionTeam`         | Team on offense (text)                                      |
| `playType`               | Type of play (text)                                         |
| `yardlineSide`           | Team code for line-of-scrimmage (text)                      |
| `yardlineNumber`         | Yard line number (numeric)                                  |
| `offenseFormation`       | Offensive formation used (text)                             |
| `personnelO`             | Offensive personnel (text)                                  |
| `defendersInTheBox`      | Number of defenders near line-of-scrimmage (numeric)        |
| `numberOfPassRushers`    | Number of pass rushers (numeric)                            |
| `personnelD`             | Defensive personnel (text)                                  |
| `typeDropback`           | Quarterback dropback type (text)                            |
| `preSnapHomeScore`       | Home team score before play (numeric)                       |
| `preSnapVisitorScore`    | Visitor team score before play (numeric)                    |
| `gameClock`              | Time on play clock (MM:SS)                                  |
| `absoluteYardlineNumber` | Distance from end zone (numeric)                            |
| `penaltyCodes`           | Penalty types (text, separated by `;`)                      |
| `penaltyJerseyNumber`    | Jersey numbers of penalized players (text, separated by `;`)|
| `passResult`             | Result of passing play (text)                               |
| `offensePlayResult`      | Yards gained excluding penalties (numeric)                  |
| `playResult`             | Net yards gained including penalties (numeric)              |
| `epa`                    | Expected points added (numeric)                             |
| `isDefensivePI`          | Indicator for defensive pass interference (TRUE/FALSE)      |

---

## 📍 Week Data Dataset
Player tracking data per frame.

| Column         | Description                                                 |
|----------------|-------------------------------------------------------------|
| `time`         | Timestamp of play (yyyy-mm-dd hh:mm:ss)                     |
| `x`            | Player position along field length (0–120 yards)            |
| `y`            | Player position along field width (0–53.3 yards)            |
| `s`            | Speed in yards/second (numeric)                             |                              
| `a`            | Acceleration in yards/second² (numeric)                     |
| `dis`          | Distance traveled since last frame (numeric)                |
| `o`            | Player orientation (degrees)                                |
| `dir`          | Direction of motion (degrees)                               |
| `event`        | Tagged play event (e.g., snap, tackle)                      |
| `nflId`        | Player identifier (numeric)                                 |
| `displayName`  | Player name (text)                                          |
| `jerseyNumber` | Jersey number (numeric)                                     |
| `position`     | Player position group (text)                                |
| `team`         | Team affiliation (home/away)                                |
| `frameId`      | Frame number in play sequence (numeric)                     |
| `gameId`       | Game identifier (numeric)                                   |
| `playId`       | Play identifier (numeric)                                   |
| `playDirection`| Direction of offensive play (left/right)                    |
| `route`        | Route run by offensive player (text)                        |

---

