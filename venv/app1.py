import streamlit as st
import mysql.connector
from mysql.connector import Error
import hashlib

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

# Function to hash passwords for secure storage
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to create a new user (Sign-Up)
def create_user(connection, name, address, contact, email, aadhar, password):
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
        hashed_password = hash_password(password)
        cursor.execute("SELECT * FROM users WHERE email = %s AND passwords = %s", (email, hashed_password))
        user = cursor.fetchone()
        if user:
            st.success("Logged in successfully!")
            return user
        else:
            st.error("Invalid email or password.")
            return None
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Main app
st.title("Pet Authentication and Welfare System")

# Display login and sign-up options
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
            user = login_user(connection, email, password)
            if user:
                st.write(f"Welcome, {user[1]}!")  # Display the user's name after login

    # Close connection after operations
    connection.close()
else:
    st.error("Unable to connect to the database.")
