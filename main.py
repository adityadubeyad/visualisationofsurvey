import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
from streamlit_option_menu import  option_menu

st.set_page_config(page_title="Department Survey Visualisationn", page_icon=":tada:", layout="wide")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


EXAMPLE_NO = 1


def streamlit_menu(example=1):
    if example == 1:

        with st.sidebar:
            selected = option_menu(
                menu_title="Main Menu",   
                options=["Home", "About", "Contact"],   
                icons=["house", "book", "envelope"],   
                menu_icon="cast",   
                default_index=0,   
            )
        return selected


    if example == 2:

        selected = option_menu(
            menu_title=None,   
            options=["Home", "About", "Contact"],   
            icons=["house", "book", "envelope"],   
            menu_icon="cast",   
            default_index=0,   
            orientation="horizontal",
        )
        return selected


    if example == 3:

        selected = option_menu(
            menu_title=None,   
            options=["Home", "About", "Contact"],   
            icons=["house", "book", "envelope"],   
            menu_icon="cast",   
            default_index=0,   
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "25px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "green"},
            },
        )
        return selected



selected = streamlit_menu(example=EXAMPLE_NO)



if selected == "Home":

    with st.container():
        st.write("---")
        st.write("##")
    st.header('Survey Results 2022')
    with st.container():
        st.write("---")
        st.write("##")
    st.subheader('Survey Visualisation of year 2022')

    ### --- LOAD DATAFRAME
    excel_file = 'Survey_Results.xlsx'
    sheet_name = 'DATA'

    df = pd.read_excel(excel_file,
                       sheet_name=sheet_name,
                       usecols='B:D',
                       header=3)

    df_participants = pd.read_excel(excel_file,
                                    sheet_name= sheet_name,
                                    usecols='F:G',
                                    header=3)
    df_participants.dropna(inplace=True)

    # --- STREAMLIT SELECTION
    department = df['Department'].unique().tolist()
    ages = df['Age'].unique().tolist()

    age_selection = st.slider('Age:',
                            min_value= min(ages),
                            max_value= max(ages),
                            value=(min(ages),max(ages)))

    department_selection = st.multiselect('Department:',
                                        department,
                                        default=department)


    # --- FILTER DATAFRAME BASED ON SELECTION
    mask = (df['Age'].between(*age_selection)) & (df['Department'].isin(department_selection))
    number_of_result = df[mask].shape[0]
    st.markdown(f'*Available Results: {number_of_result}*')

    # --- GROUP DATAFRAME AFTER SELECTION
    df_grouped = df[mask].groupby(by=['Rating']).count()[['Age']]
    df_grouped = df_grouped.rename(columns={'Age': 'Votes'})
    df_grouped = df_grouped.reset_index()

    st.write("##")
    st.write("##")
    # --- PLOT BAR CHART
    bar_chart = px.bar(df_grouped,
                       x='Rating',
                       y='Votes',
                       text='Votes',
                       color_discrete_sequence = ['#426ecb']*len(df_grouped),
                       template= 'plotly_white')
    st.plotly_chart(bar_chart)

    # --- DISPLAY IMAGE & DATAFRAME
    col1, col2 = st.columns(2)
    image = Image.open('images/survey.jpeg')
    print(image)
    col1.image(image,
            use_column_width=True)
    col2.dataframe(df[mask])

    # --- PLOT PIE CHART
    pie_chart = px.pie(df_participants,
                    title='Total No. of Participants',
                    values='Participants',
                    names='Departments')

    st.plotly_chart(pie_chart)
    with st.container():
        st.write("---")
        st.write("##")
    
    
if selected == "About":
    with st.container():
        st.write("---")
        st.write("##")
    st.title(f"{selected}")
    with st.container():
        st.write("---")
        st.write("##")

    
    st.write('''
            This is application for visalization of user reviews(ratings)
            from different department.
            Based on the ratings one can understand various scope of this application.
            The ratings are shown to show a view of reviews based on age and department.
            ''')
    with st.container():
        st.write("---")
        st.write("##")
    
    
    
if selected == "Contact":
    with st.container():
        st.write("---")
        st.write("##")
        st.header("Write us a message")
        st.write("---")
        st.write("##")

        contact_form = """
        <form action="https://formsubmit.co/dubeyaditya282@gmail.com" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Your name" required>
            <input type="email" name="email" placeholder="Your email" required>
            <textarea name="message" placeholder="Message for us" required></textarea>
            <button type="submit">Send</button>
        </form>
        """
        left_column, right_column = st.columns(2)
        with left_column:
            st.markdown(contact_form, unsafe_allow_html=True)
        with right_column:
            st.empty()
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    with st.container():
        st.write("---")
        st.write("##")


    local_css("style/style.css")

