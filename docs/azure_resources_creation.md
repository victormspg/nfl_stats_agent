
## Create Azure Resources

Follow these steps to deploy the necessary Azure services.

---

### 1️⃣ Sign in to Azure
- Go to https://portal.azure.com
- Sign in with your Microsoft account or create one if needed
---

### 2️⃣ Create a Resource Group
- In the search bar, type **"Resource groups"**
- Click **+ Create**
- Choose a subscription, name your resource group (e.g., `nfl-agent-rg`), and select a region
- Click **Review + Create**, then **Create**
---

### 3️⃣ Deploy Azure Database for PostgreSQL Flexible Server
- In the search bar, type **"Azure Database for PostgreSQL Flexible Server"**
- Click **+ Create**
- Choose:
  - **Deployment option**: Flexible Server
  - **Resource group**: Select the one you created
  - **Server name**: e.g., `nfl-postgres`
  - **Region**: Same as your resource group
  - **Authentication**: Use password authentication
  - **Admin username**: e.g., `adminuser`
  - **Password**: Choose a secure password
- Click **Next** through the tabs, keeping defaults
- Click **Review + Create**, then **Create**

> 🔐 After deployment, go to **Networking** and allow public access or configure VNet if needed.

---

### 4️⃣ Deploy Azure AI Foundry Service
- In the search bar, type **"Azure AI Studio"** or go to [https://ai.azure.com- Click **+ Create a new project**
- Choose a name (e.g., `nfl-agent-project`) and select your resource group
- Click **Create**

---

### 5️⃣ Deploy Models in Azure AI Studio
1. Open Azure AI Studio
2. In the left panel, go to **My assets > Models + endpoints**
3. Click **+ Deploy model** > **Deploy base model**
4. Search for `text-embedding-ada-002`
5. Click **Confirm**, keep default settings, and click **Deploy**
6. Repeat the steps for `gpt-4.1`

> ✅ Once deployed, copy the endpoint URLs and keys for both models.

---
