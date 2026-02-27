"""
Agent 1 – Dimension Navigator
Handles: Drill-Down, Roll-Up, Hierarchy Navigation
"""
from __future__ import annotations
import re
import pandas as pd
from backend.agents.base import BaseAgent
from backend.db import database as db

SYSTEM_PROMPT = """You are the Dimension Navigator Agent for an OLAP Business Intelligence system.
Your role is to translate natural language drill-down and roll-up requests into DuckDB SQL.

STAR SCHEMA:
  fact_sales(order_id, order_date, year, quarter, month, month_name,
             region, country, category, subcategory, customer_segment,
             quantity, unit_price, revenue, cost, profit, profit_margin)

HIERARCHIES:
  Time:      year → quarter → month_name
  Geography: region → country
  Product:   category → subcategory

OPERATIONS:
  Drill-Down: Group by a FINER level (e.g., year→quarter, region→country)
  Roll-Up:    Group by a COARSER level (e.g., month→quarter, country→region)

RULES:
1. Always SUM revenue, profit, quantity; AVG profit_margin.
2. Add ROUND(..., 2) to all numeric aggregates.
3. ORDER BY revenue DESC or by the grouping column.
4. Return ONLY valid DuckDB SQL — no markdown, no explanation.
5. Use WHERE clauses to filter when the user specifies a dimension value.
"""

class DimensionNavigatorAgent(BaseAgent):
    name = "Dimension Navigator"
    description = "Drill-Down & Roll-Up across Time, Geography, and Product hierarchies."

    def run(self, query: str, context: dict | None = None) -> dict:
        ctx_str = f"\nPrevious context: {context}" if context else ""

        sql_raw = self._call_llm(
            system=SYSTEM_PROMPT,
            user=f"User request: {query}{ctx_str}\n\nGenerate the SQL query:",
        )

        sql = _extract_sql(sql_raw)

        try:
            result_df = db.query(sql)
            explanation = self._explain(query, sql, result_df)
            return {
                "agent": self.name,
                "operation": "drill_down_roll_up",
                "sql": sql,
                "data": result_df.to_dict("records"),
                "columns": list(result_df.columns),
                "row_count": len(result_df),
                "explanation": explanation,
                "error": None,
            }
        except Exception as e:
            return {
                "agent": self.name,
                "operation": "drill_down_roll_up",
                "sql": sql,
                "data": [],
                "columns": [],
                "row_count": 0,
                "explanation": "",
                "error": str(e),
            }

    def _explain(self, query: str, sql: str, df: pd.DataFrame) -> str:
        if df.empty:
            return "No data found for this query."
        top = df.iloc[0]
        col0 = df.columns[0]
        return (
            self._call_llm(
                system="You are a BI analyst. Given a user question, SQL, and top result, "
                       "write a concise 2-sentence business insight. No bullet points.",
                user=f"Question: {query}\nTop result: {top.to_dict()}\nColumns: {list(df.columns)}",
            )
        )


def _extract_sql(text: str) -> str:
    """Strip markdown fences if present."""
    text = text.strip()
    match = re.search(r"```(?:sql)?\s*([\s\S]+?)```", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text
