import streamlit as st
import pandas as pd

st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")


# --------------------------
# Simple Login Page Template
# - in-memory credential check (example only)
# - uses st.session_state to track authentication
# - shows protected content after login
# --------------------------

# Example credentials (replace with real auth in production)
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"


def ensure_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    # store registered users in-memory for demo (username -> user data)
    if "users" not in st.session_state:
        st.session_state.users = {}
    # registration state: step 1 = collect profile, step 2 = set password
    if "registration_step" not in st.session_state:
        st.session_state.registration_step = 1
    # temporary storage for the registration info between steps
    if "pending_user" not in st.session_state:
        st.session_state.pending_user = None


def do_login():
    """Combined Login and Registration card.

    The card has a radio switch to toggle between Login and Register (step 1).
    Registration is two-step: profile -> set password. The second step uses the
    stored pending_user to show the username when creating the password.
    """
    # Card CSS (keeps previous styling, centered)
    st.markdown(
        """
    <style>
    /* Card container */
    .login-card {
        max-width: 540px;
        margin: 0 auto;
        padding: 1.5rem;
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(8px);
        border-radius: 12px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.25);
        border: 1px solid rgba(255,255,255,0.06);
        color: #fff;
    }

    .center-block { display:flex; justify-content:center; }

    .login-card .stTextInput>div>label, .login-card .stSelect>div>label { color: #eee; }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Layout: center column
    _, center_col, _ = st.columns([1, 2, 1])

    with center_col:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        mode = st.radio("", ["Login", "Register"], horizontal=True, index=0)

        # --- LOGIN ---
        if mode == "Login":
            with st.form("login_form"):
                st.subheader("Sign in")
                username = st.text_input("Username", key="login_username")
                password = st.text_input("Password", type="password", key="login_password")
                cols = st.columns([1, 1])
                with cols[0]:
                    remember = st.checkbox("Remember me", key="login_remember")
                submitted = st.form_submit_button("Login")

            if submitted:
                # check against stored users first, then fallback to demo credentials
                if username in st.session_state.users:
                    user = st.session_state.users[username]
                    if user.get("password") == password:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.experimental_rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    # fallback demo account
                    if username == VALID_USERNAME and password == VALID_PASSWORD:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.experimental_rerun()
                    else:
                        st.error("Invalid username or password")

        # --- REGISTER STEP 1: profile ---
        else:
            # Two-step registration flow
            step = st.session_state.get("registration_step", 1)
            if step == 1:
                with st.form("reg_form_step1"):
                    st.subheader("Create an account")
                    first_name = st.text_input("First name")
                    last_name = st.text_input("Last name")
                    email = st.text_input("Email")
                    id_no = st.text_input("ID No")
                    gender = st.selectbox("Gender", ["Prefer not to say", "Male", "Female", "Other"])
                    username = st.text_input("Choose a username")
                    submitted = st.form_submit_button("Continue")

                if submitted:
                    if not username:
                        st.error("Please choose a username")
                    elif username in st.session_state.users:
                        st.error("Username already taken")
                    else:
                        # store pending user info in session_state
                        st.session_state.pending_user = {
                            "first_name": first_name,
                            "last_name": last_name,
                            "email": email,
                            "id_no": id_no,
                            "gender": gender,
                            "username": username,
                        }
                        st.session_state.registration_step = 2
                        st.experimental_rerun()

            else:
                # Step 2: set password for pending_user
                pending = st.session_state.get("pending_user") or {}
                uname = pending.get("username", "")
                st.write(f"Creating password for **{uname}**")
                with st.form("reg_form_step2"):
                    pwd = st.text_input("Create password", type="password", key="reg_pwd")
                    pwd2 = st.text_input("Re-enter password", type="password", key="reg_pwd2")
                    submitted2 = st.form_submit_button("Complete registration")
                    cols = st.columns([1, 1])
                    with cols[0]:
                        if st.form_submit_button("Back to edit"):
                            st.session_state.registration_step = 1
                            st.experimental_rerun()

                if submitted2:
                    if not pwd or not pwd2:
                        st.error("Please enter and confirm the password")
                    elif pwd != pwd2:
                        st.error("Passwords do not match")
                    else:
                        # finalize registration
                        user_record = pending.copy()
                        user_record["password"] = pwd
                        st.session_state.users[uname] = user_record
                        st.success("Registration complete. You can now log in.")
                        # reset registration state
                        st.session_state.pending_user = None
                        st.session_state.registration_step = 1
                        st.experimental_rerun()

        st.markdown('</div>', unsafe_allow_html=True)


def do_logout():
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.experimental_rerun()


def protected_page():
    st.sidebar.markdown(f"**Logged in as:** {st.session_state.username}")
    if st.sidebar.button("Logout"):
        do_logout()

    st.title("My Webpage — Protected")
    st.write(f"Welcome, **{st.session_state.username}**! This is protected content.")

    # Example content: small dataframe
    df = pd.DataFrame({"first column": [1, 2, 3], "second column": ["a", "b", "c"]})
    st.dataframe(df)


def main():
    ensure_session_state()

    # inject the background wallpaper before rendering UI
    inject_background()

    if not st.session_state.authenticated:
        do_login()
    else:
        protected_page()


# --- Background wallpaper CSS ---
def inject_background(blur_px: int = 12, overlay_alpha: float = 0.25):
    """Inject CSS to add a full-screen background image with a blur overlay."""
    import base64
    from pathlib import Path

    # Read and encode the image
    try:
        image_path = Path("image2.jpg").absolute()
        if not image_path.exists():
            st.error("Background image not found! Please make sure image2.jpg is in the same folder as app.py")
            return False

        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()
            
        bg_data_url = f"data:image/jpeg;base64,{image_data}"
    except Exception as e:
        st.error(f"Error loading background image: {str(e)}")
        return False
        
        css = f"""
        <style>
        /* Main app container */
        [data-testid="stAppViewContainer"] {{
            background-image: url('{bg_data_url}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            position: relative;
            min-height: 100vh;
        }}

        /* Overlay that applies blur and tint so content remains readable */
        [data-testid="stAppViewContainer"]::before {{
            content: "";
            position: absolute;
            inset: 0;
            background: rgba(0,0,0,{overlay_alpha});
            backdrop-filter: blur({blur_px}px);
            -webkit-backdrop-filter: blur({blur_px}px);
            z-index: 0;
            pointer-events: none;
        }}

        /* Ensure the main content appears above the overlay */
        [data-testid="stMainContent"] {{
            position: relative;
            z-index: 1;
        }}

        /* Slightly translucent sidebar with blur */
        [data-testid="stSidebar"] {{
            background-color: rgba(255,255,255,0.05);
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            z-index: 1;
        }}

        /* Transparent header/toolbar */
        header {{ background: transparent; }}
        </style>
        """

        st.markdown(css, unsafe_allow_html=True)


if __name__ == "__main__":
    main()





