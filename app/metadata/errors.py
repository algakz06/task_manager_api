from fastapi import HTTPException


NoTaskFound = HTTPException(status_code=404, detail="task with that id not found")
NoExtensionSupported = HTTPException(status_code=415, detail="only .jpg files supported")

class TokenExpired(Exception):
    pass
