from altair import Key
import streamlit as st
from cryptography.fernet import Fernet

# Generate a key (this should be stored securely in production)
# Creating a Function to store key securely:
def Generate_Key():    
    KEY = Fernet.generate_key()
    with open("secret.key", "wb") as f:
        f.write(KEY)
    return KEY

# Creating a Function to load key:
def Load_Key():
    try:
        return open("secret.key", "rb").read()
    except FileNotFoundError:
        return None

# Function to encrypt data
def encrypt_data(text, KEY):
    F = Fernet(KEY)
    return F.encrypt(text.encode()).decode()

# Function to decrypt data
def decrypt_data(encrypted_text, KEY):
    F = Fernet(KEY)
    return F.decrypt(encrypted_text.encode()).decode()

# Streamlit UI
st.set_page_config(layout="wide", page_title="Secure Data Encryption")
st.title("🔒 Secure Data Encryption System")


# Navigation Bar
menu = ["Home","Generate Key", "Encrypt Data", "Retrieve Data"]
choice = st.sidebar.selectbox("Navigation Bar", menu)

# Step 1: Home Page
if choice == "Home":
    st.subheader("🏠 Welcome to the Secure Data System")
    st.write("Use this app to **securely store and retrieve data** using unique generated key.")

# Step 2: Generate Key
elif choice == "Generate Key":
    if st.button("Generate Secret Key"):
        Generate_Key()
        st.success("✅ secret.key generated and saved!")

# Step 3: Encrypt Data
elif choice == "Encrypt Data":
    note = st.text_area("Write your content to secure it...")
    if st.button("Encrypt"):
        key = Load_Key()
        if key:
            encrypted = encrypt_data(note, key)
            st.text_area("🔒 Encrypted Note", encrypted)
            st.download_button("💾 Download Encrypted Note", encrypted, file_name="encrypted_note.txt")
        else:
            st.error("❌ secret.key not found. Please generate the key first.")

# Step 4: Decrypt Data
elif choice == "Retrieve Data":
    encrypted_note = st.text_area("Paste your encrypted note from the downloaded file...")
    if st.button("Decrypt"):
        key = Load_Key()
        if key:
            try:
                decrypted = decrypt_data(encrypted_note, key)
                st.text_area("🔓 Decrypted Note", decrypted)
            except:
                st.error("❌ Invalid encrypted text or key.")
        else:
            st.error("❌ secret.key not found. Please generate the key first.")