from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.orm import Session
from data_adapter.db import DBBase, DBBaseModel
from models.user import UserModel, UserStatus, UserRole
from models.person import PersonInsertModel, PersonModel
from sqlalchemy.orm import relationship
from data_adapter.base_tables import Gender, Rol


class Person(DBBase, DBBaseModel):
    __tablename__ = "person"

    name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    age = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=False)
    gender_id = Column(Integer, ForeignKey("genders.id"))
    gender = relationship("Gender")

    def __to_model(self) -> PersonModel:
        """converts db orm object to pydantic model"""
        return PersonModel.model_validate(self)

    @classmethod
    def create_person(cls, person: PersonInsertModel) -> PersonModel:
        from controller import get_db_session

        person = person.create_db_entity()
        db: Session = get_db_session()
        db.add(person)
        db.flush()
        return person.__to_model()


class User(DBBase, DBBaseModel):
    __tablename__ = "user"

    email = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("rol.id"))
    rol = relationship("Rol")
    person_id = Column(Integer, ForeignKey("person.id"))
    person = relationship("Person")
    password_hash = Column(String(255), nullable=False)
    status = Column(String(20), nullable=False)

    def __to_model(self) -> UserModel:
        """converts db orm object to pydantic model"""
        return UserModel.model_validate(self)

    @classmethod
    def create_user(cls, user) -> UserModel:
        from controller import get_db_session

        db: Session = get_db_session()
        db.add(user)
        db.flush()

        return user.__to_model()

    @classmethod
    def get_by_id(cls, id) -> UserModel:
        user = super().get_by_id(id)
        return user.__to_model() if user else None

    @classmethod
    def get_by_uuid(cls, uuid) -> UserModel:
        user = super().get_by_uuid(uuid)
        return user.__to_model() if user else None

    @classmethod
    def get_active_user_by_email(cls, email) -> UserModel:
        from controller import get_db_session

        db = get_db_session()
        user = (
            db.query(cls)
            .filter(
                cls.email == email,
                cls.status == UserStatus.ACTIVE,
                cls.is_deleted.is_(False),
            )
            .first()
        )
        return user.__to_model() if user else None

    @classmethod
    def update_user_by_uuid(
        cls, user_uuid: str, update_dict: dict, user_role: UserRole = None
    ) -> int:
        from controller import get_db_session

        db = get_db_session()
        update_query = db.query(cls).filter(
            cls.uuid == user_uuid, cls.is_deleted.is_(False)
        )
        if user_role:
            update_query = update_query.filter(cls.role == user_role)
        updates = update_query.update(update_dict)
        db.flush()
        return updates

    @classmethod
    def list_user(cls):
        from controller import get_db_session

        db = get_db_session()
        users = db.query(cls).all()

        return [x.__to_model() for x in users]
