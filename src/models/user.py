from enum import Enum
from uuid import UUID

from pydantic import BaseModel, field_validator, EmailStr

from models import DBBaseModel, RolResponseModel
from models.person import PersonInsertModel, PersonModel, PersonResponseModel


class UserRole(str, Enum):
    """Enum for user roles"""

    ADMIN = "admin"
    CUSTOMER = "customer"


class UserStatus(str, Enum):
    """Enum for user status"""

    ACTIVE = "active"
    SUSPENDED = "suspended"


class UserTokenData(BaseModel):
    """User token data"""

    uuid: str
    role: UserRole
    email: EmailStr


class UserResponseModel(BaseModel):
    """User model for response"""

    email: EmailStr
    rol: RolResponseModel | int
    person: PersonResponseModel | None | int = None


class UserResponseModelBD(BaseModel):
    """User model for response"""

    email: EmailStr
    rol: RolResponseModel | int
    person: PersonModel


class UserBaseModel(UserResponseModel):
    """User model for insert"""

    status: UserStatus = UserStatus.ACTIVE


class UserInsertModel(UserBaseModel, PersonInsertModel):
    """User model for insert"""

    password: str

    @field_validator("password")
    def password_validator(cls, password):
        """
        Validates that the password is at least 8 characters long,
        contains at least one uppercase letter, one lowercase letter,
        one number, and one special character.
        """
        special_chars = {
            "!",
            "@",
            "#",
            "$",
            "%",
            "^",
            "&",
            "*",
            "(",
            ")",
            "-",
            "+",
            "=",
        }
        if len(password) < 8:
            raise ValueError("password must be at least 8 characters long")
        if not any(char.isupper() for char in password):
            raise ValueError("password must contain at least one uppercase letter")
        if not any(char.islower() for char in password):
            raise ValueError("password must contain at least one lowercase letter")
        if not any(char.isdigit() for char in password):
            raise ValueError("password must contain at least one number")
        if not any(char in special_chars for char in password):
            raise ValueError("password must contain at least one special character")
        return password

    def create_db_entity(self, password_hash: str):
        """
        Creates a db entity from the insert model
        """
        from data_adapter.user import User

        """ Person field """

        dict_to_build_db_entity = self.model_dump()
        dict_to_build_db_entity.pop("name")
        dict_to_build_db_entity.pop("last_name")
        dict_to_build_db_entity.pop("age")
        dict_to_build_db_entity.pop("phone_number")
        dict_to_build_db_entity.pop("gender")

        """ User Field """

        dict_to_build_db_entity["password_hash"] = password_hash
        dict_to_build_db_entity["role_id"] = self.rol
        dict_to_build_db_entity["person_id"] = self.person

        dict_to_build_db_entity.pop("person")
        dict_to_build_db_entity.pop("rol")

        dict_to_build_db_entity.pop("password")
        return User(**dict_to_build_db_entity)


class UserModel(UserBaseModel, DBBaseModel):
    """User model"""

    password_hash: str
    person: PersonModel

    class Config:
        from_attributes = True

    def build_user_token_data(self) -> dict:
        """
        Builds the user token data
        :return: dict
        """
        res_dict = self.model_dump()
        res_dict["uuid"] = str(self.uuid)
        return UserTokenData.model_validate(res_dict).model_dump()

    def build_response_model(self) -> UserResponseModel:
        return UserResponseModel.model_validate(self.model_dump())


class UserLoginModel(BaseModel):
    """User logincart model"""

    email: EmailStr
    password: str


class TokenType(str, Enum):
    bearer = "bearer"


class UserTokenResponseModel(BaseModel):
    """User token model"""

    user_uuid: UUID
    access_token: str
    token_type: TokenType = TokenType.bearer
    user_role: UserRole
    user_status: UserStatus
