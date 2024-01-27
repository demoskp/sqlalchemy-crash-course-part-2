from sqlalchemy.orm import joinedload

from completed.models.user import User, Address

users = (
    User.query
    .join(User.addresses)
    .filter(Address.city == "London")
    .options(joinedload(User.addresses))
    .all()
)

for user in users:
    print(user.addresses)