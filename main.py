import socket
import firebase_admin
from firebase_admin import db, credentials
from plyer import gps
from kivy.app import App
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog


cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://gps-tracker-garuda-default-rtdb.asia-southeast1.firebasedatabase.app/"
    },
)


class MyRoot(BoxLayout):
    def __init__(self):
        super(MyRoot, self).__init__()

    def gen(self):
        if platform == "android":
            from android.permissions import Permission, request_permissions

            request_permissions(
                [Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION]
            )

            gps.configure(on_location=self.on_location, on_status=self.on_auth_status)
            # gps.start(minTime=1000, minDistance=0)
            gps.start()

    def on_location(self, **kwargs):
        user = None
        my_lat = kwargs["lat"]
        my_lon = kwargs["lon"]
        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)

        ref = db.reference("/")
        ref.child("unid").set({"lat": my_lat, "lon": my_lon, "ip": ip_addr})
        self.ran.text = f"Lat: {my_lat} \nLon: {my_lon}"

    def gps_stop(self):
        gps.stop()

    def on_auth_status(self, general_status):
        if general_status == "provider-enabled":
            pass
        else:
            self.open_gps_access_popus()

    def open_gps_access_popup(self):
        dialog = MDDialog(title="GPS Error", text="enable GPS")
        dialog.size_hint = [0.8, 0.8]
        dialog.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        dialog.open()

    def sign_up(self, email, password):
        try:
            user = firebase_admin.auth.create_user(email=email, password=password)
            return user
        except:
            return None

    def sign_in(self, email, password):
        try:
            user = firebase_admin.auth.get_user_by_email(email)
            return user
        except:
            return None

    def change_password(self, uid, new_password):
        try:
            firebase_admin.auth.update_user(uid, password=new_password)
            return "Success"
        except:
            return None

    def reset_password(self, email):
        try:
            firebase_admin.auth.generate_password_reset_link(email)
            return "Success"
        except:
            return None


class Main(App):
    def build(self):
        return MyRoot()


ran = Main()
ran.run()
