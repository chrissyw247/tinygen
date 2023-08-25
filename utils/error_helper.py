from fastapi import HTTPException

def raise_standard_error(status_code, message):
    raise HTTPException(status_code=400, detail=message)
