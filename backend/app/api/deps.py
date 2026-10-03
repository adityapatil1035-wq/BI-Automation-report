from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.all_models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login", auto_error=False)

def get_current_user(db: Session = Depends(get_db), token: str | None = Depends(oauth2_scheme)) -> User:
    if token:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id:
                user = db.query(User).filter(User.id == int(user_id)).first()
                if user:
                    return user
        except Exception:
            pass

    # Default fallback user when sign-in is disabled/skipped
    user = db.query(User).first()
    if not user:
        from app.core.security import get_password_hash
        user = User(
            email="admin@biplatform.com",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"),
            role="Admin",
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

