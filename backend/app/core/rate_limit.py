from .redis import redis_client
from fastapi import Request,HTTPException,status
from dotenv import load_dotenv
from os import getenv
load_dotenv()



def rate_limit(req:Request):
    
    client_ip = req.client.host
    
    key = f"rate_limit:{client_ip}"
    
    try:
        curr = redis_client.incr(key)
    except Exception:
        pass  # failed to execute api endpoint
    
    # after 1 request adding ttl (`RATE_LIMIT_KEY_TTL` seconds)
    if(curr == 1):
        redis_client.expire(key,int(getenv("RATE_LIMIT_KEY_TTL")))
    
    # if bigger than `RATE_LIMIT` than throw 429 exception
    
    if(curr > int(getenv("RATE_LIMIT"))):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,detail="Too many requests")