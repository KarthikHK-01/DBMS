import streamlit as st
import mysql.connector
from mysql.connector import Error

connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "05112004!@#$",
    database = "paws_database"
)

mycursor = connection.cursor()
print("Connection Established.")

# CRUD Functions
def create_owner(connection, name, address, contact, email, aadhar):
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (name, address, contact_number, email, aadhar_no) VALUES (%s, %s, %s, %s, %s)",
                       (name, address, contact, email, aadhar))
        connection.commit()
        st.success("Owner added successfully!")
    except Error as e:
        st.error(f"Error: {e}")

def read_users(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    except Error as e:
        st.error(f"Error: {e}")
        return []

def update_owner(connection, owner_id, name, address, contact, email, aadhar):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET name=%s, address=%s, contact_number=%s, email=%s, aadhar_no=%s WHERE owner_id=%s",
                       (name, address, contact, email, aadhar, owner_id))
        connection.commit()
        st.success("Owner updated successfully!")
    except Error as e:
        st.error(f"Error: {e}")

def delete_owner(connection, owner_id):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE owner_id=%s", (owner_id,))
        connection.commit()
        st.success("Owner deleted successfully!")
    except Error as e:
        st.error(f"Error: {e}")

# Streamlit UI for CRUD Operations
st.title("Pet Authentication and Welfare System")

menu = st.sidebar.selectbox("Select Operation", ["Add Owner", "View users", "Update Owner", "Delete Owner"])


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

    elif menu == "View users":
        st.subheader("View All users")
        users = read_users(connection)
        for owner in users:
            st.write(f"ID: {owner[0]}, Name: {owner[1]}, Address: {owner[2]}, Contact: {owner[3]}, Email: {owner[4]}, Aadhar: {owner[5]}")

    elif menu == "Update Owner":
        st.subheader("Update Owner Information")
        users = read_users(connection)
        owner_dict = {f"{owner[1]} (ID: {owner[0]})": owner[0] for owner in users}
        selected_owner = st.selectbox("Select Owner", list(owner_dict.keys()))
        owner_id = owner_dict[selected_owner]

        owner_info = next(owner for owner in users if owner[0] == owner_id)
        name = st.text_input("Name", value=owner_info[1])
        address = st.text_input("Address", value=owner_info[2])
        contact = st.text_input("Contact Number", value=owner_info[3])
        email = st.text_input("Email", value=owner_info[4])
        aadhar = st.text_input("Aadhar Number", value=owner_info[5])

        if st.button("Update Owner"):
            update_owner(connection, owner_id, name, address, contact, email, aadhar)

    elif menu == "Delete Owner":
        st.subheader("Delete an Owner")
        users = read_users(connection)
        owner_dict = {f"{owner[1]} (ID: {owner[0]})": owner[0] for owner in users}
        selected_owner = st.selectbox("Select Owner to Delete", list(owner_dict.keys()))
        owner_id = owner_dict[selected_owner]

        if st.button("Delete Owner"):
            delete_owner(connection, owner_id)

    # Close the connection after operations are complete
    connection.close()
else:
    st.error("Unable to connect to the database.")
