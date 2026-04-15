import hashlib
import time

# Function that takes a plaintext string and returns its MD5 hash
def string_to_md5_hash(str):
    # 1. Encode the string to bytes
    # 2. Generate the MD5 hash
    # 3. Get the hexadecimal representation
    md5_hash = hashlib.md5(str.encode()).hexdigest()
    return md5_hash

# Function that takes a plaintext string and returns its SHA256 hash
def string_to_sha256_hash(str):
    # Same as MD5 but replace that with SHA256
    sha256_hash = hashlib.sha256(str.encode()).hexdigest()
    return sha256_hash

stored_md5_hash = string_to_md5_hash("password123")
stored_sha256_hash = string_to_sha256_hash("password123")


# Function that verifies a plaintext guess against a stored hash
def verify(guess, stored_hash):
    # Check to len of stored hash to determine proper encoding (md5 vs sha256), throws error if not proper length, encodes and hashes the guess
    try:
        if len(stored_hash) == 32: 
            guess = hashlib.md5(guess.encode()).hexdigest()
        elif len(stored_hash) == 64:
            guess = hashlib.sha256(guess.encode()).hexdigest()
        else:
            raise ValueError("Unrecognized length")
    except ValueError as e:
        print(f'Error: {e}')
        return False
        
    # Check if guess matches stored hash
    if guess == stored_hash:
        return True
    else:
        return False
#print(verify("password123", stored_md5_hash))
#print(verify("password123", stored_sha256_hash))

def dictionary_attack():
    # Open rockyou.txt with utf-8 encoding, ignoring any characters that can't be decoded
    with open('rockyou.txt', 'r', encoding='utf-8', errors='ignore') as file:
        attempt_counter = 0
        start_time = time.perf_counter()

        # Iterate through each line in the wordlist
        for line in file:
            guess = line.strip() # Remove newline character and whitespace
            result = verify(guess, stored_md5_hash) # Hash guess and compare to stored hash
            attempt_counter += 1

            # If match found, report and exit
            if result:
                end_time = time.perf_counter()
                elasped_time = end_time - start_time
                print(f'Password: {guess}')
                print(f'Attempts: {attempt_counter}')
                print(f'Time Elapsed: {elasped_time:.2f} seconds')
                return
            
         # Only reaches here if entire wordlist exhausted with no match
        end_time = time.perf_counter()
        elasped_time = end_time - start_time
        print("Password not found in wordlist")
        print(f"Attempts: {attempt_counter}")
        print(f"Time Elapsed: {elasped_time:.2f} seconds")

dictionary_attack()