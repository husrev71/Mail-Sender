import tkinter as tk
import smtplib
import json
import os

SETTINGS_FILE = "mail_settings.json"


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            try:
                settings = json.load(f)
                return settings.get('sender_email', ''), settings.get('sender_password', '')
            except json.JSONDecodeError:
                return '', ''
    return '', ''


def save_settings(email, password):
    settings = {'sender_email': email, 'sender_password': password}
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)


def display_save_note():
    status_label.config(text="Email and password have been saved as default.", fg="blue")


def send_mail():
    sender_email = sender_entry.get()
    sender_password = password_entry.get()
    receiver_email = receiver_entry.get()
    subject = subject_entry.get()
    message_body = message_text.get("1.0", tk.END).strip()

    if not all([sender_email, sender_password, receiver_email, subject, message_body]):
        status_label.config(text="Error: Please fill in all fields.", fg="red")
        return

    msg = f"Subject: {subject}\nTo: {receiver_email}\nFrom: {sender_email}\n\n{message_body}"

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.encode('utf-8'))
        server.quit()

        status_label.config(text="Email sent successfully!", fg="green")

        save_settings(sender_email, sender_password)

        root.after(3000, display_save_note)

    except Exception as e:
        status_label.config(text=f"Error: Failed to send email. Check credentials/settings.", fg="red")


root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

root.title("Mail Sender")

main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(fill=tk.BOTH, expand=True)

title_label = tk.Label(main_frame, text="Email Sender System", font=("Arial", 24, "bold"))
title_label.pack(pady=10)

tk.Label(main_frame, text="Your Email (Sender):", font=("Arial", 12)).pack(anchor='w', pady=(5, 0))
sender_entry = tk.Entry(main_frame, width=60)
sender_entry.pack(fill=tk.X, ipady=3)

tk.Label(main_frame, text="Your Password (Email Password):", font=("Arial", 12)).pack(anchor='w', pady=(5, 0))
password_entry = tk.Entry(main_frame, width=60, show='*')
password_entry.pack(fill=tk.X, ipady=3)

tk.Label(main_frame, text="Recipient Email (To):", font=("Arial", 12)).pack(anchor='w', pady=(5, 0))
receiver_entry = tk.Entry(main_frame, width=60)
receiver_entry.pack(fill=tk.X, ipady=3)

tk.Label(main_frame, text="Subject:", font=("Arial", 12)).pack(anchor='w', pady=(5, 0))
subject_entry = tk.Entry(main_frame, width=60)
subject_entry.pack(fill=tk.X, ipady=3)

tk.Label(main_frame, text="Message Body:", font=("Arial", 12)).pack(anchor='w', pady=(5, 0))
message_text = tk.Text(main_frame, height=15, width=60)
message_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

send_button = tk.Button(main_frame, text="SEND EMAIL", font=("Arial", 16, "bold"), command=send_mail, bg="green",
                        fg="white")
send_button.pack(fill=tk.X, ipady=5)

status_label = tk.Label(main_frame, text="", font=("Arial", 12))
status_label.pack(pady=(10, 0))

saved_email, saved_password = load_settings()
if saved_email:
    sender_entry.insert(0, saved_email)
if saved_password:
    password_entry.insert(0, saved_password)

root.mainloop()