import streamlit as st
import mysql.connector
from mysql.connector import Error
from datetime import date

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

# Function to check login credentials and user role
def login_user(connection, email, password):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, user_role FROM users WHERE email = %s AND passwords = %s", (email, password))
        user = cursor.fetchone()
        if user:
            st.session_state.user_id = user[0]
            st.session_state.user_name = user[1]
            st.session_state.user_role = user[2]
            st.session_state.logged_in = True
            st.session_state.selected_pet_id = None  # Reset pet ID on login
            st.success("Logged in successfully!")
        else:
            st.error("Invalid email or password.")
    except Error as e:
        st.error(f"Error: {e}")

# Function to fetch pets associated with the user
def get_user_pets(connection, owner_id):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM pets WHERE owner_id = %s", (owner_id,))
        pets = cursor.fetchall()
        return pets
    except Error as e:
        st.error(f"Error: {e}")
        return []

# Function to fetch detailed information for a specific pet
def get_pet_details(connection, pet_id):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT pets.name, pets.species, pets.breed, pets.date_of_birth, pets.color, 
                   veterinarians.name AS vet_name, veterinarians.contact_number AS vet_contact
            FROM pets
            LEFT JOIN veterinarians ON pets.vet_id = veterinarians.id
            WHERE pets.id = %s
        """, (pet_id,))
        pet_details = cursor.fetchone()

        # Calculate pet age
        if pet_details and pet_details["date_of_birth"]:
            dob = pet_details["date_of_birth"]
            age = (date.today() - dob).days // 365
            pet_details["age"] = age

        return pet_details
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Function to fetch users (for admin)
def get_all_users(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, email, user_role FROM users")
        users = cursor.fetchall()
        return users
    except Error as e:
        st.error(f"Error: {e}")
        return []

# Function to delete a user (for admin)
def delete_user(connection, user_id):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        connection.commit()
        st.success("User deleted successfully!")
    except Error as e:
        st.error(f"Error: {e}")

# Function to delete a pet (for admin)
def delete_pet(connection, pet_id):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM pets WHERE id = %s", (pet_id,))
        connection.commit()
        st.success("Pet deleted successfully!")
    except Error as e:
        st.error(f"Error: {e}")

# Initialize session state for login if it doesn't exist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'selected_pet_id' not in st.session_state:
    st.session_state.selected_pet_id = None

# Logout functionality
def logout():
    # Clear all relevant session state variables for logout
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_name = None
    st.session_state.user_role = None
    st.session_state.selected_pet_id = None

# Main app logic
if st.session_state.logged_in:
    st.set_page_config(page_title="PAWS - Home", layout="wide")

    # Sidebar with navigation options
    sidebar_options = ["Home", "Pets", "About Us"]
    if st.session_state.user_role == "admin":
        sidebar_options.insert(2, "Admin Panel")  # Insert Admin Panel only for admins

    # Display sidebar options and logout button
    selected_option = st.sidebar.radio("Navigate", sidebar_options)
    st.sidebar.button("Logout", on_click=logout)  # Logout button always visible

    connection = create_connection()
    if connection:
        if selected_option == "Home":
            st.title(f"Welcome to PAWS, {st.session_state.user_name}!")
            st.write("PAWS helps you manage your pets' medical history and more.")

        elif selected_option == "Pets":
            # Pets overview and details page
            st.title("Your Pets")
            pets = get_user_pets(connection, st.session_state.user_id)
            if pets:
                for pet in pets:
                    pet_id, pet_name = pet
                    if st.button(pet_name):
                        st.session_state.selected_pet_id = pet_id

            # Detailed view for a specific pet
            if st.session_state.selected_pet_id:
                pet_id = st.session_state.selected_pet_id
                pet_details = get_pet_details(connection, pet_id)

                if pet_details:
                    st.header(f"Details for {pet_details['name']}")
                    st.write(f"**Species**: {pet_details['species']}")
                    st.write(f"**Breed**: {pet_details['breed']}")
                    st.write(f"**Age**: {pet_details.get('age', 'N/A')} years")
                    st.write(f"**Color**: {pet_details['color']}")
                    st.write(f"**Date of Birth**: {pet_details['date_of_birth']}")
                    st.write(f"**Veterinarian**: {pet_details['vet_name']}")
                    st.write(f"**Vet Contact**: {pet_details['vet_contact']}")

                    # Back button to return to pets list
                    if st.button("Back to Pets List"):
                        st.session_state.selected_pet_id = None

        elif selected_option == "Admin Panel" and st.session_state.user_role == "admin":
            # Admin Panel content with CRUD options for users and pets
            st.title("Admin Panel")
            admin_action = st.selectbox("Choose an action", ["View All Users", "Add User", "Delete User", "Delete Pet"])

            if admin_action == "View All Users":
                users = get_all_users(connection)
                if users:
                    for user in users:
                        st.write(f"**ID**: {user[0]}, **Name**: {user[1]}, **Email**: {user[2]}, **Role**: {user[3]}")
                else:
                    st.write("No users found.")

            elif admin_action == "Add User":
                st.subheader("Add a New User")
                name = st.text_input("Name")
                address = st.text_input("Address")
                contact = st.text_input("Contact Number")
                email = st.text_input("Email")
                aadhar = st.text_input("Aadhar Number")
                password = st.text_input("Password", type="password")
                role = st.selectbox("Role", ["standard", "admin"])
                
                if st.button("Create User"):
                    create_user(connection, name, address, contact, email, aadhar, password, role)

            elif admin_action == "Delete User":
                st.subheader("Delete a User")
                user_id = st.number_input("Enter User ID to delete", min_value=1, step=1)
                if st.button("Delete User"):
                    delete_user(connection, user_id)

            elif admin_action == "Delete Pet":
                st.subheader("Delete a Pet")
                pet_id = st.number_input("Enter Pet ID to delete", min_value=1, step=1)
                if st.button("Delete Pet"):
                    delete_pet(connection, pet_id)

        elif selected_option == "About Us":
            st.title("About PAWS")
            st.write("PAWS is a comprehensive pet management solution.")

        connection.close()
    else:
        st.error("Unable to connect to the database.")
else:
    # Display Login and Sign-Up Page if not logged in
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
            role = st.selectbox("Role", ["standard", "admin"])

            if st.button("Sign Up"):
                create_user(connection, name, address, contact, email, aadhar, password, role)
        
        elif choice == "Login":
            st.subheader("Log In to Your Account")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            
            if st.button("Login"):
                login_user(connection, email, password)

        connection.close()
    else:
        st.error("Unable to connect to the database.")
