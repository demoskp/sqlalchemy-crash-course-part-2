from start.main import session
from start.models.user import User

user = User.query.first()

print(user)


session.delete(user)
session.commit()


user = User.query.first()

print(user)