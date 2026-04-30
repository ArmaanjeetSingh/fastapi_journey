import streamlit as st
import requests
import pandas as pd

# Configuration
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Expense Tracker", layout="wide")

# --- Authentication Logic ---
def login(username, password):
    url = f"{BASE_URL}/auth/token"
    data = {"username": username, "password": password}
    response = requests.post(url, data=data) # FastAPI OAuth2 uses form data
    return response

def register(name, email, password, role):
    url = f"{BASE_URL}/auth/"
    payload = {"name": name, "email": email, "password": password, "role": role}
    response = requests.post(url, json=payload)
    return response

# --- Session State Initialization ---
if "token" not in st.session_state:
    st.session_state.token = None

# --- Sidebar: Auth ---
st.sidebar.title("👤 User Account")
if not st.session_state.token:
    auth_mode = st.sidebar.radio("Login / Register", ["Login", "Register"])
    
    if auth_mode == "Login":
        user = st.sidebar.text_input("Username")
        pw = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            res = login(user, pw)
            if res.status_code == 200:
                st.session_state.token = res.json()["access_token"]
                st.sidebar.success("Logged in!")
                st.rerun()
            else:
                st.sidebar.error("Invalid credentials")
    else:
        new_name = st.sidebar.text_input("Full Name")
        new_email = st.sidebar.text_input("Email")
        new_pw = st.sidebar.text_input("Password", type="password")
        new_role = st.sidebar.selectbox("Role", ["admin", "user"])
        if st.sidebar.button("Create Account"):
            res = register(new_name, new_email, new_pw, new_role)
            if res.status_code == 201:
                st.sidebar.success("Account created! Please login.")
            else:
                st.sidebar.error("Registration failed")
else:
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.rerun()

# --- Main App Logic ---
if not st.session_state.token:
    st.title("💰 Welcome to Expense Tracker")
    st.info("Please login from the sidebar to manage your expenses.")
else:
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    tab1, tab2 = st.tabs(["📊 Expenses", "🏷️ Categories"])

    # --- TAB 1: EXPENSES ---
    with tab1:
        st.header("Your Expenses")
        
        # Form to add expense
        with st.expander("➕ Add New Expense"):
            # Fetch categories for the dropdown
            cat_res = requests.get(f"{BASE_URL}/categories/", headers=headers)
            if cat_res.status_code == 200:
                categories = cat_res.json()
                cat_options = {c['name']: c['id'] for c in categories}
                
                with st.form("add_expense"):
                    amount = st.number_input("Amount", min_value=0.1)
                    e_type = st.selectbox("Type", ["Essential", "Leisure", "Investment"])
                    cat_name = st.selectbox("Category", options=list(cat_options.keys()))
                    if st.form_submit_button("Save"):
                        payload = {
                            "amount": amount, 
                            "type": e_type, 
                            "category_id": cat_options[cat_name]
                        }
                        requests.post(f"{BASE_URL}/expenses/", json=payload, headers=headers)
                        st.success("Expense added!")
            else:
                st.warning("Create a category first!")

        # List Expenses
        res = requests.get(f"{BASE_URL}/expenses/", headers=headers)
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.write("No expenses found.")

    # --- TAB 2: CATEGORIES ---
    with tab2:
        st.header("Manage Categories")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Add Category")
            with st.form("add_cat"):
                c_name = st.text_input("Category Name")
                c_desc = st.text_area("Description")
                if st.form_submit_button("Create"):
                    payload = {"name": c_name, "description": c_desc}
                    requests.post(f"{BASE_URL}/categories/", json=payload, headers=headers)
                    st.rerun()

        with col2:
            st.subheader("Existing Categories")
            res = requests.get(f"{BASE_URL}/categories/", headers=headers)
            if res.status_code == 200:
                st.table(res.json())