# Streamlit Login Webpage

A stylish and secure web application built with Streamlit featuring a modern authentication system with login and registration functionality.

## Features

- 🔐 User Authentication System
  - Login functionality with username/password
  - Two-step registration process
  - Session state management
  - Remember me option
  
- 💫 Modern UI Design
  - Blurred glass-morphism effect
  - Custom background wallpaper
  - Responsive layout
  - Stylish login/registration cards

- 🛡️ Protected Content
  - Secure content access after authentication
  - User session management
  - Logout functionality
  - Sidebar user information display

## Prerequisites

- Python 3.7+
- Streamlit
- Pandas

## Installation

1. Clone this repository:
```bash
git clone https://github.com/YOHANROSHITHA/Streamlit_Webpage.git
cd Streamlit_Webpage
```

2. Install the required packages:
```bash
pip install streamlit pandas
```

3. Make sure you have the background image:
- Place `image2.jpg` in the same directory as `app.py`

## Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. The application will open in your default web browser

3. Default demo credentials:
   - Username: `admin`
   - Password: `password`

## Structure

- `app.py` - Main application file containing all the logic
- `image2.jpg` - Background wallpaper image
- `README.md` - Project documentation

## Features in Detail

### Authentication System
- In-memory user storage (for demonstration purposes)
- Two-step registration process:
  1. Collect user profile information
  2. Set up password
- Session state management using Streamlit's session state
- Login validation with error handling

### UI/UX
- Modern glass-morphism design
- Blurred background effect
- Responsive layout that works on different screen sizes
- Interactive forms with validation
- Smooth transitions between login and registration

### Protected Content
- Example protected page with data visualization
- User-specific content display
- Secure session management
- Easy logout functionality

## Customization

You can customize the application by:
1. Modifying the CSS styles in the `inject_background` function
2. Changing the background image
3. Adjusting the blur and overlay settings
4. Adding more fields to the registration form
5. Extending the protected content section

## Security Note

This is a demonstration project and uses in-memory storage for user data. For production use, you should:
- Implement proper password hashing
- Use a secure database for user storage
- Add proper input validation
- Implement rate limiting
- Use HTTPS
- Add additional security measures as needed

## License

This project is open-source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.