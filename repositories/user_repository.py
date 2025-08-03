from firebase_admin import firestore
from dtos.user_dto import UserDto
from firebase_admin import credentials, firestore
from models.user import User
from database import SessionLocal

class UserRepository:
    def __init__(self):
        self.db = firestore.client()

        self.collection = self.db.collection("users")

    def get_by_uid(self, uid: str) -> UserDto | None:
        doc = self.collection.document(uid).get()
        if doc.exists:
            return UserDto(**doc.to_dict())
        return None
    
    def get_by_google_id(self, google_id: str) -> dict:
        try:
            db = SessionLocal()
            user_doc = db.query(User).filter(User.google_id == google_id).first()

            if not user_doc:
                return None

            return user_doc
        except Exception as e:
            db.rollback()
            print(f"Error al remover el departamento: {e}")
            raise
        
    
    def create_user(self, new_user: User) -> User:
        db = SessionLocal()

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    def update_last_login(self, uid: str):
        self.collection.document(uid).update({
            "last_login": firestore.SERVER_TIMESTAMP
        })

    def upsert_user(self, user_data: dict) -> UserDto:
        existing = self.get_by_uid(user_data["uid"])
        if existing:
            self.collection.document(user_data["uid"]).update({
                "email": user_data["email"],
                "name": user_data["name"],
                "picture": user_data.get("picture"),
                "last_login": firestore.SERVER_TIMESTAMP
            })
            return self.get_by_uid(user_data["uid"])
        else:
            return self.create_user(user_data)
