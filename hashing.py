import hashlib

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
