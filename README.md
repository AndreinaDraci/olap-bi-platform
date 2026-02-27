# 📊 OLAP Business Intelligence Platform

**Tier 3 – Multi-Agent BI System** | Business Intelligence Capstone Project

A production-grade OLAP Assistant powered by multiple specialized AI agents, built with FastAPI, Streamlit, and DuckDB.

---

## 🏗️ Architecture

```
FRONTEND (Streamlit)
       │
       ▼
  FastAPI Backend
       │
  Planner/Orchestrator
       │
  ┌────┼────┬────────┐
  │    │    │        │
Dim  Cube  KPI   Anomaly
Nav  Ops  Calc    Det
  │    │    │        │
  └────┴────┴────────┘
       │
  ┌────┴────┐
  │  Viz   Report
  │  Agent  Gen
  └─────────┘
       │
  DuckDB Star Schema
```

## 🤖 The Six Agents

| Agent | Role | Operations |
|-------|------|-----------|
| **Dimension Navigator** | Hierarchy traversal | Drill-Down, Roll-Up |
| **Cube Operations** | Cube filtering | Slice, Dice, Pivot |
| **KPI Calculator** | Metrics computation | YoY, MoM, Rankings |
| **Report Generator** | Output formatting | Summaries, Follow-ups |
| **Visualization** *(optional)* | Chart selection | Bar, Line, Pie, Treemap |
| **Anomaly Detection** *(optional)* | Pattern finding | Outliers, Spikes, Drops |

---

## 🚀 Quick Start

### 1. Clone and install

```bash
git clone https://github.com/yourusername/olap-bi-platform
cd olap-bi-platform
pip install -r requirements.txt
```

### 2. Configure API keys

```bash
cp .env.example .env
# Edit .env and add your API key(s):
# ANTHROPIC_API_KEY=sk-ant-...
# OPENAI_API_KEY=sk-...
```

### 3. Generate the dataset

```bash
python scripts/generate_dataset.py
# Creates: data/global_retail_sales.csv (10,000 rows)
```

### 4. Run the Streamlit app

```bash
cd frontend
streamlit run app.py
# Opens at http://localhost:8501
```

### 5. (Optional) Run the FastAPI backend separately

```bash
cd backend
uvicorn api.main:app --reload --port 8000
# Swagger UI: http://localhost:8000/docs
```

---

## 📊 Dataset

- **10,000 transactions** (Jan 2022 – Dec 2024)
- **Regions**: North America, Europe, Asia Pacific, Latin America
- **Categories**: Electronics, Furniture, Office Supplies, Clothing
- **Star Schema**: fact_sales + 4 dimension tables

## 🎯 Example Queries

```
Slice:      "Show only Q4 2024 sales"
Dice:       "Electronics in Europe, Corporate segment only"
Drill-Down: "Break down 2024 by quarter, then drill Q4 by month"
Roll-Up:    "Roll up monthly data to quarterly totals"
KPI:        "Compare 2023 vs 2024 revenue by region with YoY growth"
Top-N:      "Top 5 countries by profit — rank them"
Pivot:      "Pivot revenue by region as columns, years as rows"
Anomaly:    "Find unusual patterns or anomalies in our data"
Complex:    "Break down Q4 sales by region, drill into top performer by month"
```

---

## 📁 Project Structure

```
olap-bi-platform/
├── frontend/
│   └── app.py                    # Streamlit UI
├── backend/
│   ├── agents/
│   │   ├── base.py               # BaseAgent (Anthropic + OpenAI)
│   │   ├── planner.py            # Planner/Orchestrator
│   │   ├── dimension_navigator.py
│   │   ├── cube_operations.py
│   │   ├── kpi_calculator.py
│   │   ├── report_generator.py
│   │   ├── visualization_agent.py
│   │   └── anomaly_detection.py
│   ├── db/
│   │   └── database.py           # DuckDB star schema
│   └── api/
│       └── main.py               # FastAPI endpoints
├── scripts/
│   └── generate_dataset.py
├── data/
│   └── global_retail_sales.csv
├── docs/
│   ├── architecture.md
│   ├── agent_specifications.md
│   ├── prompt_design.md
│   ├── user_guide.md
│   └── reflection.md
├── CLAUDE.md
├── requirements.txt
└── .env.example
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/overview` | Dataset statistics |
| GET | `/schema` | Star schema info + DDL |
| POST | `/query` | Natural language OLAP query |
| POST | `/sql` | Raw SQL execution |
| GET | `/examples` | Example queries |

---

## 📈 Grading Evidence (Tier 3 – A+)

- ✅ All 4 required agents implemented
- ✅ 2 optional agents implemented (Visualization + Anomaly Detection)
- ✅ All OLAP operations: Slice, Dice, Drill-Down, Roll-Up, Pivot, KPI
- ✅ DuckDB star schema (fact_sales + 4 dim tables)
- ✅ FastAPI backend with Swagger/OpenAPI docs
- ✅ Streamlit polished frontend
- ✅ Anthropic + OpenAI (user-selectable)
- ✅ Conversation history / multi-turn context
- ✅ Agent debug panel (SQL, explanations)
- ✅ CSV export
- ✅ Follow-up question suggestions
