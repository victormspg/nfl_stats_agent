# 🛠️ `.env` File Configuration Guide

This guide walks you through the step-by-step process of completing the `.env` file required to run the [NFL Stats Agent](https://github.com/victormspg/nfl_stats_agent). The `.env` file stores sensitive credentials and configuration values for Azure services and PostgreSQL databases.

---

### 1️⃣ Clone the `.env` Example

- Copy the .env.example file from the repo root and rename it:
    ```bash
    cp .env.example .env
    ```

### 2️⃣ Sign in to Azure
- Go to https://portal.azure.com

---

### 3️⃣ Collect and Update Azure Sunscription and Resource Group

- In the search bar at the top, type **"Resource groups"**
- Click on the resource group you created earlier (e.g., `nfl-agent-rg`)
- Collect the Subscription ID and Resource Group Name.
- Update the values on the `# Azure Subscription and Resource Group` section of the `.env` file.

---

### 4️⃣ Collect and Update PostgreSQL credentials and details
- Inside the resource group, find and click on your **Azure Database for PostgreSQL Flexible Server** (e.g., `nfl-postgres`)
- This opens the server overview page
- Collect the PostgreSQL Endpoint (POSTGRES_HOST) and Server name (POSTGRES_SERVER_NAME).
- Update the values on the `# PostgreSQL Database` section of the `.env` file.

---

### 5️⃣ Collect and Update Azure Open AI Models credentials and details
- Inside the resource group, find and click on your **Azure AI Foundry project** (e.g., `nfl-agent-project`)
- Launch the Azure AI Foundry Portal.
- In the left panel, go to **My assets > Models + endpoints**
- click on both models and collect below values.
    #### Azure OpenAI
    - **AZURE_OPENAI_API_KEY:** key
    - **AZURE_OPENAI_ENDPOINT:** Target URI (e.g., `https://<azure-foundry-service>.cognitiveservices.azure.com/openai/deployments/gpt-4.1/chat/completions?api-version=2025-01-01-preview`)
    - **AZURE_OPENAI_API_VERSION:** api-version value on Target URI (e.g., `2024-12-01-preview`)
    - **AZURE_OPENAI_CHAT_DEPLOYMENT_NAME:** Deployment name (e.g., `gpt-4.1`)

    #### Embedding Model
    - **AZURE_OPENAI_EMBED_ID:** Deployment name (e.g., `text-embedding-ada-002`)
    - **AZURE_OPENAI_EMBED_MODEL:** Deployment name (e.g., `text-embedding-ada-002`)
    - **AZURE_OPENAI_EMBED_DIMENSIONS:** 1536 (If you are using a different model, search for its associate number of dimensions) 
    - **AZURE_OPENAI_EMBEDDING_COLUMN:** Deployment name (e.g., `text-embedding-ada-002`)
    - **AZURE_OPENAI_EMBED_ENDPOINT**: Target URI (e.g., `https://<azure-foundry-service>.cognitiveservices.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2023-05-15`)
    - **AZURE_OPENAI_BASE_EMBED_URL**: Target URI without `/embeddings?api-version=...` (e.g., `https://<azure-foundry-service>.cognitiveservices.azure.com/openai/deployments/text-embedding-ada-002`)

- Update the values on the `# Azure OpenAI` and `# Azure OpenAI` section of the `.env` file.

---
