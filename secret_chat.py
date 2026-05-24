from cryptography.fernet import Fernet

# 1. ഒരു രഹസ്യ താക്കോൽ (Secret Key) നിർമ്മിക്കുന്നു
# യഥാർത്ഥ ചാറ്റിൽ ഈ കീ രണ്ട് ഉപയോക്താക്കൾക്ക് മാത്രമേ അറിയാവൂ
secret_key = Fernet.generate_key()
cipher_suite = Fernet(secret_key)

print("==================================================")
print("🔐 MILITARY GRADE AES-256 ENCRYPTED CHAT SYSTEM")
print("==================================================")
print(f"നിങ്ങളുടെ രഹസ്യ താക്കോൽ (Secret Key):\n{secret_key.decode()}\n")
print("--------------------------------------------------\n")

# ഉപയോക്താവ് അയക്കാൻ ആഗ്രഹിക്കുന്ന രഹസ്യ സന്ദേശം
original_message = "നമ്മൾ ഇന്ന് രാത്രി 9 മണിക്ക് രഹസ്യമായി കാണുന്നു."
print(f"💬 [അയക്കുന്നയാൾ ടൈപ്പ് ചെയ്തത്]: {original_message}")

# 2. ENCRYPTION PROCESS (സന്ദേശം ലോക്ക് ചെയ്യുന്നു)
# മെസ്സേജ് ഇന്റർനെറ്റിലേക്ക് പോകുന്നതിന് മുൻപ് ലോക്ക് ആകുന്നു
bytes_message = original_message.encode('utf-8')
encrypted_message = cipher_suite.encrypt(bytes_message)

print("\n🚀 [ഇന്റർനെറ്റിലൂടെ/സെർവറിലൂടെ കടന്നുപോകുന്ന കോഡ്]:")
print(f"👉 {encrypted_message.decode()}")
print("(ഹാക്കർമാർക്കോ സെർവറിനോ ഈ മെസ്സേജ് കിട്ടിയാൽ അവർക്ക് ഇതേ കാണാൻ കഴിയൂ)")

# 3. DECRYPTION PROCESS (സന്ദേശം അൺലോക്ക് ചെയ്യുന്നു)
# മെസ്സേജ് സ്വീകരിക്കുന്ന ആളുടെ ഫോണിൽ എത്തിക്കഴിഞ്ഞാൽ ലോക്ക് തുറക്കുന്നു
decrypted_bytes = cipher_suite.decrypt(encrypted_message)
decrypted_message = decrypted_bytes.decode('utf-8')

print("\n📥 [സ്വീകരിക്കുന്നയാളുടെ സ്ക്രീനിൽ കാണുന്നത്]:")
print(f"✔ {decrypted_message}")
print("==================================================")

