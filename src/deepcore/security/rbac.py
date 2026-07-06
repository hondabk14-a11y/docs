from typing import List, Dict
from fastapi import HTTPException

# Simple role model for DeepCore Systems Enterprise
# In production, this would be backed by a policy engine (OPA / Cedar)

ROLES: Dict[str, List[str]] = {
    "admin": ["*"],
    "operator": ["read", "ingest", "replay"],
    "viewer": ["read"],
}


def check_permission(user_role: str, action: str):
    allowed = ROLES.get(user_role)

    if not allowed:
        raise HTTPException(status_code=403, detail="Unknown role")

    if "*" in allowed:
        return True

    if action not in allowed:
        raise HTTPException(status_code=403, detail="Permission denied")

    return True


def require_role(required_roles: List[str]):
    def decorator(func):
        def wrapper(*args, **kwargs):
            role = kwargs.get("role", "viewer")

            if role not in required_roles:
                raise HTTPException(status_code=403, detail="Insufficient role")

            return func(*args, **kwargs)
        return wrapper

    return decorator
