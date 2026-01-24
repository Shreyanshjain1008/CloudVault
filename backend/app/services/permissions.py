from fastapi import HTTPException

def check_permission(role: str, action: str):
    permissions = {
        "owner": ["read", "write", "delete"],
        "editor": ["read", "write"],
        "viewer": ["read"]
    }

    if action not in permissions.get(role, []):
        raise HTTPException(status_code=403, detail="Permission denied")
