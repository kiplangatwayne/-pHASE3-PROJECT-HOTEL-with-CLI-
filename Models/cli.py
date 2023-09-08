import argparse
import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import User, City, Hotel, Reservation
# Database Configuration
DATABASE_URL = "sqlite:///hotel_booking.db"  # SQLite database
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
@click.option("--hotel_name", prompt="Hotel Name", help="Hotel Name")
@click.option("--city_name", prompt="City Name", help="City Name")
def add_user(name, username, email, password, role, hotel_name, city_name):
    """Add a new user to the database, book a hotel, and add a city."""
    with Session() as session:
        user = User(name=name, username=username, email=email, password=password, role=role)
        session.add(user)

        # Book a hotel
        hotel = session.query(Hotel).filter_by(name=hotel_name).first()
        if hotel:
            user.reservations.append(Reservation(hotel=hotel, room=hotel.rooms[0]))
        
        # Add a city
        city = session.query(City).filter_by(name=city_name).first()
        if not city:
            city = City(name=city_name)
            session.add(city)

        session.commit()
    print("User added, hotel booked, and city added successfully!")

@cli.command()
@click.option("--name", prompt="City Name", help="City's Name")
def add_city(name):
    """Add a new city."""
    with Session() as session:
        city = City(name=name)
        session.add(city)
        session.commit()
    print("City added successfully!")

@cli.command()
def add_hotel():
    """Add a new hotel."""
    name = input("Enter the Hotel Name: ").strip()
    description = input("Enter the Hotel Description: ").strip()
    rating = float(input("Enter the Hotel Rating (0-5): ").strip())
    city_name = input("Enter the City Name: ").strip()

    with Session() as session:
        # Check if the city exists
        city = session.query(City).filter_by(name=city_name).first()
        if not city:
            city = City(name=city_name)
            session.add(city)
            session.commit()

        # Create a Hotel object
        hotel = Hotel(
            name=name,
            description=description,
            rating=rating,
            city=city  # Assign the city object to the hotel
        )

        # Add the hotel to the session and commit to the database
        session.add(hotel)
        session.commit()
    print("Hotel added successfully!")

@cli.command()
@click.option("--username", prompt="Username", help="Username")
def print_user(username):
    """Print user details."""
    with Session() as session:
        user = session.query(User).filter_by(username=username).first()
        if user:
            print(f"User ID: {user.id}")
            print(f"Name: {user.name}")
            print(f"Email: {user.email}")
            print(f"Role: {user.role}")
            print("Reservations:")
            for reservation in user.reservations:
                print(f"\tHotel: {reservation.hotel.name}")
                print(f"\tRoom: {reservation.room.name}")
                print(f"\tDate: {reservation.date}")
        else:
            print(f"User with username '{username}' not found.")

@cli.command()
@click.option("--city_name", prompt="City Name", help="City Name")
def print_city(city_name):
    """Print city hotels."""
    with Session() as session:
        city = session.query(City).filter_by(name=city_name).first()
        if city:
            print(f"City: {city.name}")
            hotels = city.hotels
            for hotel in hotels:
                print(f"Hotel: {hotel.name}")
                print(f"\tDescription: {hotel.description}")
                print(f"\tRating: {hotel.rating}")
                print(f"\tRooms:")
                for room in hotel.rooms:
                    print(f"\t\t{room.name} - {room.description} - {room.price}")
        else:
            print(f"City '{city_name}' not found.")

@cli.command()
@click.option("--hotel_name", prompt="Hotel Name", help="Hotel Name")
def print_reservations(hotel_name):
    """Print hotel reservations."""
    with Session() as session:
        hotel = session.query(Hotel).filter_by(name=hotel_name).first()
        if hotel:
            print(f"Hotel: {hotel.name}")
            reservations = hotel.reservations
            for reservation in reservations:
                print(f"User: {reservation.user.username}")
                print(f"Room: {reservation.room.name}")
                print(f"Date: {reservation.date}")
        else:
            print(f"Hotel '{hotel_name}' not found.")

def print_menu():
    print("1. Add User, Book Hotel, and Add City")
    print("2. Add City")
    print("3. Add Hotel")
    print("4. Print User Details")
    print("5. Print City Hotels")
    print("6. Print Hotel Reservations")
    print("0. Exit")

def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_user()
        elif choice == "2":
            add_city()
        elif choice == "3":
            add_hotel()
        elif choice == "4":
            username = input("Enter the username: ").strip()
            print_user(username)
        elif choice == "5":
            city_name = input("Enter the city name: ").strip()
            print_city(city_name)
        elif choice == "6":
            hotel_name = input("Enter the hotel name: ").strip()
            print_reservations(hotel_name)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please enter a number from the menu.")

if __name__ == "__main__":
    main()