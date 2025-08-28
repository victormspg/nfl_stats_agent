# 🏈 Multi-Agent NFL Analytics System
**Empowering Tactical Decision-Making with AI Agents**  
Developed by **Victor Santana Puga**

---

## 📌 Overview

This project showcases a multi-agent AI system designed to analyze NFL games, players, plays, and formations. It leverages intelligent agents to automate tactical analysis, assess strategy effectiveness, and answer complex football-related questions—empowering coaches, analysts, and decision-makers.

---

# 🎯 Objectives

- Facilitate faster, data-driven tactical decisions in football.
- Automate the analysis of formations and plays using real match data.
- Evaluate team and player performance with key metrics.
- Enable natural language interaction with specialized agents.

---

## 🔍 Use Cases

- **Analytics & Comparison**  
  Analyze player and game statistics  
  Compare teams and players across seasons

- **Tactical Insights**  
  Simulate tactical scenarios  
  Recommend optimal formations based on context

- **Summarization & Interpretation**  
  Generate automated game summaries  
  Highlight and explain key events

---

## Architecture


## 🧠 Agents Description

AgentDescriptionMaster AgentOrchestrates user interactions, classifies intent, and delegates tasks to specialized agents while maintaining session continuity.| **Game Analyst Agent** | Delivers insights from game-level data, including team performance, match summaries, and key events. |
| **Player Analyst Agent** | Analyzes individual player metrics, trends, and comparisons across games and seasons. |
| **Formation Strategist Agent** | Evaluates tactical formations and recommends optimal setups based on game context and strategy. |

---

## 🗂️ Dataset

Source: [Beginners Sports Analytics NFL Dataset (Kaggle)](https://www.kaggle.com/datasets/aryashah2k/beginners-sports-analytics-nfl-dataset)

> 📌 **Data Coverage:**  
> The datasets contain information from the **2018 NFL regular season**.  
> The `week_data` file includes player tracking data **only for Week 11**.

- **Games**: Metadata for each NFL game (date, time, teams, week).
- **Players**: Biographical and physical data (height, weight, position, college).
- **Plays**: Tactical and scoring details (formations, down, yardage, EPA, penalties).
- **Week Data**: Player tracking data per frame (position, speed, orientation, events).

---


## ⚙️ Tech Stack

- 🐍 **Python + Semantic Kernel Framework**  
  Agent definition and orchestration

- 🛢️ **PostgreSQL on Azure**  
  Storage for datasets and chat history

- 🤖 **Azure OpenAI Models**  
  - `text-embedding-ada-002`: Semantic embeddings for retrieval  
  - `gpt-4.1`: LLM for agent reasoning and response generation

---

## 📁 Repository Structure

nfl_stats_agent/
├── agents/
│   ├── master_agent.py
│   ├── game_analyst.py
│   ├── player_analyst.py
│   └── formation_strategist.py
├── data/
│   ├── games.csv
│   ├── players.csv
│   ├── plays.csv
│   └── week_data.csv
├── embeddings/
├── chat_history/
├── config/
│   └── semantic_kernel.yaml
└── README.md


## Prerequisites

1. Create azure resources

2. Create football and chat_history Databases

---

## 🚀 Getting Started

1. Clone the repo:
   ```bash
   git clone https://github.com/victormspg/nfl_stats_agent.git
   cd nfl_stats_agent

2. Open folder and create a python env:

3. Install dependencies:
    pip install -r requirements.txt

4. Configure resource credentials
    .env

5. Tables Creation & Population
    notebook workflows/football_db_setup.ipynb

6. Chat History Table Creation
    notebook workflows/chat_history_db_setup.ipynb

7. Embeddings Creation
    embeddings_creation.ipynb

8. Run the Multi-Agent system
    python run agent_orchestrator.py

