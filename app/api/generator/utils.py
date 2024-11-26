import random
import string

from app.service import RedisConnection

# Function to generate a fixed shuffled pool of characters
def get_shuffled_pool(seed):
    char_pool = list(string.ascii_letters + string.digits)
    random.seed(seed)
    random.shuffle(char_pool)
    return char_pool

# Pre-generate character pools for different lengths using fixed seeds
char_pools = {
    # 1: get_shuffled_pool(seed=42),
    # 2: get_shuffled_pool(seed=43),
    # 3: get_shuffled_pool(seed=44),
    # 4: get_shuffled_pool(seed=45),
    5: get_shuffled_pool(seed=46),
    6: get_shuffled_pool(seed=47),
}

# Function to generate a unique string of a given length for a specific index
async def generate_unique_string(index, length=5):
    if length not in char_pools:
        raise ValueError("Length must be either 5 and 6")
    
    pool = char_pools[length]
    pool_size = len(pool)
    
    # Ensure the index is within the valid range for the given length
    if index > pool_size ** length:
        raise ValueError("Index out of range for unique string generation")

    # Generate the unique string
    result = []
    current_index = index
    for _ in range(length):
        result.append(pool[current_index % pool_size])
        current_index //= pool_size
    return ''.join(result)


async def redis_incre_counter(key_length):
    redis_client = RedisConnection().redis_connection()
    redis_key = f'counter_{key_length}'
    return redis_client.incr(redis_key)