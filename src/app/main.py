from fastapi import FastAPI, HTTPException, status
from .models import Transaction
from . import core

app = FastAPI()

@app.post("/reset", status_code=status.HTTP_200_OK)
def reset_state():
    core.reset_state()  
    return {"detail": "State reset successfully"}

@app.get("/balance")
def get_balance(account_id: str):
    account = core.get_account_balance(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account.balance

@app.post("/event", status_code=201)
def post_event(transaction: Transaction):
    if transaction.type == "deposit":
        account = core.create_or_update_account(transaction.destination, transaction.amount)
        return {"destination": account}
    elif transaction.type == "withdraw":
        account = core.withdraw_from_account(transaction.origin, transaction.amount)
        if account is None:
            raise HTTPException(status_code=404, detail="Insufficient funds or account not found")
        return {"origin": account}
    elif transaction.type == "transfer":
        origin, destination = core.transfer_between_accounts(transaction.origin, transaction.destination, transaction.amount)
        if origin is None or destination is None:
            raise HTTPException(status_code=404, detail="Insufficient funds or account not found")
        return {"origin": origin, "destination": destination}
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")
