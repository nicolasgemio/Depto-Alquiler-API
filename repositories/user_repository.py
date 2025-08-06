from models.user import User
from database import SessionLocal

class UserRepository:
    def __init__(self):
        pass
    
    def get_by_google_id(self, google_id: str) -> dict:
        with SessionLocal() as db:
            try:
                user_doc = db.query(User).filter(User.google_id == google_id).first()

                if not user_doc:
                    return None

                return user_doc
            except Exception as e:
                db.rollback()
                print(f"Error al remover el departamento: {e}")
                raise
        
    def create_user(self, new_user: User) -> User:
        with SessionLocal() as db:
            try:
                db.add(new_user)
                db.commit()
                db.refresh(new_user)

                return new_user
            except Exception as e:
                db.rollback()
                print(f"Error al remover el departamento: {e}")
                raise

    # def update_last_login(self, uid: str):
    #     self.collection.document(uid).update({
    #         "last_login": firestore.SERVER_TIMESTAMP
    #     })
