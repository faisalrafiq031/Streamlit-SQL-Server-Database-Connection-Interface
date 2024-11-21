# Streamlit SQL Server Database Connection Interface

A streamlined, user-friendly app built with Streamlit to connect to SQL Server databases, view and interact with data tables, and export data in various formats. This interface supports both Windows Authentication and SQL Server Authentication, allowing flexible and secure connections.

## Features

- **Flexible Database Connection**: Connect to multiple SQL Server databases with options for both Windows Authentication and SQL Server authentication.
- **Database and Table Management**: View available databases and tables, and switch between them with ease.
- **Data Retrieval and Display**: Retrieve and display data from selected tables.
- **Download Options**: Export table data as CSV or Excel files for offline analysis or reporting.
- **Customizable Theme**: Includes custom CSS for a light gray and black theme for improved readability and user experience.

## Demo

### Sidebar
- **Database Type**: Choose from options such as All, AWS, Azure, or Microsoft.
- **Database Selection**: After choosing the database type, select the specific database (e.g., SQL Server, AWS RDS).
  
### Main Interface
- **Authentication Options**: Enter SQL Server details, select authentication method, and input credentials if necessary.
- **Database Navigation**: Select a database and table to view its contents.
- **Data Download**: Download data in CSV or Excel format with a single click.

## Requirements

- **Python** 3.7+
- **Streamlit** for creating the web app interface
- **SQLAlchemy** and **pyodbc** for database connection management
- **Pandas** for data handling and export

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/faisalrafiq031/streamlit-sql-server-interface.git
   cd streamlit-sql-server-interface
   ```

2. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

   > **Note**: You may need the [ODBC Driver 17 for SQL Server](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server) installed on your machine.

3. **Run the Streamlit App**:
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Launch the App**: After running the app, open the provided local URL in your browser.
2. **Connect to SQL Server**:
   - Select the Database Type and Database.
   - Enter your SQL Server name and authentication details.
   - Click **Connect** to establish a connection.
3. **View and Manage Data**:
   - Select a database from the dropdown to view available tables.
   - Choose a table to display its contents.
4. **Download Data**:
   - Use the **Download as CSV** or **Download as Excel** buttons to save data.

## Customization

### CSS Styling
The app includes custom CSS styling for a light gray and black theme. You can modify the CSS in the `st.markdown` section to adjust colors, font sizes, or add additional styles to suit your preferences.

## Troubleshooting

- **Connection Errors**: Ensure your SQL Server instance allows remote connections and the ODBC driver is correctly installed.
- **Authentication Issues**: Verify that credentials and authentication method (Windows or SQL) are set correctly in the input fields.

## Contributions

Feel free to fork the repository and submit pull requests for any improvements or additional features! For major changes, please open an issue to discuss your proposed changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

 
