from .models import Account

accounts = {}

def reset_state():
    accounts.clear()

def get_account_balance(account_id: str):
    if account_id in accounts:
        return accounts[account_id]
    return None

def create_or_update_account(account_id: str, amount: int):
    if account_id in accounts:
        accounts[account_id].balance += amount
    else:
        accounts[account_id] = Account(id=account_id, balance=amount)
    return accounts[account_id]

def withdraw_from_account(account_id: str, amount: int):
    if account_id not in accounts or accounts[account_id].balance < amount:
        return None
    accounts[account_id].balance -= amount
    return accounts[account_id]

def transfer_between_accounts(origin_id: str, destination_id: str, amount: int):
    if origin_id not in accounts or accounts[origin_id].balance < amount:
        return None, None
    accounts[origin_id].balance -= amount
    return withdraw_from_account(origin_id, amount), create_or_update_account(destination_id, amount)
