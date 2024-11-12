import streamlit as st
import mysql.connector
from mysql.connector import Error

# Database connection function
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',       
            database='paws_schema', 
            user='root',            
            password='05112004!@#$' 
        )
        return connection
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Function to create a new user (Sign-Up)
def create_user(connection, name, address, contact, email, aadhar, password, role="standard"):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (name, address, contact_number, email, aadhar_no, passwords, user_role) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (name, address, contact, email, aadhar, password, role)
        )
        connection.commit()
        st.success("Account created successfully!")
    except Error as e:
        st.error(f"Error: {e}")

# Function to check login credentials
def login_user(connection, email, password):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM users WHERE email = %s AND passwords = %s", (email, password))
        user = cursor.fetchone()
        if user:
            st.session_state.user_id = user[0]
            st.session_state.user_name = user[1]
            st.session_state.logged_in = True  # Set login state to True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid email or password.")
    except Error as e:
        st.error(f"Error: {e}")

# Function to fetch pets associated with the user
def get_user_pets(connection, owner_id):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT name, species, breed, date_of_birth, color FROM pets WHERE owner_id = %s", (owner_id,))
        pets = cursor.fetchall()
        return pets
    except Error as e:
        st.error(f"Error: {e}")
        return []

# Initialize session state for login if it doesn't exist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Main app logic
if st.session_state.logged_in:
    # Home Page
    st.set_page_config(page_title="PAWS - Home", layout="wide")
    st.sidebar.title("Navigation")
    selected_option = st.sidebar.radio("Go to", ["Home", "Pets", "About Us"])

    connection = create_connection()
    if connection:
        if selected_option == "Home":
            st.title(f"Welcome to PAWS, {st.session_state.user_name}!")
            st.write("PAWS (Pet Authentication and Welfare System) is your companion in managing your pets' medical history, vaccinations, and other essential information.")
            st.write("Our mission is to ensure pets get the care they need, while making it easy for pet owners to manage their beloved pets' records.")

        elif selected_option == "Pets":
            st.title("Your Pets")
            pets = get_user_pets(connection, st.session_state.user_id)
            
            if pets:
                for pet in pets:
                    st.subheader(pet[0])  # Pet Name
                    st.write(f"**Species**: {pet[1]}")
                    st.write(f"**Breed**: {pet[2]}")
                    st.write(f"**Date of Birth**: {pet[3]}")
                    st.write(f"**Color**: {pet[4]}")
                    st.write("---")
            else:
                st.write("No pets found for this user.")

        elif selected_option == "About Us":
            st.title("About PAWS")
            st.write("""
                **Pet Authentication and Welfare System (PAWS)** is a comprehensive solution designed to manage 
                pet data efficiently. With PAWS, pet owners can track their pets' medical history, vaccinations, 
                and insurance policies, all in one place. Our mission is to ensure pets receive the care they deserve 
                while making it easier for pet owners to manage important details about their furry friends.
            """)

        connection.close()
    else:
        st.error("Unable to connect to the database.")

else:
    # Login/Sign-Up Page
    st.title("Welcome to PAWS")
    choice = st.radio("Select Option", ["Login", "Sign Up"])

    connection = create_connection()
    if connection:
        if choice == "Sign Up":
            st.subheader("Create a New Account")
            name = st.text_input("Name")
            address = st.text_input("Address")
            contact = st.text_input("Contact Number")
            email = st.text_input("Email")
            aadhar = st.text_input("Aadhar Number")
            password = st.text_input("Password", type="password")
            
            if st.button("Sign Up"):
                create_user(connection, name, address, contact, email, aadhar, password)
        
        elif choice == "Login":
            st.subheader("Log In to Your Account")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            
            if st.button("Login"):
                login_user(connection, email, password)

        connection.close()
    else:
        st.error("Unable to connect to the database.")
