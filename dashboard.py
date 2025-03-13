import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("all_data.csv")

with st.sidebar:
    st.title("📊 Dashboard E-Commerce") 
    st.image("mokaa.png")

st.title("E-Commerce Dashboard")

total_orders = df["order_id"].nunique()
total_customers = df["customer_id"].nunique()
total_sales = df["payment_value"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", total_orders)
col2.metric("Total Customers", total_customers)
col3.metric("Total Sales", f"${total_sales:,.2f}")

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3", "#D3D3D3"]

st.subheader("Distribusi Metode Pembayaran")
payment_counts = df["payment_type"].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=payment_counts.index, y=payment_counts.values, palette=colors, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("Metode Pembayaran yang Paling Digemari")
bypayment_df = df["payment_type"].value_counts().reset_index()
bypayment_df.columns = ["payment_type", "payment_count"]

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    y="payment_count",
    x="payment_type",
    hue="payment_type",
    data=bypayment_df.sort_values(by="payment_count", ascending=False),
    palette=colors,
    legend=False
)
plt.title("Metode Pembayaran yang Paling Digemari", loc="center", fontsize=15)
plt.ylabel("Tingkat Pemakaian", fontsize=11)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

st.subheader("Top 10 Kategori Produk Terlaris")
category_counts = df["product_category_name"].value_counts().head(10)
fig, ax = plt.subplots()
sns.barplot(x=category_counts.values, y=category_counts.index, palette=colors, ax=ax)
st.pyplot(fig)

st.subheader("Preferensi Harga Pelanggan")

if "price" in df.columns:
    Q1 = df["price"].quantile(0.25)
    Q3 = df["price"].quantile(0.75)

    bins = [0, Q1, Q3, df["price"].max()]
    labels = ["Murah", "Sedang", "Mahal"]

    df["price_category"] = pd.cut(df["price"], bins=bins, labels=labels, include_lowest=True)

    price_preference = df.groupby("price_category")["customer_id"].nunique().reset_index()
    price_preference.columns = ["price_category", "customer_count"]

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        x="price_category",
        y="customer_count",
        hue="customer_count",
        data=price_preference,
        palette=["#D3D3D3", "#D3D3D3", "#72BCD4"], legend=False
    )
    plt.title("Preferensi Harga Pelanggan", fontsize=14)
    plt.xlabel(None)
    plt.ylabel("Jumlah Pelanggan", fontsize=10)
    st.pyplot(fig)
else:
    st.warning("Kolom 'price' tidak ditemukan dalam dataset. Pastikan file 'all_data.csv' memiliki kolom ini.")

st.subheader("Top 10 Kota dengan Transaksi Terbanyak")
city_transactions = df["customer_city"].value_counts().head(10)
fig, ax = plt.subplots()
sns.barplot(x=city_transactions.values, y=city_transactions.index, palette=colors, ax=ax)
st.pyplot(fig)

st.subheader("Top 10 Negara dengan Transaksi Terbanyak")
state_transactions = df["customer_state"].value_counts().head(10)
fig, ax = plt.subplots()
sns.barplot(x=state_transactions.values, y=state_transactions.index, palette=colors, ax=ax)
st.pyplot(fig)


city_transactions = df["customer_city"].value_counts().reset_index()
city_transactions.columns = ["city", "transaction_count"]

Q1 = city_transactions["transaction_count"].quantile(0.25)
Q3 = city_transactions["transaction_count"].quantile(0.75)

bins = [0, Q1, Q3, city_transactions["transaction_count"].max()]
labels = ["Peluang Kecil", "Peluang Sedang", "Peluang Besar"]

city_transactions["business_opportunity"] = pd.cut(
    city_transactions["transaction_count"], bins=bins, labels=labels, include_lowest=True
)

category_opportunity_city = city_transactions["business_opportunity"].value_counts().reset_index()
category_opportunity_city.columns = ["business_opportunity", "count"]

st.subheader("Peluang Bisnis Berdasarkan Kota")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x="business_opportunity",
    y="count",
    data=category_opportunity_city,
    order=["Peluang Besar", "Peluang Sedang", "Peluang Kecil"],
    palette=["#72BCD4", "#72BCD4", "#72BCD4"],
    ax=ax
)
plt.xlabel(None)
plt.ylabel("Jumlah Kota")
plt.title("Distribusi Peluang Bisnis Berdasarkan Kota", fontsize=15)
st.pyplot(fig)
