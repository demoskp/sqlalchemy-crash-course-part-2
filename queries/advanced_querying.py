from operator import and_

from sqlalchemy import column, case
from sqlalchemy import func
from sqlalchemy.orm import aliased

from models import User, Drive, Distance, Economy, Role, Duration, Unit

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
#
#
# all_users_with_drive_count = (
#     User
#     .query
#     .outerjoin(User.drives)
#     .add_columns(func.count(Drive.id).label("drive_count"))
#     .group_by(User.id)
#     .all()
# )
#
# print(all_users_with_drive_count)


# users_with_avg_drive_distance = (
#     User
#     .query
#     .outerjoin(User.drives)
#     .outerjoin(Drive.distance)
#     .add_columns(func.avg(Distance.value).label("avg_drive_distance"))
#     .group_by(User.id)
#     .all()
# )
#
# print(users_with_avg_drive_distance)

# users_with_avg_drive_distance_or_0 = (
#     User
#     .query
#     .outerjoin(User.drives)
#     .outerjoin(Drive.distance)
#     .add_columns(func.avg(func.coalesce(Distance.value, 0)).label("avg_drive_distance"))
#     .group_by(User.id)
#     .all()
# )
#
# print(users_with_avg_drive_distance_or_0)

# users_with_total_distance_driven = (
#     User
#     .query
#     .outerjoin(User.drives)
#     .outerjoin(Drive.distance)
#     .add_columns(func.coalesce(func.sum(Distance.value), 0).label("total_distance_driven"))
#     .group_by(User.id)
#     .all()
# )
#
# print(users_with_total_distance_driven)


# wrong! values are calculated multiple times because of another join
# users_with_total_distance_driven = (
#     User
#     .query
#     .outerjoin(User.drives)
#     .outerjoin(User.roles)
#     .outerjoin(Drive.distance)
#     .add_columns(func.coalesce(func.sum(Distance.value), 0).label("total_distance_driven"))
#     .group_by(User.id)
#     .all()
# )
#
# print(users_with_total_distance_driven)


# subquery = (
#     User.
#     query
#     .outerjoin(User.drives)
#     .outerjoin(Drive.distance)
#     .with_entities(
#         func.coalesce(func.sum(Distance.value), 0).label("total_distance_driven"),
#         User.id.label("user_id")
#     )
#     .group_by(User.id)
#     .subquery()
# )
#
# users_with_total_distance_driven = (
#     User
#     .query
#     .outerjoin(User.roles)
#     .outerjoin(subquery, User.id == subquery.c.user_id)
#     .add_columns(subquery.c.total_distance_driven)
#     .all()
# )
#
# print(users_with_total_distance_driven)


# subquery = (
#     User
#     .query
#     .outerjoin(User.drives)
#     .outerjoin(Drive.distance)
#     .outerjoin(Drive.duration)
#     .with_entities(
#         case(
#             (
#                 # func.sum(Distance.value) & func.sum(Duration.value),
#                 and_(func.sum(Distance.value), func.sum(Duration.value)),
#                 func.sum(Distance.value) / (func.sum(Duration.value) / 60)
#             ),
#             else_=0
#         ).label("mph"),
#         User.id.label("user_id")
#     )
#     .group_by(User.id)
#     .subquery()
# )
#
# users_with_average_drive_speed = (
#     User
#     .query
#     .join(User.roles)
#     .outerjoin(subquery, User.id == subquery.c.user_id)
#     .add_columns(subquery.c.mph)
#     .all()
# )
#
# print(users_with_average_drive_speed)

distance_unit = aliased(Unit)
duration_unit = aliased(Unit)

subquery = (
    User
    .query
    .outerjoin(User.drives)
    .outerjoin(Drive.distance)
    .outerjoin(Drive.duration)
    .outerjoin(
        distance_unit,
        and_(distance_unit.id == Distance.unit_id, distance_unit.slug == "miles")
    )
    .outerjoin(
        duration_unit,
        and_(duration_unit.id == Duration.unit_id, duration_unit.slug == "minutes")
    )
    .with_entities(
        case(
            (
                func.sum(Distance.value) & func.sum(Duration.value),
                func.sum(Distance.value) / (func.sum(Duration.value) / 60)
            ),
            else_=0
        ).label("mph"),
        User.id.label("user_id")
    )
    .group_by(User.id)
    .subquery()
)

users_with_average_drive_speed = (
    User
    .query
    .join(User.roles)
    .outerjoin(subquery, User.id == subquery.c.user_id)
    .add_columns(subquery.c.mph)
    .all()
)

print(users_with_average_drive_speed)
