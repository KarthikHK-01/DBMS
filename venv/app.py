import streamlit as st

# Dummy data for the logged-in user and pets (replace this with your database connection)
logged_in_user = "John Doe"
pets_data = {
    "Fluffy": {
        "Medical History": "No significant issues",
        "Veterinary Doctor": "Dr. Smith",
        "Vaccination Details": "Rabies, DHPP",
        "Insurance": "Covered until 2025"
    },
    "Bella": {
        "Medical History": "Recent surgery",
        "Veterinary Doctor": "Dr. Jones",
        "Vaccination Details": "Rabies, DHPP, Bordetella",
        "Insurance": "Covered until 2026"
    }
}


st.set_page_config(page_title="Pet Authentication & Welfare System", layout="wide")


st.markdown(
    f"""
    <style>
        /* Change background color to white */
        .css-18e3th9 {{
            background-color: #ffffff;
        }}

        /* Navbar styling */
        .navbar {{
            display: flex;
            justify-content: space-between;
            background-color: #f9f9f9;
            padding: 10px;
            border-bottom: 1px solid #e0e0e0;
        }}
        .navbar-item {{
            padding: 0 15px;
            font-weight: bold;
            color: #333;
            text-decoration: none;
        }}
        .navbar-item:hover {{
            color: #0078D4;
        }}
        
        /* Dropdown styling */
        .dropdown {{
            position: relative;
            display: inline-block;
        }}
        .dropdown-content {{
            display: none;
            position: absolute;
            right: 0;
            background-color: #f9f9f9;
            min-width: 100px;
            box-shadow: 0px 8px 16px rgba(0,0,0,0.2);
            z-index: 1;
            border-radius: 5px;
        }}
        .dropdown-content a {{
            color: black;
            padding: 8px 12px;
            text-decoration: none;
            display: block;
        }}
        .dropdown-content a:hover {{
            background-color: #f1f1f1;
        }}
        .dropdown:hover .dropdown-content {{
            display: block;
        }}
    </style>
    <div class="navbar">
        <div>
            <a class="navbar-item" href="#home">Home</a>
            <a class="navbar-item" href="#pets">Pets</a>
        </div>
        <div class="dropdown">
            <span class="navbar-item">{logged_in_user}</span>
            <div class="dropdown-content">
                <a href="#profile">Profile</a>
                <a href="#logout">Logout</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True
)

# Page content based on selected page
page = st.sidebar.radio("Navigation", ["Home", "Pets"])

if page == "Home":
    st.title("Welcome to the Pet Authentication & Welfare System!")
    st.write("This system helps pet owners manage information about their pets, including medical history, vaccinations, and insurance details.")

elif page == "Pets":
    st.title("Your Pets")
    selected_pet = st.selectbox("Select a pet to view details", list(pets_data.keys()))

    if selected_pet:
        pet_info = pets_data[selected_pet]
        st.subheader(f"{selected_pet}'s Details")
        st.write("### Medical History")
        st.write(pet_info["Medical History"])
        
        st.write("### Veterinary Doctor")
        st.write(pet_info["Veterinary Doctor"])
        
        st.write("### Vaccination Details")
        st.write(pet_info["Vaccination Details"])
        
        st.write("### Insurance")
        st.write(pet_info["Insurance"])

# Hide Streamlit footer for a cleaner look
st.markdown(
    """
    <style>
        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)
