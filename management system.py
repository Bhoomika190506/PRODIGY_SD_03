import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import re

FILE_NAME = "contacts.json"


def load_contacts():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return {}


def save_contacts():
    with open(FILE_NAME, "w") as file:
        json.dump(contacts, file, indent=4)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def add_contact():
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    email = entry_email.get().strip()

    if not (name and phone and email):
        messagebox.showwarning("Missing Data", "Please fill all fields.")
        return

    if not is_valid_email(email):
        messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
        return

    if name in contacts:
        overwrite = messagebox.askyesno("Duplicate", f"'{name}' already exists. Overwrite?")
        if not overwrite:
            return

    contacts[name] = {"phone": phone, "email": email}
    save_contacts()
    refresh_contact_list()
    messagebox.showinfo("Success", f"Contact '{name}' added/updated.")
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)

def view_contact():
    selected = listbox.curselection()
    if selected:
        name = listbox.get(selected)
        info = contacts[name]
        messagebox.showinfo(name, f"Phone: {info['phone']}\nEmail: {info['email']}")
    else:
        messagebox.showwarning("No Selection", "Please select a contact.")

# Delete contact
def delete_contact():
    selected = listbox.curselection()
    if selected:
        name = listbox.get(selected)
        if messagebox.askyesno("Confirm", f"Delete contact '{name}'?"):
            del contacts[name]
            save_contacts()
            refresh_contact_list()
            messagebox.showinfo("Deleted", f"Contact '{name}' deleted.")
    else:
        messagebox.showwarning("No Selection", "Please select a contact.")

def edit_contact():
    selected = listbox.curselection()
    if selected:
        name = listbox.get(selected)
        contact = contacts[name]

        new_phone = simpledialog.askstring("Edit Phone", "Enter new phone number:", initialvalue=contact["phone"])
        new_email = simpledialog.askstring("Edit Email", "Enter new email:", initialvalue=contact["email"])

        if new_phone and new_email and is_valid_email(new_email):
            contacts[name] = {"phone": new_phone.strip(), "email": new_email.strip()}
            save_contacts()
            messagebox.showinfo("Updated", f"Contact '{name}' updated.")
        else:
            messagebox.showwarning("Invalid Input", "Update canceled or invalid email.")
    else:
        messagebox.showwarning("No Selection", "Please select a contact.")

def refresh_contact_list():
    listbox.delete(0, tk.END)
    for name in sorted(contacts.keys()):
        listbox.insert(tk.END, name)

root = tk.Tk()
root.title("Contact Management System")
root.geometry("400x500")
root.resizable(False, False)
root.configure(bg="white")

contacts = load_contacts()

tk.Label(root, text="Name", bg="white").pack(pady=(10, 2))
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Phone", bg="white").pack(pady=(10, 2))
entry_phone = tk.Entry(root)
entry_phone.pack()

tk.Label(root, text="Email", bg="white").pack(pady=(10, 2))
entry_email = tk.Entry(root)
entry_email.pack()

tk.Button(root, text="Add Contact", width=20, command=add_contact).pack(pady=10)

tk.Label(root, text="Saved Contacts", bg="white", font=("Arial", 10, "bold")).pack(pady=(10, 2))
listbox = tk.Listbox(root)
listbox.pack(pady=5, fill=tk.BOTH, expand=True)

tk.Button(root, text="View Contact", command=view_contact).pack(pady=2)
tk.Button(root, text="Edit Contact", command=edit_contact).pack(pady=2)
tk.Button(root, text="Delete Contact", command=delete_contact).pack(pady=2)

refresh_contact_list()

root.bind("<Return>", lambda event: add_contact())

root.mainloop()
