from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create an SQLAlchemy session
DATABASE_URL = "sqlite:///hotel_booking.db"  # Replace with your actual database URL
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def find_most_visited_hotel():
    # Query the database to find the most visited hotel
    hotels = session.query(hotels).all()
    most_visited_hotel = None
    max_reservation_count = 0

    for hotel in hotels:
        # Count the number of reservations for each hotel
        reservation_count = session.query(Reservation).filter_by(hotel_id=hotel.id).count()

        # Check if this hotel has more reservations than the current most visited hotel
        if reservation_count > max_reservation_count:
            max_reservation_count = reservation_count
            most_visited_hotel = hotel

    if most_visited_hotel:
        print(f"The most visited hotel is {most_visited_hotel.name} with {max_reservation_count} reservations.")
    else:
        print("No reservations found in the database.")

    # Close the session
    session.close()

if __name__ == "__main__":
    find_most_visited_hotel()