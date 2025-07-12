# --- Import Libraries ---
import streamlit as st 
import pandas as pd
import numpy as np 
import pickle 
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


# --- Konfigurasi Halaman ---
st.set_page_config(
	    page_title="Sales Analysis",
	    page_icon="📊", 
	    layout="centered",
	    initial_sidebar_state="auto"
	)


# -- Load Data --
@st.cache_data
def load_data():
    file_path = "C:/Users/LENOVO/Downloads/superstore_dataset.xlsx"
    try:
        df = pd.read_excel(file_path)
        # Konversi kolom 'order_date' ke datetime
        if 'order_date' in df.columns:
            df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
            df.dropna(subset=['order_date'], inplace=True) # Hapus baris dengan tanggal tidak valid
        return df
    except FileNotFoundError:
        st.error(f"File not found at path {file_path}. Please ensure the path is correct.")
        return pd.DataFrame() # Kembalikan DataFrame kosong jika file tidak ditemukan
    except Exception as e:
        st.error(f"An error occurred while loading the file: {e}")
        st.info("Please ensure 'openpyxl' is installed using `pip install openpyxl`.")
        return pd.DataFrame()

# --- Memuat Data ---
df = load_data()


# --- Judul dan Deskripsi ---
st.title("📊 Sales Analysis")
st.markdown("This dashboard provides an overview of sales analysis")


# --- Dashboard ---
st.header("Key Visualizations")

# --- Monthly Sales Trend ---
if 'order_date' in df.columns and 'sales' in df.columns:
    st.subheader("Monthly Sales Trend")
    df_monthly_sales = df.set_index('order_date')['sales'].resample('M').sum().reset_index()


    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_monthly_sales['order_date'], df_monthly_sales['sales'], marker='o')
    ax.set_title('Total Sales per Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Sales')
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig) 
else:
    st.info("Columns 'order_date' or 'sales' not found for sales trend visualization.")

# --- Sales by Category ---
if 'category' in df.columns and 'sales' in df.columns:
    st.subheader("Sales by Category")
    df_category_sales = df.groupby('category')['sales'].sum().reset_index().sort_values(by='sales', ascending=False)
    
    fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
    ax_bar.bar(df_category_sales['category'], df_category_sales['sales'])
    ax_bar.set_title('Total Sales by Category')
    ax_bar.set_xlabel('Category')
    ax_bar.set_ylabel('Total Sales')

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig_bar)

# --- Footer ---
st.markdown("---")