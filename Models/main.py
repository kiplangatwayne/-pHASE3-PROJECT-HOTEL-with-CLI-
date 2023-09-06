import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from user import User  # Import the User model (update the import path as needed)
from city import City  # Import the City model
from Hotel import Hotel  # Import the Hotel model
from Room_type import RoomType  # Import the Room Type model

# Database Configuration
DATABASE_URL = "sqlite:///hotel_booking.db"  # SQLite database (update as needed)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@click.group()
def cli():
    """Hotel Booking CLI Application"""
    pass

@cli.command()
@click.option("--name", prompt="User's Full Name", help="User's Full Name")
@click.option("--username", prompt="Username", help="Username")
@click.option("--email", prompt="Email", help="Email")
@click.option("--password", prompt="Password", hide_input=True, help="Password")
@click.option("--role", type=click.Choice(["user", "admin"]), help="User Role (user/admin)")
def add_user(name, username, email, password, role):
    """Add a new user to the database."""
    session = Session()
    user = User(name=name, username=username, email=email, password=password, role=role)
    session.add(user)
    session.commit()
    session.close()
    print("User added successfully!")

@cli.command()
@click.option("--name", prompt="City Name", help="City Name")
def add_city(name):
    """Add a new city to the database."""
    session = Session()
    city = City(name=name)
    session.add(city)
    session.commit()
    session.close()
    print("City added successfully!")

@cli.command()
@click.option("--name", prompt="Hotel Name", help="Hotel Name")
@click.option("--city", prompt="City Name", help="City Name")
@click.option("--room-types", prompt="Room Types (comma-separated)", help="Room Types")
def add_hotel(name, city, room_types):
    """Add a new hotel to the database."""
    session = Session()
    city_obj = session.query(City).filter_by(name=city).first()
    if city_obj:
        room_type_names = [rt.strip() for rt in room_types.split(",")]
        hotel = Hotel(name=name, city_id=city_obj.id)
        for room_type_name in room_type_names:
            room_type = session.query(RoomType).filter_by(name=room_type_name).first()
            if room_type:
                hotel.room_types.append(room_type)
        session.add(hotel)
        session.commit()
        session.close()
        print("Hotel added successfully!")
    else:
        print(f"City '{city}' not found.")

@cli.command()
@click.option("--name", prompt="Room Type Name", help="Room Type Name")
def add_room_type(name):
    """Add a new room type to the database."""
    session = Session()
    room_type = RoomType(name=name)
    session.add(room_type)
    session.commit()
    session.close()
    print("Room Type added successfully!")

@cli.command()
@click.option("--city", prompt="City Name", help="City Name")
def search_hotels(city):
    """Search for hotels in a city."""
    session = Session()
    city_obj = session.query(City).filter_by(name=city).first()
    if city_obj:
        hotels = session.query(Hotel).filter_by(city_id=city_obj.id).all()
        session.close()
        if hotels:
            print(f"Hotels in {city}:")
            for hotel in hotels:
                print(f"- {hotel.name}")
        else:
            print(f"No hotels found in {city}.")
    else:
        print(f"City '{city}' not found.")

if __name__ == "__main__":
    cli()
