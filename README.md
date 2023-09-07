# -pHASE3-PROJECT-HOTEL-with-CLI-
Readme for SQLAlchemy Hotel Booking System
This is a Python application that uses SQLAlchemy to manage a hotel booking system. The application allows users to add new users, book hotels, add cities, and print user details, city reservations, and hotel reservations.

Requirements

Python 3.x
SQLAlchemy
Click

Installation

Clone the repository: git clone https://github.com/username/hotel-booking.git
Install the dependencies: pip install -r requirements.txt
Create the database: python create_db.py

Usage

To use the application, run python main.py and follow the prompts.
The following commands are available:
add_user: Add a new user, book a hotel, and add a city.
add_city: Add a new city.
print_user: Print user details.
print_city: Print city reservations.
add_hotel: Add a new hotel.

Models

The application uses four models: User, Hotel, City, and Reservation.
User

The User model represents a user of the hotel booking system. It has the following attributes:
id: Integer, primary key, autoincrement.
name: String, required.
username: String, unique, required.
email: String, unique, required.
password: String, required.
role: String, required.
reservations: Relationship with Reservation model.

Hotel

The Hotel model represents a hotel in the booking system. It has the following attributes:
id: Integer, primary key, autoincrement.
name: String, required.
description: String.
rating: Float.
city_id: Integer, foreign key to City model.
city: Relationship with City model.
users: Relationship with User model through Reservation model.

City

The City model represents a city in the booking system. It has the following attributes:
id: Integer, primary key, autoincrement.
name: String, required.
hotels: Relationship with Hotel model.
Reservation
The Reservation model represents a reservation in the booking system. It has the following attributes:
id: Integer, primary key, autoincrement.
date: DateTime, default is the current date and time.
user_id: Integer, foreign key to User model.
hotel_id: Integer, foreign key to Hotel model.

Functions

The application has the following functions:
add_user_with_hotel_and_city
This function adds a new user to the database, books a hotel, and adds a city. It takes the following parameters:
name: String, required.
username: String, required.
email: String, required.
password: String, required.
role: String, required.
hotel_name: String, required.
city_name: String, required.
add_city
This function adds a new city to the database. It takes the following parameter:
name: String, required.
print_user_details
This function prints the details of a user. It takes the following parameter:
username: String, required.
print_city_reservations
This function prints the reservations for a city. It takes the following parameter:
city_name: String, required.
add_hotel
This function adds a new hotel to the database. It prompts the user for the hotel details.

Conclusion
This is a simple hotel booking system that demonstrates the use of SQLAlchemy in a Python application. It can be extended to include more features and functionality.