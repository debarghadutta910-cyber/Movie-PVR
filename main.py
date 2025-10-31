# Movie Ticket Management System (CBSE Class 12 compatible version)
# Uses only functions, files, lists, strings, and basic Python features

# ----------------------- GLOBAL FILE NAMES -----------------------
USERS_FILE = "users.txt"
MOVIES_FILE = "movies.txt"
BOOKINGS_FILE = "bookings.txt"

# ----------------------- INITIAL SETUP ----------------------------
def setup_files():
    """Create initial files if not present"""
    with open(USERS_FILE, "w") as f:
        f.write("admin,admin123\n")   # default login
    
    with open(MOVIES_FILE, "w") as f:
        f.write("1,The Time Traveler,10:00 AM,1111111111111111111111111\n")
        f.write("2,Comedy Nights,03:00 PM,1111111111111111111111111\n")
        f.write("3,Sci-Fi Odyssey,07:00 PM,1111111111111111111111111\n")
    
    with open(BOOKINGS_FILE, "w") as f:
        f.write("BookingID,Name,Phone,Movie,Showtime,Seats,Food,Total\n")

# ----------------------- AUTHENTICATION ----------------------------
def login():
    print("===== MOVIE TICKET MANAGEMENT SYSTEM =====")
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    with open(USERS_FILE, "r") as f:
        for line in f:
            u, p = line.strip().split(",")
            if u == username and p == password:
                print("Login Successful!\n")
                return True
    print("Invalid Username or Password.\n")
    return False

# ----------------------- MOVIE MANAGEMENT ----------------------------
def load_movies():
    movies = []
    with open(MOVIES_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 4:
                movies.append({
                    "id": parts[0],
                    "title": parts[1],
                    "show": parts[2],
                    "seats": parts[3]
                })
    return movies

def save_movies(movies):
    with open(MOVIES_FILE, "w") as f:
        for m in movies:
            f.write(m["id"] + "," + m["title"] + "," + m["show"] + "," + m["seats"] + "\n")

def show_movies(movies):
    print("\nAvailable Movies and Showtimes:")
    for m in movies:
        available = m["seats"].count("1")
        status = "SOLD OUT" if available == 0 else str(available) + " seats"
        print(m["id"] + ". " + m["title"] + " — " + m["show"] + " — " + status)
    print()

# ----------------------- SEAT DISPLAY ----------------------------
def display_seats(seats):
    print("\nSeat Layout (5 x 5):")
    for i in range(5):
        for j in range(5):
            idx = i * 5 + j
            if seats[idx] == "1":
                print(f"{idx+1:02d}", end=" ")
            else:
                print(" X ", end=" ")
        print()
    print()

# ----------------------- BOOKING ----------------------------
def book_tickets(movies):
    show_movies(movies)
    movie_id = input("Enter Movie ID to book: ")
    selected = None
    for m in movies:
        if m["id"] == movie_id:
            selected = m
            break
    
    if not selected:
        print("Invalid Movie ID.\n")
        return
    
    if selected["seats"].count("1") == 0:
        print("All seats are booked. SOLD OUT!\n")
        return
    
    display_seats(selected["seats"])
    name = input("Customer Name: ")
    phone = input("Phone Number: ")
    seats_needed = int(input("Number of Seats: "))
    
    available = selected["seats"].count("1")
    if seats_needed > available:
        print("Not enough seats available.\n")
        return
    
    print("Enter seat numbers separated by commas (e.g. 3,7,10)")
    seat_input = input("Seats: ")
    chosen = [int(x) for x in seat_input.split(",")]
    
    s_list = list(selected["seats"])
    for seat in chosen:
        if seat < 1 or seat > 25 or s_list[seat-1] == "0":
            print("Invalid or already booked seat number.")
            return
        s_list[seat-1] = "0"
    selected["seats"] = "".join(s_list)
    
    # Food Menu
    print("\nFood Menu:")
    print("1. Burger - Rs 200")
    print("2. Fries - Rs 100")
    print("3. Popcorn - Rs 600")
    print("Press Enter if no food needed.")
    
    food_choice = input("Enter food numbers separated by commas: ")
    total_food_cost = 0
    food_items = []
    
    if food_choice.strip() != "":
        for ch in food_choice.split(","):
            ch = ch.strip()
            if ch == "1":
                total_food_cost += 200
                food_items.append("Burger")
            elif ch == "2":
                total_food_cost += 100
                food_items.append("Fries")
            elif ch == "3":
                total_food_cost += 600
                food_items.append("Popcorn")
    
    # Ticket Price
    TICKET_PRICE = 250
    total = TICKET_PRICE * seats_needed + total_food_cost
    
    # Save Booking
    import time
    booking_id = str(int(time.time()))
    with open(BOOKINGS_FILE, "a") as f:
        f.write(booking_id + "," + name + "," + phone + "," + selected["title"] + "," + selected["show"] + "," + str(chosen) + "," + ";".join(food_items) + "," + str(total) + "\n")
    
    # Update Movies
    save_movies(movies)
    
    print("\nBooking Successful!")
    print("Booking ID:", booking_id)
    print("Total Amount: Rs", total)
    print("Enjoy your movie!\n")
    
    # Generate a text-based receipt
    generate_text_receipt(booking_id, name, phone, selected, chosen, food_items, total)

# ----------------------- TEXT RECEIPT ----------------------------
def generate_text_receipt(bid, name, phone, movie, seats, food, total):
    with open("receipt_" + bid + ".txt", "w") as f:
        f.write("========== MOVIE TICKET RECEIPT ==========\n")
        f.write("Booking ID: " + bid + "\n")
        f.write("Name: " + name + "\n")
        f.write("Phone: " + phone + "\n")
        f.write("Movie: " + movie["title"] + "\n")
        f.write("Showtime: " + movie["show"] + "\n")
        f.write("Seats: " + str(seats) + "\n")
        f.write("Food Items: " + ", ".join(food) + "\n")
        f.write("Total Amount: Rs " + str(total) + "\n")
        f.write("==========================================\n")
    print("Receipt generated: receipt_" + bid + ".txt\n")

# ----------------------- MAIN MENU ----------------------------
def main():
    setup_files()
    if not login():
        return
    
    while True:
        print("1. Show Movies")
        print("2. Book Tickets")
        print("3. Exit")
        ch = input("Enter choice: ")
        movies = load_movies()
        if ch == "1":
            show_movies(movies)
        elif ch == "2":
            book_tickets(movies)
        elif ch == "3":
            print("Thank you for using the system!")
            break
        else:
            print("Invalid choice!\n")

# ----------------------- DRIVER CODE ----------------------------
main()
