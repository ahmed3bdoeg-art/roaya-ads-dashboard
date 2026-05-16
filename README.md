# 🎯 ROAYA Ads Intelligence Dashboard

A premium, production-ready Streamlit web application for analyzing Meta Ads and TikTok Ads exported reports — no API connection required.

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## 📁 Project Structure

```
roaya_ads/
├── app.py            # Main Streamlit application
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## ✨ Features

### Platforms Supported
| Platform | Report Levels |
|---|---|
| **Meta Ads** | Campaign, Ad Set, Ad, Daily, Placement |
| **TikTok Ads** | Campaign, Ad Group, Ad, Daily |

### Dashboard Tabs
| Tab | Description |
|---|---|
| 📊 Overview | KPI cards, health score, spend/results charts, top campaigns |
| ⚖️ Platform Comparison | Side-by-side Meta vs TikTok metrics |
| 🚀 Campaigns | Campaign table, top performers, scatter chart |
| 📂 Ad Sets / Groups | Ad set rankings by spend and cost/result |
| 🖼️ Ads | Ad-level table, best performers |
| 📅 Daily Trends | Spend, results, CTR, and cost/result over time |
| 🎬 Creative Analysis | Hook rate, hold rate, video metrics (when available) |
| 💡 Recommendations | Rule-based prioritized action items |
| 🔍 Data Quality | File log, column mapping, data preview |
| 📥 Export Center | Download clean CSV and full Excel report |

---

## 📂 Supported File Types

- `.csv` — Meta Ads Manager or TikTok Ads Manager export
- `.xlsx` — Excel export from either platform
- Multiple files can be uploaded simultaneously

---

## 🧮 KPI Calculations

| KPI | Formula |
|---|---|
| Cost / Result | Spend ÷ Results |
| CTR | Clicks ÷ Impressions × 100 |
| CPC | Spend ÷ Clicks |
| CPM | Spend ÷ Impressions × 1,000 |
| Frequency | Impressions ÷ Reach |
| Conversion Rate | Results ÷ Clicks × 100 |
| Hook Rate | 6s Views ÷ Impressions × 100 |
| Hold Rate | 15s Views ÷ 6s Views × 100 |
| Efficiency Score | Composite 0–100 score |

---

## 💡 Recommendations Engine

Rule-based recommendations are generated automatically:

| Priority | Rule |
|---|---|
| 🔴 Critical | High spend, zero results → Pause immediately |
| 🟠 High | Low CPR vs median → Scale budget |
| 🟠 High | High CPR vs median → Optimize targeting |
| 🟡 Medium | CTR < 0.8% → Refresh creatives |
| 🟡 Medium | Frequency > 4.5 + low CTR → Ad fatigue alert |
| 🟢 Low | Top-performing ads → Duplicate to new ad sets |

---

## 📤 Excel Export Sheets

1. **Clean Data** — All normalized rows
2. **Platform Summary** — Aggregated by platform
3. **Campaign Summary** — Campaign-level metrics
4. **Ad Set Summary** — Ad set / group metrics
5. **Ad Summary** — Ad-level performance
6. **Recommended Actions** — Prioritized action plan
7. **Files Log** — Upload history and metadata

---

## 🏗️ Technology Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Streamlit | Web UI framework |
| Pandas | Data processing |
| NumPy | Numerical operations |
| Plotly | Interactive charts |
| OpenPyXL | Excel file generation |

---

## 📋 TikTok Summary Row Handling

TikTok reports often include rows like `"Total of Campaign X"`. These are automatically detected and excluded from all aggregations. The count of removed rows is shown in the Data Quality tab.

---

## 🎭 Demo Mode

If no files are uploaded, the dashboard displays realistic demo data with:
- 4 Meta Ads campaigns across 4 ad sets and 2 ads
- 3 TikTok campaigns across 3 ad groups and 2 ads
- 30 days of daily data with realistic KPI ranges
- Full video metrics for creative analysis

---

## 📝 Notes

- Currency displayed as **EGP** (Egyptian Pound) — update `fmt_spend()` in `app.py` to change
- All calculations are performed client-side; no data is sent externally
- The app is fully offline — no API keys or network access required

---

*Built for media buying teams, performance marketing agencies, and digital advertisers.*
