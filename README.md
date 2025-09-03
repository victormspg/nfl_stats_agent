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
## 🎥 Demo

Experience the system in action:

**▶️ Watch the Demo:** [Multi-Agent NFL Analytics System](https://www.youtube.com/watch?v=gfrduCyTOKg)


## 🏗️ Architecture Diagrams

### High Level Architecture

<p align="center">
  <img src="https://github.com/victormspg/nfl_stats_agent/blob/main/images/high_level_architecture_diagram.png" alt="High Level Architecture" width="400"/>
</p>

### Multi-Agent Architecture

<p align="center">
<img src="https://github.com/victormspg/nfl_stats_agent/blob/main/images/multi_agent_architecture_diagram.png" alt="Multi-Agent Architecture" width="700"/>
</p>

---

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

## 🔄 System Flow Overview 

1. **User Initiation**:  
  The user starts a chat session, providing a customer and session ID.

2. **Intent Classification**:  
  The system analyzes the user's input to classify the intent as related to games, players, formations, or general queries.

3. **Agent Orchestration**:  
  - The system uses specialized agents:
    - **Master Agent**: General queries and delegation.
    - **Game Analyst Agent**: Game data and insights.
    - **Player Analyst Agent**: Player data and statistics.
    - **Formation Strategist Agent**: Play formations and tactical analysis.
  - Based on the classified intent, the appropriate agent is selected to handle the query.

4. **Agent Handoffs**:  
  Agents can hand off tasks to each other if a query falls outside their specialization, ensuring the right agent responds.

5. **Chat History Management**:  
  All interactions are stored in a PostgreSQL database, allowing users to resume previous sessions.

6. **Response Delivery**:  
  The selected agent processes the query and returns a response to the user, with the conversation history updated accordingly.

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
├── agent_orchestrator.py
├── requirements.txt
├── README.md
├── agents/
│   ├── master_agent/
│   │   ├── system_message.py
│   │   └── plugins/
│   │       └── master_agent_plugin.py
│   ├── game_analyst/
│   │   ├── system_message.py
│   │   └── plugins/
│   │       └── game_analyst_plugin.py
│   ├── player_analyst/
│   │   ├── system_message.py
│   │   └── plugins/
│   │       └── player_analyst_plugin.py
│   └── formation_strategist/
│       ├── system_message.py
│       └── plugins/
│           └── formation_strategist_plugin.py
├── data/
│   ├── games.csv
│   ├── players.csv
│   ├── plays.csv
│   ├── week_data.zip
│   └── data_dictionary.md
├── docs/
│   ├── azure_resources_creation.md
│   ├── env_file_configuration.md
│   └── postgresql_db_creation.md
├── helpers/
│   ├── chat_utils.py
│   ├── db_utils.py
│   └── embeddings_utils.py
├── images/
│   ├── high_level_architecture_diagram.png
│   └── multi_agent_architecture_diagram.png
├── slides/
│   └── nfl_stats_agent_capstone_project.pptx
├── workflows/
│   ├── chat_history_db_setup.ipynb
│   ├── embeddings_creation.ipynb
│   └── football_db_setup.ipynb
```

---

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
    - Add your Azure endpoints and keys and DB details to .env file. For detailed instructions refer to: [.env File Configuration Guide](https://github.com/victormspg/nfl_stats_agent/blob/main/docs/env_file_configuration.md).

5. **Run setup notebooks:**
    - [workflows/football_db_setup.ipynb](https://github.com/victormspg/nfl_stats_agent/blob/main/workflows/football_db_setup.ipynb)
    - [workflows/chat_history_db_setup.ipynb](https://github.com/victormspg/nfl_stats_agent/blob/main/workflows/chat_history_db_setup.ipynb)
    - [workflows/embeddings_creation.ipynb](https://github.com/victormspg/nfl_stats_agent/blob/main/workflows/embeddings_creation.ipynb)

6. **Launch the Multi-Agent system:**
    ```bash
    python run agent_orchestrator.py
    ```
