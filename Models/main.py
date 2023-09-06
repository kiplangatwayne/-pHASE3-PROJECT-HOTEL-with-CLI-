from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import click

# Database Configuration
DATABASE_URL = "sqlite:///hotel_booking.db"  # SQLite database
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define User Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)

# Define Reservation Model
class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))

# Define Hotel Model
class Hotel(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    rating = Column(Float)
    city_id = Column(Integer, ForeignKey("cities.id"))
    rooms = relationship("Room", back_populates="hotel")

# Define Room Model
class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    price = Column(Float)
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    hotel = relationship("Hotel", back_populates="rooms")

# Define City Model
class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    hotels = relationship("Hotel", back_populates="city")

# Create tables
Base.metadata.create_all(engine)

@click.command()
@click.option("--name", prompt="User's Full Name", help="User's Full Name")
@click.option("--username", prompt="Username", help="Username")
@click.option("--email", prompt="Email", help="Email")
@click.option("--password", prompt="Password", hide_input=True, help="Password")
@click.option("--role", type=click.Choice(["user", "admin"]), default="user", help="User Role (user/admin)")
def add_user(name, username, email, password, role):
    """Add a new user to the database."""
    session = Session()
    user = User(name=name, username=username, email=email, password=password, role=role)
    session.add(user)
    session.commit()
    session.close()
    print("User added successfully!")

@click.command()
@click.option("--name", prompt="City Name", help="City's Name")
def add_city(name):
    """Add a new city."""
    session = Session()
    city = City(name=name)
    session.add(city)
    session.commit()
    session.close()
    print("City added successfully!")

def print_user_details(username):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if user:
        print(f"User ID: {user.id}")
        print(f"Name: {user.name}")
        print(f"Email: {user.email}")
        print(f"Role: {user.role}")
    else:
        print(f"User with username '{username}' not found.")
    session.close()




def print_city_reservations(city_name):
    session = Session()
    city = session.query(City).filter_by(name=city_name).first()
    if city:
        print(f"City: {city.name}")
        hotels = city.hotels
        for hotel in hotels:
            print(f"Hotel: {hotel.name}")
            reservations = hotel.reservations
            for reservation in reservations:
                print(f"Reservation Date: {reservation.date}")
                # Add more reservation details here if needed
    else:
        print(f"City '{city_name}' not found.")
    session.close()

def print_room_types(hotel_name):
    session = Session()
    hotel = session.query(Hotel).filter_by(name=hotel_name).first()
    if hotel:
        print(f"Hotel: {hotel.name}")
        rooms = hotel.rooms
        for room in rooms:
            print(f"Room Type: {room.name}")
            print(f"Description: {room.description}")
            print(f"Price: {room.price}")
            # Add more room details here if needed
    else:
        print(f"Hotel '{hotel_name}' not found.")
    session.close()

if __name__ == "__main__":
    choice = input("What do you want to do (add_user/add_city/print_user/print_city/print_room)? ").strip().lower()
    if choice == "add_user":
        add_user()
    elif choice == "add_city":
        add_city()
    elif choice == "print_user":
        username = input("Enter the username: ").strip()
        print_user_details(username)
    elif choice == "print_city":
        city_name = input("Enter the city name: ").strip()
        print_city_reservations(city_name)
    elif choice == "print_room":
        hotel_name = input("Enter the hotel name: ").strip()
        print_room_types(hotel_name)
    else:
        print("Invalid choice. Please choose 'add_user', 'add_city', 'print_user', 'print_city', or 'print_room'.")
