import pandas as pd
import numpy as np
import os
import requests
from typing import Dict, Any, List
from app.services.data_ingestion import load_dataframe
from app.core.config import settings

def generate_ai_business_insights(file_path: str, domain: str = "Sales") -> List[Dict[str, Any]]:
    df = load_dataframe(file_path)
    
    if len(df) == 0:
        return []

    cols_map = {str(c).lower(): c for c in df.columns}
    
    def find_col(keywords: List[str]):
        for kw in keywords:
            for c_lower, orig in cols_map.items():
                if kw in c_lower:
                    return orig
        return None

    sales_col = find_col(["sales", "revenue", "amount"])
    profit_col = find_col(["profit", "margin"])
    region_col = find_col(["region", "location", "area", "city"])
    category_col = find_col(["category", "department", "type"])
    product_col = find_col(["product", "item"])
    date_col = find_col(["date", "order_date", "created_at"])
    segment_col = find_col(["segment", "channel"])

    insights = []

    # 1. Total & MoM Growth Insight
    if date_col and sales_col and pd.api.types.is_numeric_dtype(df[sales_col]):
        try:
            df_temp = df.copy()
            df_temp[date_col] = pd.to_datetime(df_temp[date_col], errors='coerce')
            df_temp = df_temp.dropna(subset=[date_col]).sort_values(by=date_col)
            
            total_rev = float(df_temp[sales_col].sum())
            
            # Split dataset into earlier half vs recent half to calculate growth
            mid_point = len(df_temp) // 2
            h1_rev = float(df_temp.iloc[:mid_point][sales_col].sum())
            h2_rev = float(df_temp.iloc[mid_point:][sales_col].sum())
            
            if h1_rev > 0:
                growth_pct = ((h2_rev - h1_rev) / h1_rev) * 100.0
                direction = "increased" if growth_pct >= 0 else "declined"
                insights.append({
                    "id": "ins_revenue_growth",
                    "title": f"Overall Revenue Trajectory",
                    "category": "Growth",
                    "type": "positive" if growth_pct >= 0 else "negative",
                    "metric": f"{'+' if growth_pct>=0 else ''}{round(growth_pct, 1)}%",
                    "impact": f"Total Revenue ₹{total_rev:,.2f}",
                    "description": f"Total business revenue {direction} by {abs(round(growth_pct, 1))}% in recent periods compared to initial baselines.",
                    "recommendation": "Maintain expansion strategy in growth channels and double down on key campaign drivers." if growth_pct >= 0 else "Audit pricing models and run targeted promotions to reverse revenue contraction."
                })
        except Exception:
            pass

    # 2. Regional Dominance & Concentration Risk
    if region_col and sales_col and pd.api.types.is_numeric_dtype(df[sales_col]):
        reg_summary = df.groupby(region_col).agg({sales_col: ['sum', 'count']})
        reg_summary.columns = ['total_sales', 'order_count']
        reg_summary = reg_summary.reset_index().sort_values(by='total_sales', ascending=False)
        
        tot_sales = float(df[sales_col].sum())
        if len(reg_summary) > 0 and tot_sales > 0:
            top_reg = reg_summary.iloc[0]
            top_reg_name = str(top_reg[region_col])
            top_reg_sales = float(top_reg['total_sales'])
            share_pct = (top_reg_sales / tot_sales) * 100.0
            
            insights.append({
                "id": "ins_top_region",
                "title": "Dominant Regional Performance",
                "category": "Regional Analytics",
                "type": "positive" if share_pct > 25 else "neutral",
                "metric": f"{round(share_pct, 1)}% Share",
                "impact": f"₹{top_reg_sales:,.2f} Sales",
                "description": f"{top_reg_name} region is the primary revenue driver, contributing {round(share_pct, 1)}% of total sales across {int(top_reg['order_count'])} orders.",
                "recommendation": f"Ensure uninterrupted supply chain and inventory allocation to {top_reg_name} to prevent stockouts."
            })

    # 3. Category Profitability & Margin Analysis
    if category_col and profit_col and sales_col:
        cat_summary = df.groupby(category_col).agg({sales_col: 'sum', profit_col: 'sum'}).reset_index()
        cat_summary['margin'] = (cat_summary[profit_col] / cat_summary[sales_col]) * 100.0
        cat_summary = cat_summary.sort_values(by='margin', ascending=False)
        
        if len(cat_summary) > 0:
            best_cat = cat_summary.iloc[0]
            worst_cat = cat_summary.iloc[-1]
            
            insights.append({
                "id": "ins_category_margin",
                "title": "Highest Margin Category",
                "category": "Profitability",
                "type": "positive",
                "metric": f"{round(best_cat['margin'], 1)}% Margin",
                "impact": f"Category: {best_cat[category_col]}",
                "description": f"'{best_cat[category_col]}' yields the highest profit margin of {round(best_cat['margin'], 1)}% generating ₹{float(best_cat[profit_col]):,.2f} profit.",
                "recommendation": f"Focus marketing budgets towards promoting '{best_cat[category_col]}' products to boost net profitability."
            })
            
            if worst_cat['margin'] < 10.0 and worst_cat[category_col] != best_cat[category_col]:
                insights.append({
                    "id": "ins_low_margin",
                    "title": "Low Profit Margin Warning",
                    "category": "Risk Analysis",
                    "type": "warning",
                    "metric": f"{round(worst_cat['margin'], 1)}% Margin",
                    "impact": f"Category: {worst_cat[category_col]}",
                    "description": f"'{worst_cat[category_col]}' has a compressed profit margin of {round(worst_cat['margin'], 1)}%, signaling high COGS or heavy discounting.",
                    "recommendation": "Review supplier unit costs or reduce discount tiers on underperforming items."
                })

    # 4. Product Concentration / Pareto Analysis
    if product_col and sales_col:
        prod_sales = df.groupby(product_col)[sales_col].sum().sort_values(ascending=False).reset_index()
        tot_sales = float(df[sales_col].sum())
        
        if len(prod_sales) >= 5 and tot_sales > 0:
            top_5_sales = float(prod_sales.head(5)[sales_col].sum())
            top_5_share = (top_5_sales / tot_sales) * 100.0
            
            insights.append({
                "id": "ins_product_pareto",
                "title": "Product Concentration Index",
                "category": "Merchandise",
                "type": "warning" if top_5_share > 50 else "neutral",
                "metric": f"{round(top_5_share, 1)}% of Revenue",
                "impact": "Top 5 Products",
                "description": f"The top 5 products account for {round(top_5_share, 1)}% of all business revenue.",
                "recommendation": "Diversify catalog promotions to lower dependence on top products." if top_5_share > 50 else "Maintain balanced inventory across top and mid-tier catalog items."
            })

    # 5. Customer Segment High Value Behavioral Insight
    if segment_col and sales_col:
        seg_summary = df.groupby(segment_col).agg({sales_col: ['sum', 'mean']})
        seg_summary.columns = ['tot_sales', 'avg_sales']
        seg_summary = seg_summary.reset_index().sort_values(by='avg_sales', ascending=False)
        
        if len(seg_summary) > 0:
            top_seg = seg_summary.iloc[0]
            insights.append({
                "id": "ins_segment_aov",
                "title": "High Value Customer Segment",
                "category": "Customer Analytics",
                "type": "positive",
                "metric": f"₹{round(float(top_seg['avg_sales']), 2)} Avg Order",
                "impact": f"Segment: {top_seg[segment_col]}",
                "description": f"The '{top_seg[segment_col]}' segment exhibits the highest average spend per transaction (₹{round(float(top_seg['avg_sales']), 2)}).",
                "recommendation": f"Develop VIP loyalty rewards or specialized enterprise tiers for '{top_seg[segment_col]}' accounts."
            })

    # Optional OpenAI Enrichment if key present
    if settings.OPENAI_API_KEY and settings.AI_PROVIDER in ["openai", "auto"]:
        try:
            # We can enrich or append an executive summary from LLM
            prompt = f"Analyze these calculated metrics for domain {domain}: {insights[:3]}. Write a 2-sentence C-level executive summary."
            headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}", "Content-Type": "application/json"}
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 150
            }
            resp = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=5)
            if resp.status_code == 200:
                ai_text = resp.json()["choices"][0]["message"]["content"].strip()
                insights.insert(0, {
                    "id": "ins_llm_exec_summary",
                    "title": "AI Executive Strategic Summary",
                    "category": "Executive Brief",
                    "type": "positive",
                    "metric": "AI Synthesis",
                    "impact": "Strategic Note",
                    "description": ai_text,
                    "recommendation": "Review operational alignment with top performing market segments."
                })
        except Exception:
            pass

    return insights
