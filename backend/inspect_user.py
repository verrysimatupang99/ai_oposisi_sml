from app.core.database import SessionLocal
from app.models.user import User

db = SessionLocal()
user = db.query(User).filter(User.username == "testuser2").first()
if user:
    print(f"Username: {user.username}")
    print(f"Hashed Password Type: {type(user.hashed_password)}")
    print(f"Hashed Password: {user.hashed_password}")
else:
    print("User not found")
db.close()
