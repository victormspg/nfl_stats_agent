
## 🗄️ Create PostgreSQL Databases

Follow these steps to create the required databases using the Azure Portal.

---

### 1️⃣ Sign in to Azure

- Go to https://portal.azure.com
- Sign in with your Microsoft account

---

### 2️⃣ Navigate to Your Resource Group

- In the search bar at the top, type **"Resource groups"**
- Click on the resource group you created earlier (e.g., `nfl-agent-rg`)

---

### 3️⃣ Open Your PostgreSQL Flexible Server

- Inside the resource group, find and click on your **Azure Database for PostgreSQL Flexible Server** (e.g., `nfl-postgres`)
- This opens the server overview page

---

### 4️⃣ Access the Query Editor (Preview)

- In the left-hand menu, scroll down and click on **"Query editor (preview)"**
- Log in using the **admin username and password** you set during server creation

---

### 5️⃣ Create the Required Databases

Paste the following SQL commands into the query editor and run them:

```bash
CREATE DATABASE football_db;
CREATE DATABASE chat_history_db;
