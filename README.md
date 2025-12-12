# Basic encryption
turing encrypt "Secret message" --paranoia high

# Save to file
turing encrypt "Classified data" -o encrypted.bin --paranoia nuclear

# Use quantum RNG
turing encrypt "Top secret" --qr --paranoia nuclear

# Store key in vault
turing encrypt "Message" --vault my_vault --burn-after

# Full example with all options
turing encrypt "Hello World" -o cipher.bin --paranoia high --qr --vault secure --burn-after

# Decrypt with hex key
turing decrypt a3f2e1d4... --key 9b8c7d6e...

# Decrypt from vault
turing decrypt a3f2e1d4... --vault my_vault

# Save to file
turing decrypt a3f2e1d4... --key 9b8c7d6e... -o plaintext.txt

# Full example
turing decrypt $(cat cipher.hex) --key $(cat key.hex) -o decrypted.txt
