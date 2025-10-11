Car Rental Management System
The Car Rental Management System is a Python-based desktop application built using PyQt6 for the graphical user interface (GUI).
It allows users to manage a list of available car models, add new cars, book cars (reducing stock), and return cars (increasing stock).
It also supports storing and updating data using a local database connection.

Features:
1. Add Car – Add a new car with name, price, stock, and optional note.
2. Book Car – Rent a car (reduces stock by 1).
3. Return Car – Return a car (increases stock by 1).
4. Delete Car – Remove a selected car from the list.
5. Refresh – Reload the table to show updated data.
6. Note Field – Add extra details like “With driver”, “For VIP”, or “Promo rate”.
7. Available Models List – Quick list of popular car models with pre-set prices.

Technologies Used:
1. Python 3	Main programming language
2. PyQt6	For building the graphical interface
3. SQLite (via get_conn)	To store and manage data
4. OOP (Classes & Objects)	To structure and organize the program
5. Dictionary (CAR_PRICES)	For storing car models and their prices

How it Works:
1. The app displays a list of available car models on the left side.
2. When a car is selected, its price is automatically filled using a dictionary (CAR_PRICES).
3. You can then set the stock and notes (like “With Driver” or “Without Driver”) and add it to the system.
4. The table on the right shows all added cars.
5. The Book Car button decreases stock by 1, while the Return Car button increases it by 1.
6. All data is managed through the ItemService and ItemRepository, which handle database operations.

Screenshots:
<img width="907" height="591" alt="image" src="https://github.com/user-attachments/assets/faf93165-6cc6-4d3f-a233-e1ee9f54919b" />
