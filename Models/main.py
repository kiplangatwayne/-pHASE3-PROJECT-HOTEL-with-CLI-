from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
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

# Define Hotel Model
class Hotel(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    rating = Column(Float)
    city_id = Column(Integer, ForeignKey("cities.id"))
    city = relationship("City", backref="hotels")  # Relationship with City
    users = relationship("User", secondary="reservations")  # Relationship with User

# Define City Model
class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

# Define Reservation Model
class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    hotel_id = Column(Integer, ForeignKey("hotels.id"))

# Create tables
Base.metadata.create_all(engine)

def add_user_with_hotel_and_city(name: str, username: str, email: str, password: str, role: str, hotel_name: str, city_name: str) -> None:
    """Add a new user to the database, book a hotel, and add a city."""
    with Session() as session:
        user = User(name=name, username=username, email=email, password=password, role=role)
        session.add(user)

        # Book a hotel
        hotel = session.query(Hotel).filter_by(name=hotel_name).first()
        if hotel:
            user.hotels.append(hotel)
        
        # Add a city
        city = session.query(City).filter_by(name=city_name).first()
        if not city:
            city = City(name=city_name)
            session.add(city)

        session.commit()
    print("User added, hotel booked, and city added successfully!")

@click.command()
@click.option("--name", prompt="User's Full Name", help="User's Full Name")
@click.option("--username", prompt="Username", help="Username")
@click.option("--email", prompt="Email", help="Email")
@click.option("--password", prompt="Password", hide_input=True, help="Password")
@click.option("--role", type=click.Choice(["user", "admin"]), default="user", help="User Role (user/admin)")
@click.option("--hotel_name", prompt="Hotel Name", help="Hotel Name")
@click.option("--city_name", prompt="City Name", help="City Name")
def add_user_book_hotel_add_city(name: str, username: str, email: str, password: str, role: str, hotel_name: str, city_name: str) -> None:
    """Add a new user, book a hotel, and add a city."""
    add_user_with_hotel_and_city(name, username, email, password, role, hotel_name, city_name)

@click.command()
@click.option("--name", prompt="City Name", help="City's Name")
def add_city(name: str) -> None:
    """Add a new city."""
    with Session() as session:
        city = City(name=name)
        session.add(city)
        session.commit()
    print("City added successfully!")

@click.command()
@click.option("--name", prompt="Hotel Name", help="Hotel Name")
@click.option("--description", prompt="Hotel Description", help="Hotel Description")
@click.option("--rating", type=click.FloatRange(0, 5), prompt="Hotel Rating (0-5)", help="Hotel Rating")
@click.option("--city_name", prompt="City Name", help="City Name")
def add_hotel(name: str, description: str, rating: float, city_name: str) -> None:
    """Add a new hotel."""
    with Session() as session:
        city = session.query(City).filter_by(name=city_name).first()
        if city:
            hotel = Hotel(name=name, description=description, rating=rating, city=city)
            session.add(hotel)
            session.commit()
            print("Hotel added successfully!")
        else:
            print(f"City '{city_name}' not found. Please add the city first.")

if __name__ == "__main__":
    choice = input("What do you want to do (add_user/add_city/add_hotel/print_user/print_city)? ").strip().lower()
    if choice == "add_user":
        add_user_book_hotel_add_city()
    elif choice == "add_city":
        add_city()
    elif choice == "add_hotel":
        add_hotel()
    elif choice == "print_user":
        username = input("Enter the username: ").strip()
        # print_user_details(username)
    elif choice == "print_city":
        city_name = input("Enter the city name: ").strip()
        # print_city_reservations(city_name)
    else:
        print("Invalid choice. Please choose 'add_user', 'add_city', 'add_hotel', 'print_user', or ")
