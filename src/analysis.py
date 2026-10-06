"""
Internship Studio - Data Analysis Project
Author: Ashutosh Ranjan

Implements the analyses shown in the Internship Studio project:
Response Plot, Transaction Amount Plot, Yearly Sales, Top 5 Customers,
Top 5 Sales, Monthly Sales, Churn Count, Top Customer Analysis,
Transactions by Month, Total Transactions Per Year, Customer Response,
Customer Segment, and Customer Frequency.

Put the original CSV at data/dataset.csv and update COLUMN_MAP if needed.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "dataset.csv"
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

COLUMN_MAP = {
    "date": "Date",
    "customer": "Customer",
    "amount": "Transaction Amount",
    "response": "Response",
    "churn": "Churn",
    "segment": "Customer Segment",
}


def load_data():
    df = pd.read_csv(DATA_FILE)
    missing = [v for v in COLUMN_MAP.values() if v not in df.columns]
    if missing:
        raise ValueError(
            f"Missing columns: {missing}. Available columns: {list(df.columns)}. "
            "Update COLUMN_MAP in src/analysis.py."
        )
    df = df.copy()
    df[COLUMN_MAP["date"]] = pd.to_datetime(df[COLUMN_MAP["date"]], errors="coerce")
    df[COLUMN_MAP["amount"]] = pd.to_numeric(df[COLUMN_MAP["amount"]], errors="coerce")
    df = df.dropna(subset=[COLUMN_MAP["date"], COLUMN_MAP["amount"]])
    df["Year"] = df[COLUMN_MAP["date"]].dt.year
    df["Month"] = df[COLUMN_MAP["date"]].dt.month
    return df


def save_plot(name):
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / name, dpi=150, bbox_inches="tight")
    plt.close()


def response_plot(df):
    c = COLUMN_MAP["response"]
    counts = df[c].astype(str).value_counts()
    sns.barplot(x=counts.index, y=counts.values)
    plt.title("Customer Response")
    plt.xlabel("Response")
    plt.ylabel("Count")
    save_plot("response_plot.png")


def transaction_amount_plot(df):
    c = COLUMN_MAP["amount"]
    sns.histplot(df[c], bins=30, kde=True)
    plt.title("Transaction Amount Plot")
    plt.xlabel("Transaction Amount")
    plt.ylabel("Frequency")
    save_plot("transaction_amount_plot.png")


def yearly_sales(df):
    c = COLUMN_MAP["amount"]
    s = df.groupby("Year")[c].sum().sort_index()
    sns.barplot(x=s.index.astype(str), y=s.values)
    plt.title("Yearly Sales")
    plt.xlabel("Year")
    plt.ylabel("Sales")
    save_plot("yearly_sales.png")
    s.rename("Sales").to_csv(OUTPUT_DIR / "yearly_sales.csv")


def top_5_customers(df):
    customer, amount = COLUMN_MAP["customer"], COLUMN_MAP["amount"]
    s = df.groupby(customer)[amount].sum().sort_values(ascending=False).head(5)
    sns.barplot(x=s.values, y=s.index)
    plt.title("Top 5 Customers")
    plt.xlabel("Total Sales")
    plt.ylabel("Customer")
    save_plot("top_5_customers.png")
    s.rename("Total Sales").to_csv(OUTPUT_DIR / "top_5_customers.csv")


def top_5_sales(df):
    customer, amount = COLUMN_MAP["customer"], COLUMN_MAP["amount"]
    top = df.nlargest(5, amount)[[customer, amount]].reset_index(drop=True)
    top.to_csv(OUTPUT_DIR / "top_5_sales.csv", index=False)
    sns.barplot(x=top[amount].values, y=top[customer].astype(str))
    plt.title("Top 5 Sales")
    plt.xlabel("Transaction Amount")
    plt.ylabel("Customer")
    save_plot("top_5_sales.png")


def monthly_sales(df):
    amount = COLUMN_MAP["amount"]
    s = df.groupby("Month")[amount].sum().reindex(range(1, 13), fill_value=0)
    labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    sns.lineplot(x=labels, y=s.values, marker="o")
    plt.title("Monthly Sales")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    save_plot("monthly_sales.png")
    pd.DataFrame({"Month": labels, "Sales": s.values}).to_csv(
        OUTPUT_DIR / "monthly_sales.csv", index=False
    )


def churn_count(df):
    c = COLUMN_MAP["churn"]
    counts = df[c].astype(str).value_counts()
    sns.barplot(x=counts.index, y=counts.values)
    plt.title("Churn Count")
    plt.xlabel("Churn")
    plt.ylabel("Count")
    save_plot("churn_count.png")
    counts.rename("Count").to_csv(OUTPUT_DIR / "churn_count.csv")


def top_customer_analysis(df):
    customer, amount = COLUMN_MAP["customer"], COLUMN_MAP["amount"]
    result = df.groupby(customer).agg(
        total_sales=(amount, "sum"),
        transaction_count=(amount, "count"),
        average_transaction=(amount, "mean"),
    ).sort_values("total_sales", ascending=False).head(10)
    result.to_csv(OUTPUT_DIR / "top_customer_analysis.csv")


def transactions_based_on_month(df):
    counts = df.groupby("Month").size().reindex(range(1, 13), fill_value=0)
    labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    sns.barplot(x=labels, y=counts.values)
    plt.title("Transactions based on Month")
    plt.xlabel("Month")
    plt.ylabel("Number of Transactions")
    save_plot("transactions_based_on_month.png")
    pd.DataFrame({"Month": labels, "Transactions": counts.values}).to_csv(
        OUTPUT_DIR / "transactions_based_on_month.csv", index=False
    )


def total_transactions_per_year(df):
    counts = df.groupby("Year").size().sort_index()
    sns.barplot(x=counts.index.astype(str), y=counts.values)
    plt.title("Total Transactions Per Year")
    plt.xlabel("Year")
    plt.ylabel("Transactions")
    save_plot("total_transactions_per_year.png")
    counts.rename("Transactions").to_csv(OUTPUT_DIR / "total_transactions_per_year.csv")


def customer_response(df):
    c = COLUMN_MAP["response"]
    counts = df[c].astype(str).value_counts()
    sns.countplot(data=df, x=c, order=counts.index)
    plt.title("Customer Response")
    plt.xlabel("Response")
    plt.ylabel("Customers")
    plt.xticks(rotation=30)
    save_plot("customer_response.png")
    counts.rename("Count").to_csv(OUTPUT_DIR / "customer_response.csv")


def customer_segment(df):
    c = COLUMN_MAP["segment"]
    counts = df[c].astype(str).value_counts()
    sns.barplot(x=counts.index, y=counts.values)
    plt.title("Customer Segment")
    plt.xlabel("Segment")
    plt.ylabel("Count")
    plt.xticks(rotation=30)
    save_plot("customer_segment.png")
    counts.rename("Count").to_csv(OUTPUT_DIR / "customer_segment.csv")


def customer_frequency(df):
    c = COLUMN_MAP["customer"]
    frequency = df.groupby(c).size().sort_values(ascending=False)
    sns.histplot(frequency, bins=20, kde=True)
    plt.title("Customer Frequency")
    plt.xlabel("Number of Transactions per Customer")
    plt.ylabel("Number of Customers")
    save_plot("customer_frequency.png")
    frequency.rename("Frequency").to_csv(OUTPUT_DIR / "customer_frequency.csv")


def main():
    df = load_data()
    for function in (
        response_plot, transaction_amount_plot, yearly_sales, top_5_customers,
        top_5_sales, monthly_sales, churn_count, top_customer_analysis,
        transactions_based_on_month, total_transactions_per_year,
        customer_response, customer_segment, customer_frequency
    ):
        plt.figure(figsize=(9, 5))
        function(df)
    print(f"Analysis completed. Results saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
