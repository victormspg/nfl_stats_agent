# 🏈 Multi-Agent NFL Analytics System
**Empowering Tactical Decision-Making with AI Agents**  
Developed by **Victor Santana Puga**

---

## 📌 Overview

This project showcases a multi-agent AI system designed to analyze NFL games, players, plays, and formations. It leverages intelligent agents to automate tactical analysis, assess strategy effectiveness, and answer complex football-related questions—empowering coaches, analysts, and decision-makers.

---

## 🎯 Objectives

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

## 🏗️ Architecture

### High Level Architecture

![High Level Architecture](https://github.com/victormspg/nfl_stats_agent/blob/main/images/high_level_architecture_diagram.png)

### Multi-Agent Architecture

![Multi-Agent Architecture](https://github.com/victormspg/nfl_stats_agent/blob/main/images/multi_agent_architecture_diagram.png)

## 🧠 Agents Description

| Agent                           | Description                                                                                                                         |
|---------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| **Master Agent**                | Orchestrates user interactions, classifies intent, and delegates tasks to specialized agents while maintaining session continuity.  |
| **Game Analyst Agent**          | Delivers insights from game-level data, including team performance, match summaries, and key events.                                |
| **Player Analyst Agent**        | Analyzes individual player metrics, trends, and comparisons across games and seasons.                                               |
| **Formation Strategist Agent**  | Evaluates tactical formations and recommends optimal setups based on game context and strategy.                                     |

---

## 🗂️ Dataset

**Source:** [Beginners Sports Analytics NFL Dataset (Kaggle)](https://www.kaggle.com/datasets/aryashah2k/beginners-sports-analytics-nfl-dataset)

> 📌 **Data Coverage:**  
> This dataset covers the **2018 NFL regular season**, with detailed player tracking data available **exclusively for Week 11** in the `week_data` file.

- **Games**: Metadata for each NFL game (date, time, teams, week).
- **Players**: Biographical and physical data (height, weight, position, college).
- **Plays**: Tactical and scoring details (formations, down, yardage, EPA, penalties).
- **Week Data**: Player tracking data per frame (position, speed, orientation, events).

🔍 For detailed schema definitions and field-level descriptions, refer to the [Data Dictionary](https://github.com/victormspg/nfl_stats_agent/blob/main/data/data_dictionary.md).

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

```bash
nfl_stats_agent/
├── agents/
│   ├── master_agent
│       ├── plugins
│           ├── master_agent_plugin.py
│   ├── game_analyst.py
│   ├── player_analyst.py
│   └── formation_strategist.py
├── data/
│   ├── games.csv
│   ├── players.csv
│   ├── plays.csv
│   └── week_data.csv
├── docs/
├── helpers/
├── slides/
│   └── semantic_kernel.yaml
├── workflows/
└── README.md
└── agent_orchestrator.py
```


## 🧰 Prerequisites

Before running the project, ensure you have the following installed locally:

- **Python 3.12+**
- **pip** (Python package manager)
- **Git** (for cloning the repository)

You will also need an active **Azure account** with access to the following services:

- **Azure OpenAI Service**  
  Required to deploy and access the `text-embedding-ada-002` and `gpt-4.1` models.
  
- **Azure Database for PostgreSQL Flexible Server**  
  Used to store NFL datasets and chat history.

---

### 🔧 Required Azure Resources

To run the project successfully, you must create the following resources in Azure:

- ✅ **Resource Group**  
  Logical container to organize all related resources.

- ✅ **Azure Database for PostgreSQL Flexible Server**  
  Used to host two databases:
  - `football_db`: stores NFL game, player, and play data.
  - `chat_history_db`: stores user-agent interaction history.

- ✅ **Azure AI Foundry Service**  
  Provides access to model deployment and orchestration.

- ✅ **OpenAI Model Deployments**  
  - `text-embedding-ada-002`: for semantic search and context embedding  
  - `gpt-4.1`: for natural language understanding and agent reasoning


📘 **Step-by-Step Setup Guide**  
For detailed instructions on how to create and configure these resources, refer to:
  - [Create Azure Resources](https://github.com/victormspg/nfl_stats_agent/blob/main/docs/azure_resources_creation.md).
  - [Create PostgreSQL Databases](https://github.com/victormspg/nfl_stats_agent/blob/main/docs/postgresql_db_creation.md)
---

## 🚀 Getting Started

1. **Clone the repository:**
    ```bash
    git clone https://github.com/victormspg/nfl_stats_agent.git
    cd nfl_stats_agent
    ```

2. **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure resource credentials:**
    - Add your Azure endpoints and keys and DB details to .env file.

5. **Run setup notebooks:**
    - [workflows/football_db_setup.ipynb](https://github.com/victormspg/nfl_stats_agent/blob/main/workflows/football_db_setup.ipynb)
    - [workflows/chat_history_db_setup.ipynb](https://github.com/victormspg/nfl_stats_agent/blob/main/workflows/chat_history_db_setup.ipynb)
    - [workflows/embeddings_creation.ipynb](https://github.com/victormspg/nfl_stats_agent/blob/main/workflows/embeddings_creation.ipynb)

6. **Launch the Multi-Agent system:**
    ```bash
    python run agent_orchestrator.py
    ```
