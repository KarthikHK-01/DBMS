import streamlit as st
import mysql.connector
from mysql.connector import Error
import hashlib

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

def login_user(connection, email, password):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND passwords = %s", (email, password))
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
            user = login_user(connection, email, password)
            if user:
                st.write(f"Welcome, {user[1]}!")

    connection.close()
else:
    st.error("Unable to connect to the database.")
