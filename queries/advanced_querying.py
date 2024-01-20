from sqlalchemy import column
from sqlalchemy import func
from models import User, Drive, Distance, Economy, Role

# users_with_new_column = (
#     User
#     .query
#     .add_columns(column("id"))
#     .all()
# )
#
# first_result = users_with_new_column[0]
# user = first_result[0]
# user_id = first_result.id
#
# print(user.email)
# print(user_id)


# users_with_drive_count = (
#     User
#     .query
#     .join(User.drives)
#     .add_columns(func.count(Drive.id).label("drive_count"))
#     .group_by(User.id)
#     .all()
# )
#
# print(users_with_drive_count)


# users_with_avg_drive_distance = (
#     User
#     .query
#     .join(User.drives)
#     .join(Drive.distance)
#     .where(Distance.value != None)
#     .add_columns(func.avg(Distance.value).label("avg_drive_distance"))
#     .group_by(User.id)
#     .all()
# )
#
# print(users_with_avg_drive_distance)

# users_with_avg_drive_distance_including_null = (
#     User
#     .query
#     .join(User.drives)
#     .join(Drive.distance)
#     .add_columns(func.avg(func.coalesce(Distance.value, 0)).label("avg_drive_distance"))
#     .group_by(User.id)
#     .all()
# )
#
# print(users_with_avg_drive_distance_including_null)

users_with_total_distance_driven = (
    User
    .query
    .join(User.drives)
    .join(Drive.distance)
    .add_columns(func.sum(Distance.value).label("total_distance_driven"))
    .group_by(User.id)
    .all()
)

print(users_with_total_distance_driven)


# wrong! values are calculated multiple times because of another join
# users_with_total_distance_driven = (
#     User
#     .query
#     .join(User.drives)
#     .join(User.roles)
#     .join(Drive.distance)
#     .add_columns(func.sum(Distance.value).label("total_distance_driven"))
#     .group_by(User.id)
#     .all()
# )
#
# print(users_with_total_distance_driven)


subquery = (
    Drive
    .query
    .join(Drive.distance)
    .with_entities(
        func.sum(Distance.value).label("total_distance_driven"),
        Drive.user_id.label("user_id")
    )
    .group_by(Drive.user_id)
    .subquery()
)

users_with_total_distance_driven = (
    User
    .query
    .join(User.roles)
    .join(subquery, User.id == subquery.c.user_id)
    .add_columns(subquery.c.total_distance_driven)
    .all()
)

print(users_with_total_distance_driven)
