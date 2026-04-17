import time
import itertools
import string
from colorama import Fore, Style, init # type: ignore
from tqdm import tqdm # type: ignore
from hashing import verify

def dictionary_attack(stored_hash):
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
                print(f'Attempts: {attempt_counter}')
                print(f'Time Elapsed: {elapsed_time:.2f} seconds')
                return True
            
        # Only reaches here if entire wordlist exhausted with no match
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(Fore.RED + "Password not found in wordlist" + Style.RESET_ALL)
        print(f"Attempts: {attempt_counter}")
        print(f"Time Elapsed: {elapsed_time:.2f} seconds")
        return False

# You would call brute_force_attack with the char_set, like string.ascii_lowercase and integers for min and max length, starting at 1 (passwords can't be 0)
# example, brute_force_attack(string.ascii_lowercase, 1, 6)
def brute_force_attack(stored_hash, char_set, min_length, max_length):
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
                print(f'Attempts: {attempt_counter}')
                print(f'Time Elapsed: {elapsed_time:.2f} seconds')
                return True
    
    # Only reaches here if search space exhausted with no match
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(Fore.RED + "Password not found in wordlist" + Style.RESET_ALL)
    print(f"Searched: {description_label} lengths {min_length}-{max_length}")
    print(f"Attempts: {attempt_counter}")
    print(f"Time Elapsed: {elapsed_time:.2f} seconds")
    return False
