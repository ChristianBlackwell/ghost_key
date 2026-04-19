import sys
import string
from colorama import Fore, Style, init # type: ignore
init()
from hashing import string_to_md5_hash, string_to_sha256_hash
from attacks import dictionary_attack, brute_force_attack, cupp_attack

#stored_md5_hash = string_to_md5_hash("password123")
#stored_sha256_hash = string_to_sha256_hash("password123")

def main():
    # Collect target hash from user
    stored_hash = input("Enter target hash (or press enter to generate one): ").strip()

    if not stored_hash:
        password = input("Enter a password to hash: ")
        algo = input("Hash algorithm - MD5 or SHA256? (m/s): ").strip().lower()
        if algo == "s":
            stored_hash = string_to_sha256_hash(password)
            print(Fore.YELLOW + f"Generated SHA256 hash: {stored_hash}" + Style.RESET_ALL)
        else:
            stored_hash = string_to_md5_hash(password)
            print(Fore.YELLOW + f"Generated MD5 hash: {stored_hash}" + Style.RESET_ALL)
        
    # Check if user has target information for CUPP
    use_cupp = input("\nDo you have target information? (y/n): ")
    if use_cupp.lower() == "y":
        result = cupp_attack(stored_hash)
        if result:
            return 0
    
    # Fall back to dictionary
    result = dictionary_attack(stored_hash)
    if result:
        return 0
    
    # Last resort brute force
    brute_force_attack(stored_hash, string.ascii_lowercase, 1, 5)
    return 0

if __name__ == "__main__":
    # This block only runs if the script is executed directly
    sys.exit(main())