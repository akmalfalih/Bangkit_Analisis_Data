import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


st.set_option('deprecation.showPyplotGlobalUse', False)

def plot_trend(grouped_data):
    plt.figure(figsize=(12, 8))
    for column in grouped_data.columns:
        plt.plot(grouped_data.index, grouped_data[column], label=column)

    plt.title('Tren Data Dingling Berdasarkan Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Rata-rata')
    plt.legend(loc='upper left')
    plt.grid(True)

    years = grouped_data.index.astype(int)
    plt.xticks(years)

    st.pyplot()

def plot_O3(df):
    O3_data = df.groupby(by="year").agg({
        'O3': 'mean'
    })

    plt.figure(figsize=(12, 6))
    O3_data.plot(title='Tren Tahunan O3', marker='o')
    plt.xlabel('Tahun')
    plt.ylabel('Rata-rata O3')
    plt.grid(True)
    plt.xticks(O3_data.index)

    st.pyplot()

def airComposition(df):
    # Filter data untuk tahun 2016
    data_2016 = df[df['year'] == 2016]

    # Hitung rata-rata nilai parameter SO2, NO2, CO, dan O3
    mean_values = data_2016[['SO2', 'NO2', 'CO', 'O3']].mean()

    # Hitung persentase masing-masing parameter
    total_mean = mean_values.sum()
    percentages = (mean_values / total_mean) * 100

    # Menentukan warna bar berdasarkan nilai tertinggi
    colors = ['skyblue' if val != percentages.max() else 'orange' for val in percentages]

    # Menyajikan data dalam diagram
    plt.figure(figsize=(10, 6))
    percentages.plot(kind='bar', color=colors)
    plt.title('Persentase Parameter SO2, NO2, CO, dan O3 pada Tahun 2016')
    plt.ylabel('Persentase (%)')
    plt.xticks(rotation=0)
    st.pyplot()

def findCorrelation(df):
    corr_matrix = df.drop(columns=["No", "year", "month", "day", "hour"]).corr(numeric_only=True)

    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Heatmap Korelasi antara Parameter Kualitas Udara')
    st.pyplot()

data_dingling = pd.read_csv("dashboard/data_dingling.csv", delimiter=",")

grouped_data = data_dingling.groupby(by="year").agg({
    "PM2_5": "mean",
    "PM10": "mean",
    "SO2": "mean",
    "NO2": "mean",
    "CO": "mean",
    "O3": "mean",
    "Temperature": "mean",
    "Pressure": "mean",
    "DEWP": "mean",
    "Rain": "mean",
    "WSPM": "mean"
})

st.title("DATA KUALITAS UDARA DI DINGLING")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Per Tahun", "Tren Data", "Data O3", "Komposisi Udara 2016", "Korelasi Data"])

with tab1:
    st.header("Data Rata-rata Kualitas Udara Berdasarkan Tahun")
    st.write(grouped_data)

    
with tab2:
    st.header("Tren Kualitas Udara 2013-2017")
    plot_trend(grouped_data)
    st.markdown(
        """
Berdasarkan grafik di atas, nilai seluruh parameter cenderung stabil dari tahun 2013 hingga 2017. Akan tetapi, terlihat bahwa unsur CO di udara mengalami kenaikan yang signifikan pada tahun 2016.
        """
    )

with tab3:
    st.header("Tren Rata-rata O3 2013-2017")
    plot_O3(data_dingling)
    st.markdown(
        """
Berdasarkan grafik, nilai rata-rata O3 sepanjang tahun paling tinggi berada pada tahun 2014 dengan nilai 72.515434. Setelah tahun 2014, nilai rata-rata O3 sepanjang tahun mengalami penurunan. Terjadi penurunan nilai nilai rata-rata O3 sepanjang tahun yang signifikan dari tahun 2016 ke 2017, yakni dari nilai 67.357060 ke 53.948925
        """
    )

with tab4:
    airComposition(data_dingling)
    st.markdown(
    """
Persentase komposisi udara pada tahun 2016 adalah SO2: 0.748521%, NO2: 2.615081%, CO: 89.725000%, dan O3: 6.911398%. Sehingga, unsur yang mendominasi komposisi udara pada tahun 2016 adalah CO.
    """
    )

with tab5:
    findCorrelation(data_dingling)
    st.markdown(
        """
Berdasarkan gambar di atas, kita bisa mengetahui parameter apa saja yang memiliki korelasi yang kuat. Parameter yang memiliki pengaruh positif paling kuat adalah DEWP dengan nilai 0.823683914367152. Sedangkan, parameter yang memiliki pengaruh negatif paling kuat adalah PRES dengan nilai -0.8377636522753331.
        """
    )