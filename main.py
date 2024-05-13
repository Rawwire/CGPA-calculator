import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="CGPA calculator", page_icon="star", layout="wide")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)

with st.sidebar:
    selectedmain=option_menu(
        menu_title=" Main_menu",
        options=["Home", "Contact Us"]
    )
if selectedmain == "Home":

    def display_centered_title(text, level=1, font_size=38):
        style = f"text-align: center; font-size: {font_size}px; border-radius: 5px;"
        st.markdown(f"<h{level} style='{style}'>{text}</h{level}>", unsafe_allow_html=True)

    display_centered_title("CGPA/GPA Calculator for Anna University (R-2021)", level=2, font_size=48)
    st.write(" ")
    des= "The CGPA/GPA Calculator for Anna University (R-2021) is a handy tool designed to help students calculate their Cumulative Grade Point Average (CGPA) or Grade Point Average (GPA) for the Anna University curriculum under the Regulation 2021. This calculator allows students to input their grades and credits for each subject or semester and obtain their CGPA or GPA with ease. It simplifies the process of calculating academic performance, aiding students in monitoring their progress throughout their academic journey. Whether you're planning your course load or aiming for academic excellence, this calculator provides valuable insights into your academic achievements. Created By Raja Pandi S"
    def display_centered_des(text, level=1, font_size=20):
        style = f"text-align: center; font-size: {font_size}px; border-radius: 5px;"
        st.markdown(f"<h{level} style='{style}'>{text}</h{level}>", unsafe_allow_html=True)

    display_centered_des(des, level=2, font_size=16)
    st.write(" ")
    selected = option_menu(menu_title="Choose the following to be calculated",
                            options=["GPA", "CGPA"],
                            default_index=0,
                            menu_icon="cast",
                            orientation="horizontal")
    with st.container():
        if selected == "GPA":
            n = st.number_input("Choose the number of Subjects:", min_value=1, step=1)
            st.header("Choose the Credits and Grade for the Subjects")
            left,center,right = st.columns((2,1,2))
            credit = []
            grade = []
            gpa = 0
            for i in range(1, n + 1):
                with st.expander(f"Subject {i}"):
                    a = st.selectbox(f"Choose Credits for Subject {i}", options=["4","3","2","1"], key=f"credits_{i}")
                    b = st.selectbox(f"Choose Grade for Subject {i}", options=["O", "A+", "A", "B+", "B", "C"], key=f"grade_{i}")
                    credit.append(int(a))
                    grade.append({"O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5}.get(b))

            if st.button("Calculate"):
                for j in range(n):
                    gpa += grade[j] * credit[j]
                gpa /= sum(credit)
                st.success(f"GPA is {gpa:.2f}")
        if selected == "CGPA":
            temp = []
            cgpa=0
            n1 = st.number_input("Enter the number of Semesters", step=1, min_value=1)
            for k in range(1, n1 + 1):
                if k == 1:
                    z = st.number_input(f"Enter the {k}st Semester GPA:", key=f"gpa_{k}")
                    temp.append(z)
                elif k == 2:
                    z = st.number_input(f"Enter the {k}nd Semester GPA:", key=f"gpa_{k+10}")
                    temp.append(z)
                elif k == 3:
                    z = st.number_input(f"Enter the {k}rd Semester GPA:", key=f"gpa_{k+20}")
                    temp.append(z)
                else:
                    z = st.number_input(f"Enter the {k}th Semester GPA:", key=f"gpa_{k+30}")
                    temp.append(z)
            cgpa= sum(temp)/n1
            if st.button("Calculate"):
                st.success(f"CPGA is {cgpa:.2f}")
if selectedmain == "Contact Us":
    def display_centered_title(text, level=1, font_size=38):
        style = f"text-align: center; font-size: {font_size}px; border-radius: 5px;"
        st.markdown(f"<h{level} style='{style}'>{text}</h{level}>", unsafe_allow_html=True)

    display_centered_title("About Us", level=2, font_size=48)

    des=  """
    This CGPA/GPA Calculator for Anna University (R-2021) is a project created by Raja Pandi S and Priyadharshini.
    """
    def display_centered_des(text, level=1, font_size=20):
        style = f"text-align: center; font-size: {font_size}px; border-radius: 5px;"
        st.markdown(f"<h{level} style='{style}'>{text}</h{level}>", unsafe_allow_html=True)

    display_centered_des(des, level=2, font_size=16)


    st.write(" ")
    conleft,conright=st.columns((2,2))
    with conleft:
        st.header("Contact us:")
        st.write("Phone no :telephone_receiver: : +91-81240-10413")
        st.write("Email :email: : rajapandivnr1@gmail.com")
    with conright:
        st.header("Share your Thoughts :leaves: :")
        st.write("For any suggestions and improvements:")
        contact_form = """
        <form action="https://formsubmit.co/dinotech2004@gmail.com" method="POST">
            <input type="hidden" name= "_captcha" value="false">
            <input type="text" id="name" name="name" placeholder="Your name" required>
            <input type="email" id="email" name="email" placeholder="Your email" required>
            <textarea name="message" placeholder="Your message here"></textarea>
            <button id = "btn" type="submit">Send</button>
        </form>
        """
        st.markdown(contact_form, unsafe_allow_html=True)

        def local_css(file):
            with open(file) as f:
                st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)
        local_css("style.css")

            