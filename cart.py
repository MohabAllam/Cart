
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout= 'wide', page_title= 'Shopping Cart EDA')

html_title = """<h1 style="color:white;text-align:center;"> Shopping Cart Exploratory Data Analysis </h1>"""
st.markdown(html_title, unsafe_allow_html=True)

df = pd.read_csv('cleaned_df.csv', index_col= 0)

page = st.sidebar.radio('Pages', ['Intro', 'Analysis Questions', 'Report'])

if page == 'Intro':

    st.image('https://www.thewatchtower.com/assets/images/blog_images/online-shopping-is-it-really-worth-it.jpg')
    st.write('Dataframe Sample')
    st.dataframe(df.head(10))

elif page == 'Analysis Questions':

    st.write('# What is the customers percentage of Genders ?')
    # st.plotly_chart(px.pie(data_frame= df, names= 'gender'))

    st.write('# Is there a relationship between Age and customer spend ?')
    st.plotly_chart(px.scatter(data_frame= df, x= 'age', y= 'total_price'))

    col1, col2 = st.columns(2, vertical_alignment= 'center')

    col1.write('### What is the cumulative revenue over time ?')
    
    df_sorted = df.sort_values(by= 'order_date')
    df_sorted['cum_total_price'] = df_sorted.total_price.cumsum()
    col2.plotly_chart(px.line(data_frame= df_sorted, x= 'order_date', y= 'cum_total_price'))

    col = st.selectbox('Columns', df.columns)

    chart = st.selectbox('Chart', ['Histogram', 'Box', 'Pie'])

    if chart == 'Histogram':
        st.plotly_chart(px.histogram(data_frame= df, x= col))

    elif chart == 'Box':
        st.plotly_chart(px.box(data_frame= df, x= col))

    else:
        st.plotly_chart(px.pie(data_frame= df, names= col))

elif page == 'Report':

    State = st.sidebar.selectbox('State', df.state.unique())

    start_date = st.sidebar.date_input('Start Date', min_value= df.order_date.min(), max_value= df.order_date.max(), value= df.order_date.min())

    end_date = st.sidebar.date_input('End Date', min_value= df.order_date.min(), max_value= df.order_date.max(), value= df.order_date.max())

    df_filtered  = df[(df.state == State) & (df.order_date >= str(start_date)) & (df.order_date <= str(end_date))]

    st.dataframe(df_filtered)

    top_n = st.sidebar.slider('Top N', min_value= 1, max_value= 30, value= 5, step= 1)

    prod_count = df_filtered.product_name.value_counts().head(top_n).reset_index()

    st.plotly_chart(px.bar(data_frame= prod_count, x= 'product_name', y= 'count',
        labels= {'product_name': 'Product Name', 'count': 'Count of Products'},
        title= f'Top {top_n} Products'))
