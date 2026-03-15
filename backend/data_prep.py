#Script for sample data upload to Redis for the demo
import redis
import json

# Connect to Redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

accounts = {
    "1234567890": {
        "first_name": "Jane",
        "last_name": "Doe",
        "type": "Current",
        "balance": 1000,
        "currency": "NAD",
        "status": "ACTIVE"
    },
    "1234567892": {
        "first_name": "John",
        "last_name": "Wick",
        "type": "Savings",
        "balance": 150,
        "currency": "NAD",
        "status": "ACTIVE"
    },
    "0987654321": {
        "first_name": "Herman",
        "last_name": "Kandjimi",
        "type": "Fixed",
        "balance": 13100800,
        "currency": "NAD",
        "status": "ACTIVE"
    },
    "9987654321": {
        "first_name": "Leena",
        "last_name": "Kandjimi",
        "type": "Business",
        "balance": 24000,
        "currency": "NAD",
        "status": "ACTIVE"
    }
}

def load_accounts_to_redis():

    for account_number, data in accounts.items():
        #Use account number as redis key
        redis_key = f"{account_number}"

        r.hset(redis_key, mapping=data)

        print(f"Loaded {redis_key}")

    print("All accounts loaded into Redis")


if __name__ == "__main__":
    load_accounts_to_redis()