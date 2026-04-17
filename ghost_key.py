import sys
import string
from hashing import string_to_md5_hash, string_to_sha256_hash, verify
from attacks import dictionary_attack, brute_force_attack

stored_md5_hash = string_to_md5_hash("password123")
stored_sha256_hash = string_to_sha256_hash("password123")

def main():
    # Step 1 - CUPP (coming Phase 5)
    # Step 2 - Dictionary
    dictionary_attack(stored_md5_hash)
    # Step 3 - Brute force
    brute_force_attack(stored_md5_hash, string.ascii_lowercase, 1, 5)
    return 0

if __name__ == "__main__":
    # This block only runs if the script is executed directly
    sys.exit(main())
