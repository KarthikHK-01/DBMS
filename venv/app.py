import streamlit as st
import mysql.connector
from mysql.connector import Error

# Database connection function
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='l27.0.0.1:3306',       # Replace with your MySQL host
            database='paws_database',  # Replace with your database name
            user='root',            # Replace with your MySQL username
            password='05112004!@#$' # Replace with your MySQL password
        )
        return connection
    except Error as e:
        st.error(f"Error: {e}")
        return None

# CRUD Functions
def create_owner(connection, name, address, contact, email, aadhar):
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO owners (name, address, contact_number, email, aadhar_number) VALUES (%s, %s, %s, %s, %s)",
                       (name, address, contact, email, aadhar))
        connection.commit()
        st.success("Owner added successfully!")
    except Error as e:
        st.error(f"Error: {e}")

def read_owners(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM owners")
        return cursor.fetchall()
    except Error as e:
        st.error(f"Error: {e}")
        return []

def update_owner(connection, owner_id, name, address, contact, email, aadhar):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE owners SET name=%s, address=%s, contact_number=%s, email=%s, aadhar_number=%s WHERE owner_id=%s",
                       (name, address, contact, email, aadhar, owner_id))
        connection.commit()
        st.success("Owner updated successfully!")
    except Error as e:
        st.error(f"Error: {e}")

def delete_owner(connection, owner_id):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM owners WHERE owner_id=%s", (owner_id,))
        connection.commit()
        st.success("Owner deleted successfully!")
    except Error as e:
        st.error(f"Error: {e}")

# Streamlit UI for CRUD Operations
st.title("Pet Authentication and Welfare System")

menu = st.sidebar.selectbox("Select Operation", ["Add Owner", "View Owners", "Update Owner", "Delete Owner"])

connection = create_connection()

if connection:
    if menu == "Add Owner":
        st.subheader("Add a New Owner")
        name = st.text_input("Name")
        address = st.text_input("Address")
        contact = st.text_input("Contact Number")
        email = st.text_input("Email")
        aadhar = st.text_input("Aadhar Number")
        if st.button("Add Owner"):
            create_owner(connection, name, address, contact, email, aadhar)

    elif menu == "View Owners":
        st.subheader("View All Owners")
        owners = read_owners(connection)
        for owner in owners:
            st.write(f"ID: {owner[0]}, Name: {owner[1]}, Address: {owner[2]}, Contact: {owner[3]}, Email: {owner[4]}, Aadhar: {owner[5]}")

    elif menu == "Update Owner":
        st.subheader("Update Owner Information")
        owners = read_owners(connection)
        owner_dict = {f"{owner[1]} (ID: {owner[0]})": owner[0] for owner in owners}
        selected_owner = st.selectbox("Select Owner", list(owner_dict.keys()))
        owner_id = owner_dict[selected_owner]

        owner_info = next(owner for owner in owners if owner[0] == owner_id)
        name = st.text_input("Name", value=owner_info[1])
        address = st.text_input("Address", value=owner_info[2])
        contact = st.text_input("Contact Number", value=owner_info[3])
        email = st.text_input("Email", value=owner_info[4])
        aadhar = st.text_input("Aadhar Number", value=owner_info[5])

        if st.button("Update Owner"):
            update_owner(connection, owner_id, name, address, contact, email, aadhar)

    elif menu == "Delete Owner":
        st.subheader("Delete an Owner")
        owners = read_owners(connection)
        owner_dict = {f"{owner[1]} (ID: {owner[0]})": owner[0] for owner in owners}
        selected_owner = st.selectbox("Select Owner to Delete", list(owner_dict.keys()))
        owner_id = owner_dict[selected_owner]

        if st.button("Delete Owner"):
            delete_owner(connection, owner_id)

    # Close the connection after operations are complete
    connection.close()
else:
    st.error("Unable to connect to the database.")
