# Registration and Login Application with Glassmorphism Design

A modern registration and login application built with Flask, featuring glassmorphism UI design and Aiven MySQL database integration.

## Features

- **Glassmorphism Design**: Modern, frosted glass effect with animated floating shapes
- **User Registration**: Collects user data and stores it securely with password hashing
- **User Login**: Validates credentials against the database
- **Aiven MySQL**: Cloud-based MySQL database integration
- **Auto-redirect**: Redirects to login after successful registration
- **Netflix Integration**: Redirects to Kodest Netflix landing page upon successful login
- **Responsive Design**: Works on all device sizes

## Database Schema

The application uses a `User` table with the following structure:
- `UserId` (String, Primary Key) - User identifier
- `name` (String) - User's full name
- `password` (String) - Hashed password
- `email` (String, Unique) - User's email address
- `phone` (String) - User's phone number

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up Aiven MySQL Database
1. Create a MySQL database on Aiven
2. Copy your database credentials
3. Create a `.env` file based on `.env.example`

### 3. Configure Environment Variables
Create a `.env` file with your Aiven MySQL credentials:
```env
AIVEN_DB_HOST=your-aiven-host.aivencloud.com
AIVEN_DB_PORT=25060
AIVEN_DB_NAME=defaultdb
AIVEN_DB_USER=avnadmin
AIVEN_DB_PASSWORD=your-aiven-password
FLASK_SECRET_KEY=your_secret_key_here
```

### 4. Run the Application
```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`

## Usage

1. **Registration**: Visit the home page to register a new account
2. **Login**: After registration, you'll be redirected to the login page
3. **Access**: Upon successful login, you'll be redirected to Kodest Netflix

## Design Features

- **Glassmorphism**: Frosted glass effect with backdrop blur
- **Animated Background**: Floating shapes with smooth animations
- **Gradient Background**: Beautiful purple-blue gradient
- **Modern Typography**: Clean, readable fonts with proper spacing
- **Interactive Elements**: Hover effects and smooth transitions

## Security Features

- Password hashing using Werkzeug
- Environment variable configuration
- SQL injection prevention through SQLAlchemy ORM
- Session management

## Technologies Used

- **Backend**: Flask, SQLAlchemy
- **Database**: Aiven MySQL
- **Frontend**: HTML5, CSS3 (Glassmorphism)
- **Security**: Werkzeug password hashing
- **Environment**: python-dotenv

## File Structure

```
auth-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── templates/
│   ├── register.html     # Registration page
│   └── login.html        # Login page
└── README.md             # This file
```
