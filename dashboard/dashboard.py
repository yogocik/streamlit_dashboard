import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_carousel import carousel

# Set the title of the app
st.title("Streamlit App of Data Analytics")

# Load data
data = pd.read_csv("./dashboard/all_data.csv", index_col=0)

# Display the data table
st.subheader("All Data From Station (only 100 sample)")
stations = data['station'].drop_duplicates()
make_choice = st.sidebar.selectbox('Select station:', stations)
st.dataframe(data.loc[data["station"] == make_choice].head(100))


# Allow user to download data
csv = data.to_csv(index=False)
st.download_button(
    label="Download Data as CSV",
    data=csv,
    file_name="sample_data.csv",
    mime="text/csv",
)

# Chart for first question
fig0, ax0 = plt.subplots()
temps_2013 = pd.DataFrame.from_records(
    data.loc[data['year'] == 2013].groupby(by='station').agg(
    temp_min=pd.NamedAgg(column="TEMP", aggfunc="min"),
    temp_avg=pd.NamedAgg(column="TEMP", aggfunc="mean"),
    temp_max=pd.NamedAgg(column="TEMP", aggfunc="max"),
).to_records()
)
temps_2013.sort_values(by='temp_max', ascending=True).plot(kind='barh', 
                ax=ax0,
                xlabel='station', 
                legend='reverse',
                x='station',
                title='Temperature Stats by Station',
                ylabel='temperature')
for container in ax0.containers:
    ax0.bar_label(container)
ax0.legend(
    bbox_to_anchor=(1.0, 1.0),
    fontsize='small',
)
st.pyplot(fig0)

# Chart for second question
target_df = data.loc[data['station'].isin(['Wanshouxigong', 'Huairou'])]
target_stat_df = pd.DataFrame.from_records(
    target_df.loc[target_df['year'] == 2013].groupby(by=['station', 'month']).agg(
        temp_avg=pd.NamedAgg(column="TEMP", aggfunc="mean"),
        rain_avg=pd.NamedAgg(column="RAIN", aggfunc="mean"),
        co_avg=pd.NamedAgg(column="CO", aggfunc="mean"),
    ).to_records()
)
station_df = target_stat_df.loc[(target_stat_df['station'] == 'Wanshouxigong')][target_stat_df.columns[
    ~target_stat_df.columns.isin(['month'])]]
fig1, ax1 = plt.subplots()
sns.heatmap(station_df.corr(method='pearson', numeric_only=True), ax=ax1)
ax1.set_title("Wanshouxigong Coorelation Heatmap")
st.pyplot(fig1)

station_df = target_stat_df.loc[(target_stat_df['station'] == 'Huairou')][target_stat_df.columns[
    ~target_stat_df.columns.isin(['month'])]]
fig2, ax2 = plt.subplots()
sns.heatmap(station_df.corr(method='pearson', numeric_only=True), ax=ax2)
ax2.set_title("Huairou Coorelation Heatmap")
st.pyplot(fig2)

