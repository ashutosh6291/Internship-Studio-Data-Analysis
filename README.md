# Internship Studio - Data Analysis

**Author:** Ashutosh Ranjan

Python implementation of the analyses presented in the Internship Studio Data
Analysis project.

## Analyses
- Response Plot
- Transaction Amount Plot
- Yearly Sales
- Top 5 Customers
- Top 5 Sales
- Monthly Sales
- Churn Count
- Analysis of Top Customers
- Transactions based on Month
- Total Transactions Per Year
- Customer Response
- Customer Segment
- Customer Frequency

## Structure
```text
Internship-Studio-Data-Analysis/
├── data/dataset.csv
├── output/
├── src/analysis.py
├── requirements.txt
└── README.md
```

## Run
1. Put the original CSV in `data/dataset.csv`.
2. Check `COLUMN_MAP` in `src/analysis.py` and change names if necessary.
3. Install:
```bash
pip install -r requirements.txt
```
4. Run:
```bash
python src/analysis.py
```

Generated charts and summary CSV files are saved in `output/`.

> The original presentation/report was available, but the original raw dataset
> and source code were not included. Therefore this is a clean Python
> implementation of the documented analyses, not a claim to reproduce the
> original source code exactly.
