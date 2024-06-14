import re
import os

contacts = {}

def display_menu():
    print("\nWelcome to the Contact Management System!")
    print("Menu:")
    print("1. Add a new contact")
    print("2. Edit an existing contact")
    print("3. Delete a contact")
    print("4. Search for a contact")
    print("5. Display all contacts")
    print("6. Export contacts to a text file")
    print("7. Import contacts from a text file")
    print("8. Quit")

def get_contact_input():
    name = input("Enter name: ")
    phone = input("Enter phone number (format: 123-456-7890): ")
    email = input("Enter email address: ")
    additional_info = input("Enter additional information: ")
    return name, phone, email, additional_info

def validate_phone(phone):
    return re.match(r"^\d{3}-\d{3}-\d{4}$", phone)

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def add_contact():
    name, phone, email, additional_info = get_contact_input()
    if not validate_phone(phone):
        print("Invalid phone number format. Please use format: 123-456-7890")
        return
    if not validate_email(email):
        print("Invalid email format.")
        return
    if phone in contacts:
        print("Contact with this phone number already exists.")
        return
    contacts[phone] = {
        "name": name,
        "phone": phone,
        "email": email,
        "additional_info": additional_info
    }
    print("Contact added successfully.")

def edit_contact():
    identifier = input("Enter the phone number of the contact to edit: ")
    contact = find_contact(identifier)
    if not contact:
        print("Contact not found.")
        return
    
    print("Contact found:")

    print("What would you like to update?")
    print("1. Name")
    print("2. Phone number")
    print("3. Email address")
    print("4. Additional information")
    choice = input("Enter your choice: ")

    if choice == '1':
        name = input("Enter new name: ")
        contacts[contact['phone']]['name'] = name
    elif choice == '2':
        phone = input("Enter new phone number (format: 123-456-7890): ")
        if not validate_phone(phone):
            print("Invalid phone number format. Please use format: 123-456-7890")
            return
        if phone in contacts and phone != contact['phone']:
            print("Contact with this phone number already exists.")
            return
        contacts[phone] = contacts.pop(contact['phone'])
        contacts[phone]['phone'] = phone
    elif choice == '3':
        email = input("Enter new email address: ")
        if not validate_email(email):
            print("Invalid email format.")
            return
        contacts[contact['phone']]['email'] = email
    elif choice == '4':
        additional_info = input("Enter new additional information: ")
        contacts[contact['phone']]['additional_info'] = additional_info
    else:
        print("Invalid choice. No updates made.")
        return
    
    print("Contact updated successfully.")

def delete_contact():
    phone = input("Enter the phone number of the contact to delete: ")
    if phone in contacts:
        del contacts[phone]
        print("Contact deleted successfully.")
    else:
        print("Contact not found.")

def search_contact():
    phone = input("Enter the phone number of the contact to search: ")
    if phone in contacts:
        contact = contacts[phone]
        print(f"Name: {contact['name']}")
        print(f"Phone: {contact['phone']}")
        print(f"Email: {contact['email']}")
        print(f"Additional Info: {contact['additional_info']}")
    else:
        print("Contact not found.")

def display_all_contacts():
    if not contacts:
        print("No contacts available.")
    for phone, contact in contacts.items():
        print(f"Phone: {phone}, Name: {contact['name']}, Email: {contact['email']}, Additional Info: {contact['additional_info']}")

def export_contacts(filename):
    try:
        with open(filename, 'w') as file:
            for phone, contact in contacts.items():
                file.write(f"{contact['name']},{contact['phone']},{contact['email']},{contact['additional_info']}\n")
        print("Contacts exported successfully.")
    except IOError:
        print(f"Error exporting contacts to {filename}. Check file path and permissions.")

def import_contacts(filename):
    global contacts
    if not os.path.exists(filename):
        print("File not found.")
        return
    try:
        with open(filename, 'r') as file:
            contacts.clear()  # Clear existing contacts
            for line in file:
                name, phone, email, additional_info = line.strip().split(',')
                contacts[phone] = {
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "additional_info": additional_info
                }
        print("Contacts imported successfully.")
    except IOError:
        print(f"Error importing contacts from {filename}. Check file path and permissions.")

def find_contact(identifier):
    for contact in contacts.values():
        if identifier == contact['phone'] or identifier == contact['email']:
            return contact
    return None

def main():
    while True:
        display_menu()
        choice = input("Select an option: ")
        if choice == '1':
            add_contact()
        elif choice == '2':
            edit_contact()
        elif choice == '3':
            delete_contact()
        elif choice == '4':
            search_contact()
        elif choice == '5':
            display_all_contacts()
        elif choice == '6':
            filename = input("Enter filename to export: ")
            export_contacts(filename)
        elif choice == '7':
            filename = input("Enter filename to import: ")
            import_contacts(filename)
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
