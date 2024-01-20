from random import randint, choice

from main import session
from models.drive import Unit, Drive, Distance, Duration, Economy
from models.user import User, Address, Preference, Role

role_data = [
    {"name": "Administrator", "slug": "admin"},
    {"name": "Super Administrator", "slug": "super-admin"},
]

unit_data = [
    {"name": "Miles", "slug": "miles"},
    {"name": "Kilometers", "slug": "kilometers"},
    {"name": "Miles Per Gallon", "slug": "miles-per-gallon"},
    {"name": "Liters Per 100KM", "slug": "liters-per-100km"},
    {"name": "Seconds", "slug": "seconds"},
    {"name": "Minutes", "slug": "minutes"},
]

user_data = [
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@gmail.com",
        "addresses": [
            {
                "road_name": "123 Main St",
                "postcode": "12345",
                "city": "London",
            },
            {
                "road_name": "456 Maple Ave",
                "postcode": "67890",
                "city": "Cambridge",
            }
        ],
        "preference": {
            "currency": "USD",
            "language": "English"
        }
    },
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "janesmith@gmail.com",
        "addresses": [
            {
                "road_name": "789 Oak St",
                "postcode": "54321",
                "city": "Paris",
            },
            {
                "road_name": "321 Elm St",
                "postcode": "09876",
                "city": "Lyon",
            }
        ],
        "preference": {
            "currency": "EUR",
            "language": "German"
        }
    },
    {
        "first_name": "Bob",
        "last_name": "Johnson",
        "email": "bobjohnson@gmail.com",
        "addresses": [
            {
                "road_name": "555 Cedar St",
                "postcode": "11111",
                "city": "Berlin",
            },
            {
                "road_name": "777 Pine St",
                "postcode": "22222",
                "city": "Frankfurt",
            }
        ],
        "preference": {
            "currency": "JPY",
            "language": "Japanese"
        }
    },
    {
        "first_name": "Alice",
        "last_name": "Lee",
        "email": "alicelee@example.com",
        "addresses": [
            {
                "road_name": "999 Birch Rd",
                "postcode": "33333",
                "city": "San Diego",
            },
            {
                "road_name": "222 Maple Rd",
                "postcode": "44444",
                "city": "Sacramento",
            }
        ],
        "preference": {
            "currency": "GBP",
            "language": "English"
        }
    },
    {
        "first_name": "David",
        "last_name": "Kim",
        "email": "davidkim@example.com",
        "addresses": [
            {
                "road_name": "444 Cherry Ln",
                "postcode": "55555",
                "city": "Porto",
            },
            {
                "road_name": "888 Pine Ln",
                "postcode": "66666",
                "city": "Lisbon",
            }
        ],
        "preference": {
            "currency": "AUD",
            "language": "English"
        }
    },
    {
        "first_name": "Emily",
        "last_name": "Nguyen",
        "email": "emilynguyen@example.com",
        "addresses": [
            {
                "road_name": "777 Oak Blvd",
                "postcode": "77777",
                "city": "Warsaw",
            },
            {
                "road_name": "333 Maple Blvd",
                "postcode": "88888",
                "city": "Kraków",
            }
        ],
        "preference": {
            "currency": "USD",
            "language": "Vietnamese"
        }
    },
    {
        "first_name": "Michael",
        "last_name": "Davis",
        "email": "michaeldavis@example.com",
        "addresses": [
            {
                "road_name": "111 Elm Blvd",
                "postcode": "99999",
                "city": "Birmingham",
            },
            {
                "road_name": "444 Oak Blvd",
                "postcode": "00000",
                "city": "London",
            }
        ],
        "preference": {
            "currency": "EUR",
            "language": "English"
        }
    }
]

for role in role_data:
    session.add(Role(**role))

session.commit()

roles = Role.query.all()

for unit in unit_data:
    session.add(Unit(**unit))

session.commit()

units = Unit.query.all()
miles_unit = next(filter(lambda un: un.slug == "miles", units), None)
mpg_unit = next(filter(lambda un: un.slug == "miles-per-gallon", units), None)
minutes_unit = next(filter(lambda un: un.slug == "minutes", units), None)

users = []

for i, u in enumerate(user_data):
    user = User()
    user.first_name = u.get("first_name")
    user.last_name = u.get("last_name")
    user.email = u.get("email")

    addresses = []
    for address in u.get("addresses"):
        addresses.append(Address(**address))

    user.addresses.extend(addresses)
    user.preference = Preference(**u.get("preference"))
    user.roles = roles
    drives = []

    if i % 2 == 0:
        for _ in range(randint(2, 10)):
            distance = Distance(value=choice([randint(30, 300), None]), unit=miles_unit)
            duration = Duration(value=choice([randint(30, 90), None]), unit=minutes_unit)
            economy = Economy(value=randint(30, 90), unit=mpg_unit)
            drive = Drive(distance=distance, economy=economy, duration=duration)
            drives.append(drive)

    user.drives = drives

    users.append(user)

session.add_all(users)
session.commit()

