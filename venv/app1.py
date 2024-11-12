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

# Function to check login credentials
def login_user(connection, email, password):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM users WHERE email = %s AND passwords = %s", (email, password))
        user = cursor.fetchone()
        if user:
            st.session_state.user_id = user[0]
            st.session_state.user_name = user[1]
            st.session_state.logged_in = True
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

# Function to fetch activity log for a specific pet
def get_pet_activity_log(connection, pet_id):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT activity_type, duration, activity_date 
            FROM pet_activity_log 
            WHERE pet_id = %s
            ORDER BY activity_date DESC
        """, (pet_id,))
        activity_log = cursor.fetchall()
        return activity_log
    except Error as e:
        st.error(f"Error: {e}")
        return []

# Initialize session state for login if it doesn't exist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'selected_pet_id' not in st.session_state:
    st.session_state.selected_pet_id = None

# Main app logic
if st.session_state.logged_in:
    st.set_page_config(page_title="PAWS - Home", layout="wide")
    selected_option = st.sidebar.radio("Navigate", ["Home", "Pets", "About Us"])

    connection = create_connection()
    if connection:
        if selected_option == "Home":
            st.title(f"Welcome to PAWS, {st.session_state.user_name}!")
            st.write("PAWS helps you manage your pets' medical history and more.")

        elif selected_option == "Pets":
            if st.session_state.selected_pet_id is None:
                # Pets overview page: list of pets with clickable names
                st.title("Your Pets")
                pets = get_user_pets(connection, st.session_state.user_id)
                if pets:
                    for pet in pets:
                        pet_id, pet_name = pet
                        if st.button(pet_name):
                            st.session_state.selected_pet_id = pet_id
                            st.query_params.update(selected_pet=pet_id)  # Update query parameters
            else:
                # Detailed view for a specific pet
                pet_id = st.session_state.selected_pet_id
                pet_details = get_pet_details(connection, pet_id)
                activity_log = get_pet_activity_log(connection, pet_id)

                if pet_details:
                    st.header(f"Details for {pet_details['name']}")
                    st.write(f"**Species**: {pet_details['species']}")
                    st.write(f"**Breed**: {pet_details['breed']}")
                    st.write(f"**Age**: {pet_details.get('age', 'N/A')} years")
                    st.write(f"**Color**: {pet_details['color']}")
                    st.write(f"**Date of Birth**: {pet_details['date_of_birth']}")
                    st.write(f"**Veterinarian**: {pet_details['vet_name']}")
                    st.write(f"**Vet Contact**: {pet_details['vet_contact']}")

                    # Display activity log
                    st.subheader("Activity Log")
                    if activity_log:
                        for activity in activity_log:
                            st.write(f"- **{activity['activity_type']}** on {activity['activity_date']} for {activity['duration']}")
                    else:
                        st.write("No activities recorded.")
                
                # Back button to return to pets list
                if st.button("Back to Pets List"):
                    st.session_state.selected_pet_id = None

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
