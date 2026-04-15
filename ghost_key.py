import hashlib
import time
import itertools
import string
from colorama import Fore, Style, init
from tqdm import tqdm

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
    # Check len of stored hash to determine proper encoding (md5 vs sha256), throws error if not proper length, encodes and hashes the guess
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

def dictionary_attack():
    # Open rockyou.txt with utf-8 encoding, ignoring any characters that can't be decoded
    with open('rockyou.txt', 'r', encoding='utf-8', errors='ignore') as file:
        attempt_counter = 0
        start_time = time.perf_counter()

        # Iterate through each line in the wordlist
        for line in tqdm(file, total=14344391):
            guess = line.strip() # Remove newline character and whitespace
            result = verify(guess, stored_md5_hash) # Hash guess and compare to stored hash
            attempt_counter += 1

            # If match found, report and exit
            if result:
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                print(Fore.GREEN + f'Password: {guess}' + Style.RESET_ALL)
                print(f'Attempts: {attempt_counter}')
                print(f'Time Elapsed: {elapsed_time:.2f} seconds')
                return
            
        # Only reaches here if entire wordlist exhausted with no match
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(Fore.RED + "Password not found in wordlist" + Style.RESET_ALL)
        print(f"Attempts: {attempt_counter}")
        print(f"Time Elapsed: {elapsed_time:.2f} seconds")

# You would call brute_force_attack with the char_set, like string.ascii_lowercase and integers for min and max length, starting at 1 (passwords can't be 0)
# example, brute_force_attack(string.ascii_lowercase, 1, 6)
def brute_force_attack(char_set, min_length, max_length):
    attempt_counter = 0
    start_time = time.perf_counter()

    # Map known string constants to human readable labels for output
    possible_sets = [
    (string.ascii_lowercase, "lowercase"),
    (string.ascii_uppercase, "uppercase"),
    (string.digits, "digits"),
    (string.punctuation, "symbols"),
    ]

    # Auto-detect which character sets are present in char_set
    description = []
    for charset, label in possible_sets:
        if all(c in char_set for c in charset):
            description.append(label)   
    description_label = " + ".join(description) if description else "custom"

    # Generate every combination from min_length to max_length and check against stored hash
    for i in range(min_length, max_length + 1):
        total = len(char_set) ** i
        for combo in tqdm(itertools.product(char_set, repeat=i), total=total):
            converted_combo = "".join(combo) # product returns tuples, join converts to string
            result = verify(converted_combo, stored_md5_hash)
            attempt_counter += 1

            # If match found, report and exit
            if result:
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                print(Fore.GREEN + f'Password: {converted_combo}' + Style.RESET_ALL)
                print(f"Searched: {description_label} lengths {min_length}-{max_length}")
                print(f'Attempts: {attempt_counter}')
                print(f'Time Elapsed: {elapsed_time:.2f} seconds')
                return
    
    # Only reaches here if search space exhausted with no match
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(Fore.RED + "Password not found in wordlist" + Style.RESET_ALL)
    print(f"Searched: {description_label} lengths {min_length}-{max_length}")
    print(f"Attempts: {attempt_counter}")
    print(f"Time Elapsed: {elapsed_time:.2f} seconds")
brute_force_attack(string.ascii_lowercase, 1, 6)