import argparse
import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from user import User  # Import the User model (update the import path as needed)
from city import City  # Import the City model
from Hotel import Hotel  # Import the Hotel model

# Database Configuration
DATABASE_URL = "sqlite:///hotel_booking.db"  # SQLite database (update as needed)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@click.group()
def cli():
    """Hotel Booking CLI Application"""
    pass

# @cli.command()
# @click.option("--name", prompt="User's Full Name", help="User's Full Name")
# @click.option("--username", prompt="Username", help="Username")
# @click.option("--email", prompt="Email", help="Email")
# @click.option("--password", prompt="Password", hide_input=True, help="Password")
# @click.option("--role", type=click.Choice(["user", "admin"]), help="User Role (user/admin)")
# def add_user(name, username, email, password, role):
#     """Add a new user to the database."""
#     session = Session()
#     user = User(name=name, username=username, email=email, password=password, role=role)
#     session.add(user)
#     session.commit()
#     session.close()
#     print("User added successfully!")

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

def parse_args():
    parse = argparse .ArgumentParser()
    