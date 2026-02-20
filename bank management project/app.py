import streamlit as st
import json
import random
import string
from pathlib import Path

class Bank:
    database = 'data.json'

    @staticmethod
    def load_data():
        if Path(Bank.database).exists():
            try:
                with open(Bank.database, 'r') as fs:
                    return json.load(fs)
            except json.JSONDecodeError:
                return []
        return []

    @staticmethod
    def save_data(data):
        with open(Bank.database, 'w') as fs:
            json.dump(data, fs, indent=4)

    @staticmethod
    def generate_account_no():
        alpha = random.choices(string.ascii_uppercase, k=3)
        num = random.choices(string.digits, k=3)
        id_list = alpha + num
        random.shuffle(id_list)
        return "".join(id_list)

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Digital Bank", page_icon="🏦")
st.title("🏦 Community Digital Bank")

data = Bank.load_data()

# Sidebar Navigation
menu = ["Home", "Create Account", "Deposit Money", "Withdraw Money", "View Details", "Update Profile", "Delete Account"]
choice = st.sidebar.selectbox("Menu", menu)

# --- Feature: Create Account ---
if choice == "Create Account":
    st.subheader("Open a New Account")
    with st.form("registration_form"):
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=0, max_value=120)
        email = st.text_input("Email ID")
        pin = st.text_input("Set 4-Digit PIN", type="password", max_chars=4)
        submit = st.form_submit_button("Register")

        if submit:
            if age < 18:
                st.error("Must be 18+ to open an account.")
            elif len(pin) != 4 or not pin.isdigit():
                st.error("PIN must be exactly 4 digits.")
            else:
                acc_no = Bank.generate_account_no()
                new_user = {
                    "name": name,
                    "age": age,
                    "email": email,
                    "pin": int(pin),
                    "accountNo": acc_no,
                    "balance": 0
                }
                data.append(new_user)
                Bank.save_data(data)
                st.success(f"Account Created! Your Account Number is: {acc_no}")

# --- Feature: Deposit ---
elif choice == "Deposit Money":
    st.subheader("Deposit Funds")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount to Deposit", min_value=1)

    if st.button("Deposit"):
        user = next((i for i in data if i["accountNo"] == acc_no and i["pin"] == int(pin)), None)
        if user:
            user["balance"] += amount
            Bank.save_data(data)
            st.success(f"Successfully deposited ${amount}. New Balance: ${user['balance']}")
        else:
            st.error("Invalid Credentials")

# --- Feature: Withdraw ---
elif choice == "Withdraw Money":
    st.subheader("Withdraw Funds")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount to Withdraw", min_value=1)

    if st.button("Withdraw"):
        user = next((i for i in data if i["accountNo"] == acc_no and i["pin"] == int(pin)), None)
        if user:
            if user["balance"] >= amount:
                user["balance"] -= amount
                Bank.save_data(data)
                st.success(f"Withdrew ${amount}. Remaining Balance: ${user['balance']}")
            else:
                st.error("Insufficient Funds!")
        else:
            st.error("Invalid Credentials")

# --- Feature: View Details ---
elif choice == "View Details":
    st.subheader("Account Statement")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Show Info"):
        user = next((i for i in data if i["accountNo"] == acc_no and i["pin"] == int(pin)), None)
        if user:
            st.json(user)
        else:
            st.error("User not found.")

# --- Feature: Delete ---
elif choice == "Delete Account":
    st.subheader("Close Account")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    confirm = st.checkbox("I understand this action is permanent.")

    if st.button("Delete My Account"):
        if confirm:
            user = next((i for i in data if i["accountNo"] == acc_no and i["pin"] == int(pin)), None)
            if user:
                data.remove(user)
                Bank.save_data(data)
                st.warning("Account deleted successfully.")
            else:
                st.error("Invalid Credentials")
        else:
            st.info("Please confirm the deletion checkbox.")

else:
    st.write("Welcome to the Digital Banking Portal. Use the sidebar to navigate.")