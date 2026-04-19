import time
import itertools
import string
from colorama import Fore, Style, init # type: ignore
init()
from tqdm import tqdm # type: ignore
from hashing import verify

def dictionary_attack(stored_hash):
    print(Fore.YELLOW + "\n[*] Running dictionary attack..." + Style.RESET_ALL)
    
    # Open rockyou.txt with utf-8 encoding, ignoring any characters that can't be decoded
    with open('rockyou.txt', 'r', encoding='utf-8', errors='ignore') as file:
        attempt_counter = 0
        start_time = time.perf_counter()

        # Iterate through each line in the wordlist
        for line in tqdm(file, total=14344391):
            guess = line.strip() # Remove newline character and whitespace
            result = verify(guess, stored_hash) # Hash guess and compare to stored hash
            attempt_counter += 1

            # If match found, report and exit
            if result:
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                print(Fore.GREEN + f'Password: {guess}' + Style.RESET_ALL)
                print(f'Attempts: {attempt_counter:,}')
                print(f'Time Elapsed: {elapsed_time:.2f} seconds')
                return True
            
        # Only reaches here if entire wordlist exhausted with no match
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(Fore.RED + "Password not found in wordlist" + Style.RESET_ALL)
        print(f"Attempts: {attempt_counter:,}")
        print(f"Time Elapsed: {elapsed_time:.2f} seconds")
        return False

# You would call brute_force_attack with the char_set, like string.ascii_lowercase and integers for min and max length, starting at 1 (passwords can't be 0)
# example, brute_force_attack(string.ascii_lowercase, 1, 6)
def brute_force_attack(stored_hash, char_set, min_length, max_length):
    print(Fore.YELLOW + "\n[*] Running brute force attack..." + Style.RESET_ALL)
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
            result = verify(converted_combo, stored_hash)
            attempt_counter += 1

            # If match found, report and exit
            if result:
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                print(Fore.GREEN + f'Password: {converted_combo}' + Style.RESET_ALL)
                print(f"Searched: {description_label} lengths {min_length}-{max_length}")
                print(f'Attempts: {attempt_counter:,}')
                print(f'Time Elapsed: {elapsed_time:.2f} seconds')
                return True
    
    # Only reaches here if search space exhausted with no match
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(Fore.RED + "Password not found in wordlist" + Style.RESET_ALL)
    print(f"Searched: {description_label} lengths {min_length}-{max_length}")
    print(f"Attempts: {attempt_counter:,}")
    print(f"Time Elapsed: {elapsed_time:.2f} seconds")
    return False

def leet_speak(word):
    # Map of common leet speak character substitutions
    # Used to generate password variations that replace letters with look-alike symbols/numbers
    leet_map = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$'}
    variations = []

    # For each substitution, if the character exists in the word add a leet variation
    for char, substitute in leet_map.items():
        if char in word.lower():
            variations.append(word.lower().replace(char, substitute))
    return variations

def cupp_attack(stored_hash):
    print(Fore.YELLOW + "\n[*] Running CUPP targeted attack..." + Style.RESET_ALL)
    print("--- Target Profile ---")

    # Collect target information — all fields optional except first name
    first_name = input("First name: ")
    last_name = input("Last name (optional): ")
    birth_year = input("Birth year (optional): ")
    pet_name = input("Pet name (optional): ")
    keywords = input("Keywords, comma separated (optional): ")

    # Split keywords into individual items, stripping whitespace
    keyword_list = [k.strip() for k in keywords.split(",") if k.strip()]

    # Build base word list from provided profile fields
    possible_passwords = []
    bases = [first_name.lower(), first_name.upper(), first_name.title()]
    if last_name:
        bases.extend([last_name.lower(), last_name.upper(), last_name.title()])
    if pet_name:
        bases.extend([pet_name.lower(), pet_name.upper(), pet_name.title()])
    for keyword in keyword_list:
        bases.extend([keyword.lower(), keyword.upper(), keyword.title()])

    # Generate leet speak variations for every base word and add to bases
    leet_bases = []
    for base in bases:
        leet_bases.extend(leet_speak(base))
    bases.extend(leet_bases)

    # Common suffixes and prefixes people append to passwords
    suffixes = [birth_year, "123", "1234", "!", "!!", "?", ".", "#"]

    # Combine every base with every suffix in both orders
    for base in bases:
        for suffix in suffixes:
            possible_passwords.append(base + suffix)
            possible_passwords.append(suffix + base)
    
    # Deduplicate — many combinations produce identical strings
    possible_passwords = list(set(possible_passwords))
    print(Fore.YELLOW + f"\n[*] Generated {len(possible_passwords)} candidates from profile..." + Style.RESET_ALL)
    
    # Run each candidate through verify — same core loop as all other attack modes
    for guess in tqdm(possible_passwords, total=len(possible_passwords)):
        if verify(guess, stored_hash):
            print(Fore.GREEN + f"Password found: {guess}" + Style.RESET_ALL)
            return True

    print(Fore.RED + "Target profile exhausted, no match found" + Style.RESET_ALL)
    return False