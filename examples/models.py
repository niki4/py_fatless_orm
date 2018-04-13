from lib.model import Base


class User(Base):

    __tablename__ = 'users'

    id = (int, 'required')
    username = (str, 'not_required')
