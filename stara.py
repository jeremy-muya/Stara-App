import streamlit as st
import pandas as pd
from datetime import datetime

# Dummy user
users = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'user1': {'password': 'user123', 'role': 'user'},
    'user2': {'password': 'user123', 'role': 'user'},
}

# Initialize data storage
inventory_data = pd.DataFrame(columns=['Date', 'Day', 'Booking_Id', 'Amount Paid (Ksh)', 'Expense', 'Expense Reason'])

# Function to calculate Net Total
def calculate_net_total():
    net_total = inventory_data.groupby('Day')['Amount Paid (Ksh)'].sum() - inventory_data.groupby('Day')['Expense'].sum()
    return net_total

# Streamlit app
def main():
    st.title("Stara Management System")

    # User authentication
    username = st.sidebar.text_input("Username:")
    password = st.sidebar.text_input("Password:", type="password")
    
    if st.sidebar.button("Login"):
        if username in users and users[username]['password'] == password:
            st.success(f"Logged in as {username} ({users[username]['role']})")
            main_dashboard(users[username]['role'])
        else:
            st.error("Invalid username or password")

# Main dashboard based on user role
def main_dashboard(role):
    st.sidebar.header("Navigation")
    if role == 'admin':
        st.sidebar.subheader("Admin Options")
        selected_option = st.sidebar.radio("Select Option", ['Add Entry', 'View Data', 'Download Data'])
        if selected_option == 'Add Entry':
            add_entry()
        elif selected_option == 'View Data':
            view_data()
        elif selected_option == 'Download Data':
            download_data()
    else:
        st.sidebar.subheader("User Options")
        selected_option = st.sidebar.radio("Select Option", ['Add Entry', 'View Data'])
        if selected_option == 'Add Entry':
            add_entry()
        elif selected_option == 'View Data':
            view_data()

# Function to add an entry to the inventory
def add_entry():
    st.header("Add Entry")
    
    date = st.date_input("Date", datetime.today())
    day = st.text_input("Day")
    booking_id = st.text_input("Booking ID")
    amount_paid = st.number_input("Amount Paid (Ksh)", min_value=0.0)
    expense = st.number_input("Expense", min_value=0.0)
    expense_reason = st.text_input("Expense Reason")

    if st.button("Add Entry"):
        new_entry = pd.DataFrame({
            'Date': [date],
            'Day': [day],
            'Booking_Id': [booking_id],
            'Amount Paid (Ksh)': [amount_paid],
            'Expense': [expense],
            'Expense Reason': [expense_reason],
        })
        global inventory_data
        inventory_data = pd.concat([inventory_data, new_entry], ignore_index=True)
        st.success("Entry added successfully")

# Function to view data in the inventory
def view_data():
    st.header("View Data")
    st.dataframe(inventory_data)

# Function to download data as an Excel file
def download_data():
    st.header("Download Data")
    if st.button("Download Data as Excel"):
        file_name = "inventory_data.xlsx"
        inventory_data.to_excel(file_name, index=False)
        st.success(f"Data downloaded successfully as {file_name}")

if __name__ == "__main__":
    main()
