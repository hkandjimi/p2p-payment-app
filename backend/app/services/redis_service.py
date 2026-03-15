import redis
import json

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)


def account_exists(account_number: str) -> bool:
    key = f"{account_number}"
    return redis_client.exists(key) == 1


def get_account_details(account_number: str):
    key = f"{account_number}"
    return redis_client.hgetall(key)


def get_balance(account_number: str) -> float:
    key = f"{account_number}"
    balance = redis_client.hget(key, "balance")

    if balance is None:
        return 0

    return float(balance)


def update_balance(account_number: str, new_balance: float):
    key = f"{account_number}"
    redis_client.hset(key, "balance", new_balance)

# def save_account(account, data):
#     redis_client.set(account, json.dumps(data))

# def account_exists(account):
#     return redis_client.exists(account)

# def get_account_details(account):
#     data = redis_client.get(account)
#     if data:
#         return json.loads(data)
#     return None
