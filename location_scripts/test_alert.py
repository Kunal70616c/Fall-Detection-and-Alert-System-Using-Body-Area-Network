# test_alert.py
# This script demonstrates how to call the send_fall_alert_email function.
# Ensure that 'send_alert_email.py' and 'get_nearby_hospitals.py' are in the same directory.

from send_alert_email import send_fall_alert_email

if __name__ == "__main__":
    print("--- Running example usage ---")
    # Example 1: Fall detected
    send_fall_alert_email(
        fall_detected=True,
        latitude=22.5678,
        longitude=88.4154,
        user_name="Test Subject 1"
    )
