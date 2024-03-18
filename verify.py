import firebase_admin
from firebase_admin import db, auth, credentials

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://gps-tracker-garuda-default-rtdb.asia-southeast1.firebasedatabase.app/"})

def sign_up(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        return user
    except:
        return None

def sign_in(email, password):
    try:
        user = auth.get_user_by_email(email)
        return user
    except:
        return None

def change_password(uid, new_password):
    try:
        auth.update_user(uid, password=new_password)
        return "Success"
    except:
        return None

def reset_password(email):
    try:
        auth.generate_password_reset_link(email)
        return "Success"
    except:
        return None

# Example usage
if __name__ == "__main__":
    # Replace these with your desired email and password
    email = "example@example.com"
    password = "example_password"
    new_password = "new_example_password"

    # Sign up
    # sign_up(email, password)

    # Sign in
    user = sign_in(email, password)
    if user:
        ref = db.reference("/")
        ref.child(user.uid).set({"lon": 0.1, "lat": 0.0})

    sign_up("hulu@hulu.com", "password")
    user = sign_in("hulu@hulu.com", "password")
    if user:
        ref = db.reference("/")
        ref.child(user.uid).set({"lon": 0.1, "lat": 5.0})

    # Change password (requires user UID, you can get it from user object returned by sign_in method)
    # change_password(user.uid, new_password)

    # Reset password
    # reset_password(email)
