import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
from image import img

st.set_page_config(page_title="Snap Grade", page_icon="star", layout="wide")

# Hide the default Streamlit UI elements
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Sidebar menu
with st.sidebar:
    selectedmain = option_menu(
        menu_title="Main Menu",
        options=["Home", "Contact Us"]
    )

# Function to display centered title
def display_centered_title(text, level=1, font_size=38):
    style = f"text-align: center; font-size: {font_size}px; border-radius: 5px;"
    st.markdown(f"<h{level} style='{style}'>{text}</h{level}>", unsafe_allow_html=True)

# Function to display centered description
def display_centered_des(text, level=1, font_size=20):
    style = f"text-align: center; font-size: {font_size}px; border-radius: 5px;"
    st.markdown(f"<h{level} style='{style}'>{text}</h{level}>", unsafe_allow_html=True)

# Home page
if selectedmain == "Home":
    display_centered_title("SNAPGRADE", level=2, font_size=48)
    st.write(" ")
    description = """
    The CGPA/GPA Calculator for Anna University (R-2021) is a handy tool designed to help students calculate their Cumulative Grade Point Average (CGPA) or Grade Point Average (GPA) for the Anna University curriculum under the Regulation 2021. This calculator allows students to input their grades and credits for each subject or semester and obtain their CGPA or GPA with ease. It simplifies the process of calculating academic performance, aiding students in monitoring their progress throughout their academic journey. Whether you're planning your course load or aiming for academic excellence, this calculator provides valuable insights into your academic achievements.
    """
    display_centered_des(description, level=2, font_size=16)
    st.write(" ")

    # Horizontal menu for GPA, CGPA, and Upload Marksheet
    selected = option_menu(
        menu_title="Choose the following to be calculated",
        options=["GPA", "CGPA", "Upload Marksheet"],
        default_index=0,
        menu_icon="cast",
        orientation="horizontal"
    )

    # GPA calculation
    if selected == "GPA":
        n = st.number_input("Choose the number of Subjects:", min_value=1, step=1)
        st.header("Choose the Credits and Grade for the Subjects")
        left, center, right = st.columns((2, 1, 2))
        credit = []
        grade = []
        gpa = 0
        for i in range(1, n + 1):
            with st.expander(f"Subject {i}"):
                a = st.selectbox(f"Choose Credits for Subject {i}", options=["4", "3", "2", "1"], key=f"credits_{i}")
                b = st.selectbox(f"Choose Grade for Subject {i}", options=["O", "A+", "A", "B+", "B", "C"], key=f"grade_{i}")
                credit.append(int(a))
                grade.append({"O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5}.get(b))

        if st.button("Calculate"):
            for j in range(n):
                gpa += grade[j] * credit[j]
            gpa /= sum(credit)
            st.success(f"GPA is {gpa:.2f}")

    # CGPA calculation
    if selected == "CGPA":
        temp = []
        cgpa = 0
        n1 = st.number_input("Enter the number of Semesters", step=1, min_value=1)
        for k in range(1, n1 + 1):
            if k == 1:
                z = st.number_input(f"Enter the {k}st Semester GPA:", key=f"gpa_{k}")
            elif k == 2:
                z = st.number_input(f"Enter the {k}nd Semester GPA:", key=f"gpa_{k+10}")
            elif k == 3:
                z = st.number_input(f"Enter the {k}rd Semester GPA:", key=f"gpa_{k+20}")
            else:
                z = st.number_input(f"Enter the {k}th Semester GPA:", key=f"gpa_{k+30}")
            temp.append(z)
        cgpa = sum(temp) / n1
        if st.button("Calculate"):
            st.success(f"CGPA is {cgpa:.2f}")

    # Marksheet upload and processing
    if selected == "Upload Marksheet":
        uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption=uploaded_file.name, use_column_width=True)
            try:
                result = img(uploaded_file)
                cgpam=[]
                gpa1=0
                cred=[]
                for k in result[1]:
                    cred.append(int(k))
                for i in result[0]:
                    if "O" in i:
                        cgpam.append(10)
                    elif i == "A+":
                        cgpam.append(9)
                    elif "A" in i:
                        cgpam.append(8)
                    elif "B+" in i:
                        cgpam.append(7)
                    elif "B" in i:
                        cgpam.append(6)
                    elif "C" in i:
                        cgpam.append(5)
                    else:
                        st.warning("Unable to process the Image")
                st.write("Grades:",cgpam)
                st.write("Credits:",result[0])
                if st.button("Calculate"):
                    for j in range(len(cgpam)):
                        gpa1 += int(cgpam[j]) * int(cred[j])
                    gpa1 /= sum(cred)
                    st.success(f"GPA is {gpa1:.2f}")
            except Exception as e:
                st.error(f"Error processing the image: {e}")

# Contact Us page
if selectedmain == "Contact Us":
    display_centered_title("About Us", level=2, font_size=48)
    description = """
    This CGPA/GPA Calculator for Anna University (R-2021) is a project created by Raja Pandi S and Priyadharshini.
    """
    display_centered_des(description, level=2, font_size=16)

    st.write(" ")
    conleft, conright = st.columns((2, 2))
    with conleft:
        st.header("Contact us:")
        st.write("Phone no :telephone_receiver: : +91-81240-10413")
        st.write("Email :email: : rajapandivnr1@gmail.com")
    with conright:
        st.header("Share your Thoughts :leaves: :")
        st.write("For any suggestions and improvements:")
        contact_form = """
        <form action="https://formsubmit.co/dinotech2004@gmail.com" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" id="name" name="name" placeholder="Your name" required>
            <input type="email" id="email" name="email" placeholder="Your email" required>
            <textarea name="message" placeholder="Your message here"></textarea>
            <button id="btn" type="submit">Send</button>
        </form>
        """
        st.markdown(contact_form, unsafe_allow_html=True)

        def local_css(file_name):
            with open(file_name) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

        local_css("style.css")
