# Made with 💛 by Faisal Rafiq 


# pip install streamlit sqlalchemy pandas openpyxl xlsxwriter

import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import urllib.parse
from io import BytesIO

# Initialize session state for connection and selected database
if "connection_established" not in st.session_state:
    st.session_state.connection_established = False
if "selected_database" not in st.session_state:
    st.session_state.selected_database = None

# Custom CSS for light gray and black theme
st.markdown("""
    <style>
    /* General Background */
    body, .reportview-container {
        background-color: #f0f0f0;
    }

    /* Sidebar Style */
    .sidebar .sidebar-content {
        background-color: #333333;
        color: #ffffff;
    }
    .sidebar .sidebar-content h2 {
        color: #ffffff;
    }
    
    /* Sidebar Menu Styling */
    .sidebar-link {
        padding: 10px 15px;
        font-size: 18px;
        color: #ffffff;
        cursor: pointer;
        text-decoration: none;
        display: block;
    }
    .sidebar-link:hover {
        background-color: #555555;
        color: #ffffff;
    }

    /* Main Content Box Styling */
    .stButton > button, .stTextInput, .stSelectbox {
        background-color: #f9f9f9;
        color: #333333;
        border: 1px solid #cccccc;
        padding: 8px;
        border-radius: 5px;
    }

    /* Button Styling */
    .stButton > button {
        background-color: #333333;
        color: #ffffff;
        border: none;
        padding: 8px 16px;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #555555;
    }

    /* Header Styling */
    h1, h2, h3, h4, h5, h6 {
        color: #333333;
    }

    /* Table Styling */
    .dataframe {
        color: #333333;
        background-color: #f9f9f9;
        border: 1px solid #cccccc;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Menu Creation (Logo)
st.sidebar.title("DB Connection")

# Define menu options  
menu_options = ["Home", "Databases", "Option Two", "Option Three", "Option Four"]

# Sidebar links for each menu option
for option in menu_options:
    st.sidebar.markdown(f'<a class="sidebar-link" href="?page={option}">{option}</a>', unsafe_allow_html=True)

# Retrieve the selected page from the URL query parameter
selected_page = st.experimental_get_query_params().get("page", ["Home"])[0]

if selected_page == "Home":
    st.title("Welcome to Django Database Connection")
    st.write("Where you can get connected into SQL")

elif selected_page == "Databases":
    st.header("Databases")

    db_type = st.selectbox("Choose Database Type", ["All", "AWS", "Azure", "Microsoft"]) # Add more Available

    if db_type == "All":
        db_options = ["SQLite", "Postgres", "MySQL", "Example"] # Add more Available
    elif db_type == "AWS":
        db_options = ["AWS_RDS", "Postgres_AWS"] # Add more Available
    elif db_type == "Azure":
        db_options = ["Azure_SQL"] # Add more Available
    elif db_type == "Microsoft":
        db_options = ["SQL Server"] # Add more Available

    selected_db = st.selectbox("Select Database", db_options)

    if not st.session_state.connection_established:
        st.subheader(f"Connect to {selected_db}")
        db_server = st.text_input("DB Server Name (e.g., DESKTOP-XXXXXXX\\SQLEXPRESS)")
        use_windows_auth = st.checkbox("Windows Authentication Trusted")  # Use checkbox for Windows Authentication
        
        # Only request username and password if Windows Authentication is not selected
        if not use_windows_auth:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
        else:
            username = ""
            password = ""

        if st.button("Connect"):
            try:
                if use_windows_auth:
                    # Windows Authentication: No need for username and password
                    connection_string = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db_server};DATABASE=master;Trusted_Connection=yes;')}"
                else:
                    # Using SQL Server authentication
                    connection_string = f"mssql+pyodbc://{username}:{password}@{db_server}/master?driver=ODBC+Driver+17+for+SQL+Server"

                engine = create_engine(connection_string)
                conn = engine.connect()
                st.success("Connected successfully")
                
                # Store connection details in session state
                st.session_state.connection_established = True
                st.session_state.engine = engine  # Store the engine for reuse
                st.session_state.selected_database = None  # Reset selected database
                st.session_state.db_server = db_server  # Store the server
                st.session_state.use_windows_auth = use_windows_auth  # Store authentication method
                
            except Exception as e:
                st.error(f"Connection failed: {e}")
    
    # Only show database options if connected
    if st.session_state.connection_established:
        engine = st.session_state.engine  # Retrieve the stored engine

        # Retrieve and display available databases
        databases = pd.read_sql("SELECT name FROM sys.databases", engine)
        selected_database = st.selectbox("Available Databases", databases['name'], index=databases['name'].tolist().index(st.session_state.selected_database) if st.session_state.selected_database else 0)
        
        # Store selected database in session state
        st.session_state.selected_database = selected_database
        
        if selected_database:
            # Update the connection to point to the selected database directly
            db_server = st.session_state.db_server
            use_windows_auth = st.session_state.use_windows_auth

            if use_windows_auth:
                db_connection_string = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db_server};DATABASE={selected_database};Trusted_Connection=yes;')}"
            else:
                # If SQL authentication is used, use username and password from user input
                username = st.text_input("Username", value="")
                password = st.text_input("Password", value="", type="password")
                db_connection_string = f"mssql+pyodbc://{username}:{password}@{db_server}/{selected_database}?driver=ODBC+Driver+17+for+SQL+Server"

            db_engine = create_engine(db_connection_string)
            db_conn = db_engine.connect()

            # Retrieve and display tables in the selected database
            tables = pd.read_sql("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'", db_conn)
            st.write("Tables Available in Selected Database:")
            st.write(tables)
            
            table_name = st.selectbox("Select a Table", tables['TABLE_NAME'])

            if table_name:
                # Fetch the data from the selected table
                query = f"SELECT * FROM {table_name}"
                data = pd.read_sql(query, db_conn)
                
                # Display the table data
                st.write(f"Showing data from {table_name} table:")
                st.write(data)

                # Provide download options
                st.subheader("Download Options")

                # Download as CSV
                csv = data.to_csv(index=False)
                st.download_button("Download as CSV", csv, file_name=f"{table_name}.csv", mime="text/csv")

                # Download as Excel (using BytesIO)
                excel_buffer = BytesIO()
                with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
                    data.to_excel(writer, index=False, sheet_name=table_name)
                excel_buffer.seek(0)  # Move to the beginning of the buffer

                st.download_button("Download as Excel", excel_buffer, file_name=f"{table_name}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            
            db_conn.close()

# These for later menu if you want to add and work on.

elif selected_page == "Option Two":
    st.write("Content for Option Two")
elif selected_page == "Option Three":
    st.write("Content for Option Three")
elif selected_page == "Option Four":
    st.write("Content for Option Four")
