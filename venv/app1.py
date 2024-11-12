import streamlit as st
import mysql.connector
from mysql.connector import Error

# Database connection function
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',       # Replace with your MySQL host
            database='paws_database',  # Replace with your database name
            user='root',            # Replace with your MySQL username
            password='05112004!@#$' # Replace with your MySQL password
        )
        return connection
    except Error as e:
        st.error(f"Error: {e}")
        return None

def create_user(connection, name, address, contact, email, aadhar, password, role="standard"):
    try:
        cursor = connection.cursor()
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (name, address, contact_number, email, aadhar_no, passwords) VALUES (%s, %s, %s, %s, %s, %s)",
                       (name, address, contact, email, aadhar, hashed_password))
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
            return user
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
        return None

st.title("Pet Authentication and Welfare System")
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
