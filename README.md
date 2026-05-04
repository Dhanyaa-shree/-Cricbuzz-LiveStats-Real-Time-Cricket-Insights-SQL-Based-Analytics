# 🏏 Cricbuzz LiveStats Dashboard

A **Python + Streamlit-based cricket analytics dashboard** that delivers real-time match updates, live scorecards, and player insights using the Cricbuzz API.

The application integrates with a **MySQL database** to store and manage structured cricket data, including players, squads, and performance statistics. It also features interactive data visualization, SQL query execution, and full CRUD operations — making it a complete end-to-end data-driven application.

---

## 🚀 Features

### 📊 Live Cricket Updates

* Real-time match data (scores, status, venues)
* Auto-refresh every 30 seconds

### 📝 Scorecards & Player Insights

* Batting & bowling statistics
* Player performance analysis

### 🎯 Interactive Dashboard

* Built with Streamlit
* Filters by format, status, and venue
* Click to view detailed match insights

### 🗄️ Database Integration

* MySQL backend
* Efficient data storage & retrieval

### 🔎 SQL Query Playground

* Execute custom SQL queries
* Pre-built analytics queries
* Interactive schema explorer

### 🛠 CRUD Operations

* Add, update, delete, and view data
* Manage players, matches, and stats

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/cricbuzz-livestats.git
cd cricbuzz-livestats
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

```env
RAPIDAPI_KEY="your_api_key_here"
DB_HOST="localhost"
DB_USER="root"
DB_PASSWORD="your_password"
DB_NAME="cricket_db"
```

### 4️⃣ Run the Application

```bash
streamlit run app.py
```

---

## 📸 Screenshots

### 🔹 Home Page

<img src="https://github.com/user-attachments/assets/c3c9ea2a-f934-4c25-bd52-5dc4bc87215f" width="800"/>

### 🔹 Live Match Dashboard

<img src="https://github.com/user-attachments/assets/e52699a6-b99d-4167-9d96-619f81d4110d" width="800"/>

### 🔹 CRUD Operations Dashboard

<img src="https://github.com/user-attachments/assets/0a7c261b-4dfa-4459-9bc3-6d2680dfbeca" width="800"/>

---

## 🎯 Key Modules

* 🔴 **Live Matches Dashboard** – real-time updates & ball-by-ball data
* 📈 **Top Stats & Analytics** – leaderboards & performance trends
* 🧠 **SQL Query Playground** – custom queries & schema explorer
* ⚡ **CRUD Operations** – full database interaction

---

## 📁 Project Structure

```
CRICKETANALYTICS/
│── app.py
│── config.py
│── requirements.txt
│── pages/
│── utils/
│── data/
```

---

## 📦 Requirements

* streamlit
* pandas
* plotly
* requests
* python-dotenv

---

## 🙏 Acknowledgements

* Cricbuzz API – real-time cricket data
* Streamlit – UI framework
* MySQL – database system

---

## 👩‍💻 Author

**Dhanyaa Shree T**

---



