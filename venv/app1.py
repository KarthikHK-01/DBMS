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

# Function to fetch a user's details by ID
def get_user_by_id(connection, user_id):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return cursor.fetchone()
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Function to fetch all users
def get_all_users(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, email, user_role FROM users")
        return cursor.fetchall()
    except Error as e:
        st.error(f"Error: {e}")
        return []

# Function to verify admin password
def verify_admin_password(connection, admin_id, password):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT passwords FROM users WHERE id = %s AND user_role = 'admin'", (admin_id,))
        result = cursor.fetchone()
        return result and result[0] == password
    except Error as e:
        st.error(f"Error: {e}")
        return False

# Function to update user details
def update_user(connection, user_id, name, address, contact, email, aadhar, password, role):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE users 
            SET name = %s, address = %s, contact_number = %s, email = %s, aadhar_no = %s, passwords = %s, user_role = %s 
            WHERE id = %s
        """, (name, address, contact, email, aadhar, password, role, user_id))
        connection.commit()
        st.success("User updated successfully!")
    except Error as e:
        st.error(f"Error: {e}")

# Function to fetch pets for a specific user
def get_user_pets(connection, owner_id):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM pets WHERE owner_id = %s", (owner_id,))
        return cursor.fetchall()
    except Error as e:
        st.error(f"Error: {e}")
        return []

# Function to fetch detailed pet information
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
        pet = cursor.fetchone()

        # Add pet's age
        if pet and pet["date_of_birth"]:
            dob = pet["date_of_birth"]
            age = (date.today() - dob).days // 365
            pet["age"] = age

        return pet
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Function to add a pet
def add_pet(connection, name, species, breed, gender, date_of_birth, color, reg_date, owner_id, vet_id):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO pets (name, species, breed, gender, date_of_birth, color, reg_date, owner_id, vet_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, species, breed, gender, date_of_birth, color, reg_date, owner_id, vet_id))
        connection.commit()
        st.success("Pet added successfully!")
    except Error as e:
        st.error(f"Error: {e}")

# Function to delete a pet
def delete_pet(connection, pet_id):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM pets WHERE id = %s", (pet_id,))
        connection.commit()
        st.success("Pet deleted successfully!")
    except Error as e:
        st.error(f"Error: {e}")

# Function to handle Admin Panel actions
def admin_panel(connection):
    st.title("Admin Panel")
    action = st.selectbox("Choose an action", ["View All Users", "Add User", "Update User", "Delete User", "Add Pet", "Delete Pet"])

    if action == "View All Users":
        users = get_all_users(connection)
        if users:
            for user in users:
                st.write(f"**ID**: {user[0]}, **Name**: {user[1]}, **Email**: {user[2]}, **Role**: {user[3]}")
        else:
            st.warning("No users found.")

    elif action == "Add User":
        name = st.text_input("Name")
        address = st.text_input("Address")
        contact = st.text_input("Contact Number")
        email = st.text_input("Email")
        aadhar = st.text_input("Aadhar Number")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["standard", "admin"])
        if st.button("Create User"):
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO users (name, address, contact_number, email, aadhar_no, passwords, user_role)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (name, address, contact, email, aadhar, password, role))
                connection.commit()
                st.success("User added successfully!")
            except Error as e:
                st.error(f"Error: {e}")

    elif action == "Update User":
        user_id = st.number_input("Enter User ID", min_value=1, step=1)
        if st.button("Fetch User Details"):
            user = get_user_by_id(connection, user_id)
            if user:
                name = st.text_input("Name", user["name"])
                address = st.text_input("Address", user["address"])
                contact = st.text_input("Contact Number", user["contact_number"])
                email = st.text_input("Email", user["email"])
                aadhar = st.text_input("Aadhar Number", user["aadhar_no"])
                password = st.text_input("Password", user["passwords"])
                role = st.selectbox("Role", ["standard", "admin"], index=0 if user["user_role"] == "standard" else 1)

                admin_password = None
                if role == "admin":
                    admin_password = st.text_input("Re-enter your admin password to confirm", type="password")

                if st.button("Update User"):
                    if role == "admin" and not verify_admin_password(connection, st.session_state.user_id, admin_password):
                        st.error("Authentication failed. Incorrect admin password.")
                    else:
                        update_user(connection, user_id, name, address, contact, email, aadhar, password, role)

    elif action == "Delete User":
        user_id = st.number_input("Enter User ID to delete", min_value=1, step=1)
        if st.button("Delete User"):
            try:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                connection.commit()
                st.success("User deleted successfully!")
            except Error as e:
                st.error(f"Error: {e}")

    elif action == "Add Pet":
        name = st.text_input("Pet Name")
        species = st.text_input("Species")
        breed = st.text_input("Breed")
        gender = st.text_input("Gender")
        date_of_birth = st.date_input("Date of Birth")
        color = st.text_input("Color")
        reg_date = st.date_input("Registration Date")
        owner_id = st.number_input("Owner ID", min_value=1, step=1)
        vet_id = st.number_input("Veterinarian ID", min_value=1, step=1)
        if st.button("Add Pet"):
            add_pet(connection, name, species, breed, gender, date_of_birth, color, reg_date, owner_id, vet_id)

    elif action == "Delete Pet":
        pet_id = st.number_input("Enter Pet ID to delete", min_value=1, step=1)
        if st.button("Delete Pet"):
            delete_pet(connection, pet_id)

# Main app logic
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.set_page_config(page_title="PAWS - Admin Panel", layout="wide")
    connection = create_connection()
    if connection:
        selected_option = st.sidebar.radio("Navigate", ["Home", "Pets", "Admin Panel", "About Us"])
        st.sidebar.button("Logout", on_click=lambda: st.session_state.update({'logged_in': False}))

        if selected_option == "Home":
            st.title(f"Welcome, {st.session_state.user_name}!")
            st.write("Manage your pets and user data efficiently.")
        
        elif selected_option == "Pets":
            pets = get_user_pets(connection, st.session_state.user_id)
            for pet in pets:
                if st.button(pet[1]):
                    pet_details = get_pet_details(connection, pet[0])
                    if pet_details:
                        st.write(f"**Name**: {pet_details['name']}")
                        st.write(f"**Species**: {pet_details['species']}")
                        st.write(f"**Breed**: {pet_details['breed']}")
                        st.write(f"**Age**: {pet_details['age']} years")
                        st.write(f"**Color**: {pet_details['color']}")
                        st.write(f"**Veterinarian**: {pet_details['vet_name']}")
                        st.write(f"**Vet Contact**: {pet_details['vet_contact']}")

        elif selected_option == "Admin Panel":
            if st.session_state.user_role == "admin":
                admin_panel(connection)
            else:
                st.error("Access denied. Only admins can view this page.")

        elif selected_option == "About Us":
            st.title("About PAWS")
            st.write("PAWS is a comprehensive pet management solution.")

        connection.close()
else:
    st.title("Pet Authentication and Welfare System")
    choice = st.radio("Select Option", ["Login", "Sign Up"])
    connection = create_connection()
    if connection:
        if choice == "Login":
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                cursor = connection.cursor()
                cursor.execute("SELECT id, name, user_role FROM users WHERE email = %s AND passwords = %s", (email, password))
                user = cursor.fetchone()
                if user:
                    st.session_state.user_id = user[0]
                    st.session_state.user_name = user[1]
                    st.session_state.user_role = user[2]
                    st.session_state.logged_in = True
                    st.success("Logged in successfully!")
                else:
                    st.error("Invalid email or password.")

        elif choice == "Sign Up":
            name = st.text_input("Name")
            address = st.text_input("Address")
            contact = st.text_input("Contact Number")
            email = st.text_input("Email")
            aadhar = st.text_input("Aadhar Number")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Role", ["standard", "admin"])
            if st.button("Sign Up"):
                try:
                    cursor = connection.cursor()
                    cursor.execute("""
                        INSERT INTO users (name, address, contact_number, email, aadhar_no, passwords, user_role)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (name, address, contact, email, aadhar, password, role))
                    connection.commit()
                    st.success("Account created successfully!")
                except Error as e:
                    st.error(f"Error: {e}")
        connection.close()
