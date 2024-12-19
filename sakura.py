import streamlit as st
import datetime
import random
from PIL import Image
import pandas as pd

# Initialize session state variables if they don't exist
if 'airline_system' not in st.session_state:
    st.session_state.airline_system = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

class Seat:
    def __init__(self, seat_number):
        self.seat_number = seat_number
        self.is_occupied = False
        self.seat_class = self.get_seat_class()

    def get_seat_class(self):
        row = int(self.seat_number[:-1])
        if row <= 2:
            return 'First'
        elif row <= 7:
            return 'Business'
        else:
            return 'Economy'

    def occupy(self):
        self.is_occupied = True
        
    def empty(self):
        self.is_occupied = False

class FirstClass(Seat):
    def __init__(self, seat_number):
        super().__init__(seat_number)
        self._price = 10000000.0
        self._amenities = ["15kg Luggage", "Premium Meals", "Private Line", "Private Restroom"]
    
    def get_price(self):
        return self._price
    
    def get_amenities(self):
        return self._amenities

class BusinessClassSeat(Seat):
    def __init__(self, seat_number):
        super().__init__(seat_number)
        self._price = 5000000.0
        self._amenities = ["10kg Luggage", "Business Meals", "Priority Boarding"]
    
    def get_price(self):
        return self._price
    
    def get_amenities(self):
        return self._amenities

class EconomyClassSeat(Seat):
    def __init__(self, seat_number):
        super().__init__(seat_number)
        self._price = 1000000.0
        self._amenities = ["2kg Luggage", "Standard Seat", "Basic Meal"]
    
    def get_price(self):
        return self._price
    
    def get_amenities(self):
        return self._amenities

class Payment:
    def __init__(self, amount, payment_method):
        self._payment_id = str(random.randint(10000000, 99999999))
        self._amount = amount
        self._payment_method = payment_method
        self._status = "Pending"  
        self._timestamp = datetime.datetime.now()

    def get_amount(self):
        return self._amount
    
    def get_payment(self):
        return self._payment_method
    
    def get_status(self):
        return self._status
    
    def process_payment(self):
        self._status = "Completed"
        return True
    
    def refund_payment(self):
        if self.get_status() == "Completed":
            self._status = "Refunded"
            return True
        return False

class Flight:
    def __init__(self, flight_number, flight_date, destination, 
                 departure_time, arrival_time, gate_number):
        self._flight_number = flight_number
        self._flight_date = flight_date
        self._destination = destination
        self._departure_time = departure_time
        self._arrival_time = arrival_time
        self._gate_number = gate_number
        self._seats = {}
        self._passengers = []
        self._initialize_seats()

    def get_flight_number(self):
        return self._flight_number
    
    def get_flight_date(self):
        return self._flight_date
    
    def get_destination(self):
        return self._destination
    
    def get_departure_time(self):
        return self._departure_time
    
    def get_arrival_time(self):
        return self._arrival_time
    
    def get_gate_number(self):
        return self._gate_number
    
    def get_seats(self):
        return self._seats

    def _initialize_seats(self):
        # First Class (Rows 1-2)
        for row in range(1, 3):
            for col in ['A', 'B', 'E', 'F']:
                seat_number = f"{row}{col}"
                self._seats[seat_number] = FirstClass(seat_number)
            
        # Business Class (Rows 3-7)
        for row in range(3, 8):
            for col in ['A', 'B', 'E', 'F']:
                seat_number = f"{row}{col}"
                self._seats[seat_number] = BusinessClassSeat(seat_number)
        
        # Economy Class (Rows 8-30)
        for row in range(8, 31):
            for col in ['A', 'B', 'C', 'D', 'E', 'F']:
                seat_number = f"{row}{col}"
                self._seats[seat_number] = EconomyClassSeat(seat_number)

    def get_available_seats(self):
        return [seat for seat in self._seats.values() if not seat.is_occupied]

    def assign_seat(self, seat_number, passenger):
        if seat_number in self._seats and not self._seats[seat_number].is_occupied:
            self._seats[seat_number].occupy()
            self._passengers.append(passenger)
            return True
        return False

class Passenger:
    def __init__(self, passport_number, first_name, last_name, age, email=None, phone=None):
        self._passenger_id = str(random.randint(10000, 99999))
        self._passport_number = passport_number
        self._first_name = first_name
        self._last_name = last_name
        self._age = age
        self._email = email
        self._phone = phone

    def get_full_name(self):
        return f"{self._first_name} {self._last_name}"

class Reservation:
    def __init__(self, passenger, flight, seat_number):
        self._reservation_id = str(random.randint(10000000, 99999999))
        self._passenger = passenger
        self._flight = flight
        self._seat_number = seat_number
        self._reservation_date = datetime.datetime.now()
        self.status = "Pending"
        self._payment = None
    
    def confirm_reservation(self, payment_method):
        seat = self._flight._seats[self._seat_number]
        payment = Payment(seat.get_price(), payment_method)
        
        if payment.process_payment():
            self._payment = payment
            self.status = "Confirmed"
            self._flight.assign_seat(self._seat_number, self._passenger)
            return True
        return False
    
    def cancel_reservation(self):
        if self.status == "Confirmed":
            self.status = "Cancelled"
            self._flight._seats[self._seat_number].empty()
            if self._payment:
                self._payment.refund_payment()
            return True
        return False

class AirlineSystem:
    def __init__(self):
        self.flights = []
        self.reservations = []
    
    def add_flight(self, flight):
        # Check if flight number already exists
        if any(f.get_flight_number() == flight.get_flight_number() for f in self.flights):
            return False
        self.flights.append(flight)
        return True
    
    def find_flights(self, destination=None, date=None):
        filtered_flights = []
        for flight in self.flights:
            if destination and date:
                if flight.get_destination().lower() == destination.lower() and flight.get_flight_date() == date:
                    filtered_flights.append(flight)
            elif destination:
                if flight.get_destination().lower() == destination.lower():
                    filtered_flights.append(flight)
            elif date:
                if flight.get_flight_date() == date:
                    filtered_flights.append(flight)
            else:
                filtered_flights.append(flight)
        return filtered_flights
    
    def create_reservation(self, passenger, flight, seat_number, payment_method):
        reservation = Reservation(passenger, flight, seat_number)
        if reservation.confirm_reservation(payment_method):
            self.reservations.append(reservation)
            return reservation
        return None

def create_seat_map(flight):
    st.markdown("### Seat Map")
    st.markdown("#### Legend:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🟦 Available")
    with col2:
        st.markdown("🟥 Occupied")
    with col3:
        st.markdown("⬛ Not Available")

    st.markdown("#### Seat Classes:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("F - First Class (Rows 1-2)")
    with col2:
        st.markdown("B - Business Class (Rows 3-7)")
    with col3:
        st.markdown("E - Economy Class (Rows 8-30)")

    # Header row with column letters
    cols = st.columns(7)
    cols[0].markdown("Row")
    for i, col in enumerate(['A', 'B', 'C', 'D', 'E', 'F']):
        cols[i+1].markdown(col)

    # Create seat map
    for row in range(1, 31):
        cols = st.columns(7)
        cols[0].markdown(f"{row}")
        
        for i, col in enumerate(['A', 'B', 'C', 'D', 'E', 'F']):
            seat_num = f"{row}{col}"
            
            # Check if seat exists and get its status
            if seat_num in flight._seats:
                seat = flight._seats[seat_num]
                if seat.is_occupied:
                    cols[i+1].markdown("🟥")
                else:
                    cols[i+1].markdown("🟦")
            else:
                cols[i+1].markdown("⬛")

def show_home_page():
    st.markdown("### 🌸 Welcome to Sakura Airlines!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Our Services
        - ✨ First Class Luxury Experience
        - 💼 Business Class Comfort
        - 🌟 Economy Class Value
        """)
        
    with col2:
        st.markdown("""
        #### Why Choose Sakura Airlines?
        - 🌸 Japanese Hospitality
        - 🛫 Modern Fleet
        - 🎯 On-time Performance
        """)

    # Display current flights overview
    if st.session_state.airline_system.flights:
        st.markdown("### Today's Flights")
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        today_flights = st.session_state.airline_system.find_flights(date=today)
        
        if today_flights:
            for flight in today_flights:
                with st.expander(f"Flight {flight.get_flight_number()} to {flight.get_destination()}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"Departure: {flight.get_departure_time()}")
                        st.write(f"Gate: {flight.get_gate_number()}")
                    with col2:
                        available_seats = flight.get_available_seats()
                        st.write(f"Available Seats: {len(available_seats)}")

def show_add_flight_page():
    st.markdown("### ✈️ Add New Flight")
    
    with st.form("add_flight_form"):
        flight_number = st.text_input("Flight Number")
        flight_date = st.date_input("Flight Date")
        destination = st.text_input("Destination")
        departure_time = st.time_input("Departure Time")
        arrival_time = st.time_input("Arrival Time")
        gate_number = st.text_input("Gate Number")
        
        submit = st.form_submit_button("Add Flight")
        
        if submit:
            if not flight_number or not destination or not gate_number:
                st.error("Please fill in all required fields")
                return
                
            try:
                # Validate times
                if arrival_time <= departure_time:
                    st.error("Arrival time must be after departure time")
                    return
                
                flight = Flight(
                    flight_number,
                    flight_date.strftime("%Y-%m-%d"),
                    destination.capitalize(),
                    departure_time.strftime("%H:%M"),
                    arrival_time.strftime("%H:%M"),
                    gate_number
                )
                
                if st.session_state.airline_system.add_flight(flight):
                    st.success("Flight added successfully!")
                else:
                    st.error("Flight number already exists")
            except Exception as e:
                st.error(f"Error adding flight: {str(e)}")

def show_search_flights_page():
    st.markdown("### 🔍 Search Flights")
    
    destination = st.text_input("Destination (optional)")
    date = st.date_input("Date (optional)", None)
    
    if st.button("Search"):
        date_str = date.strftime("%Y-%m-%d") if date else None
        flights = st.session_state.airline_system.find_flights(
            destination if destination else None,
            date_str
        )
        
        if flights:
            st.success(f"Found {len(flights)} flights matching your criteria")
            
            for flight in flights:
                with st.expander(f"Flight {flight.get_flight_number()} to {flight.get_destination()}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"Date: {flight.get_flight_date()}")
                        st.write(f"Time: {flight.get_departure_time()} - {flight.get_arrival_time()}")
                        st.write(f"Gate: {flight.get_gate_number()}")
                    with col2:
                        available_seats = flight.get_available_seats()
                        st.write(f"Available Seats: {len(available_seats)}")
                        if len(available_seats) == 0:
                            st.warning("FULLY BOOKED")
        else:
            st.warning("No flights found matching your criteria.")

def show_flight_details_page():
    st.markdown("### 📋 View Flight Details")
    
    flight_number = st.text_input("Enter Flight Number")
    
    if flight_number:
        flight = None
        for f in st.session_state.airline_system.flights:
            if f.get_flight_number() == flight_number:
                flight = f
                break
        
        if flight:
            st.success(f"Flight {flight_number} Details")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"Destination: {flight.get_destination()}")
                st.write(f"Date: {flight.get_flight_date()}")
                st.write(f"Departure Time: {flight.get_departure_time()}")
                st.write(f"Arrival Time: {flight.get_arrival_time()}")
            with col2:
                st.write(f"Gate: {flight.get_gate_number()}")
                available_seats = flight.get_available_seats()
                st.write(f"Available Seats: {len(available_seats)}")
            
            # Display seat class information
            st.markdown("### Seat Class Information")
            class_cols = st.columns(3)
            
            # First Class
            with class_cols[0]:
                st.markdown("#### First Class")
                first_class_seat = next((seat for seat in flight.get_seats().values() 
                                      if isinstance(seat, FirstClass)), None)
                if first_class_seat:
                    st.write(f"Price: VND {first_class_seat.get_price():,.0f}")
                    st.write("Amenities:")
                    for amenity in first_class_seat.get_amenities():
                        st.write(f"- {amenity}")
            
            # Business Class
            with class_cols[1]:
                st.markdown("#### Business Class")
                business_class_seat = next((seat for seat in flight.get_seats().values() 
                                         if isinstance(seat, BusinessClassSeat)), None)
                if business_class_seat:
                    st.write(f"Price: VND {business_class_seat.get_price():,.0f}")
                    st.write("Amenities:")
                    for amenity in business_class_seat.get_amenities():
                        st.write(f"- {amenity}")
            
            # Economy Class
            with class_cols[2]:
                st.markdown("#### Economy Class")
                economy_class_seat = next((seat for seat in flight.get_seats().values() 
                                        if isinstance(seat, EconomyClassSeat)), None)
                if economy_class_seat:
                    st.write(f"Price: VND {economy_class_seat.get_price():,.0f}")
                    st.write("Amenities:")
                    for amenity in economy_class_seat.get_amenities():
                        st.write(f"- {amenity}")
            
            # Display seat map
            create_seat_map(flight)
        else:
            st.error("Flight not found. Please check the flight number.")

def show_booking_page():
    st.markdown("### 🎫 Book a Flight")
    
    flight_number = st.text_input("Enter Flight Number")
    
    if flight_number:
        flight = None
        for f in st.session_state.airline_system.flights:
            if f.get_flight_number() == flight_number:
                flight = f
                break
        
        if flight:
            st.success(f"Booking for Flight {flight_number}")
            
            # Display flight information
            st.markdown("#### Flight Details")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"Destination: {flight.get_destination()}")
                st.write(f"Date: {flight.get_flight_date()}")
                st.write(f"Time: {flight.get_departure_time()} - {flight.get_arrival_time()}")
            with col2:
                st.write(f"Gate: {flight.get_gate_number()}")
                available_seats = flight.get_available_seats()
                st.write(f"Available Seats: {len(available_seats)}")
            
            # Display seat map
            create_seat_map(flight)
            
            # Booking form
            with st.form("booking_form"):
                st.markdown("#### Passenger Information")
                
                col1, col2 = st.columns(2)
                with col1:
                    first_name = st.text_input("First Name")
                    last_name = st.text_input("Last Name")
                    passport_number = st.text_input("Passport Number")
                with col2:
                    age = st.number_input("Age", min_value=0, max_value=150)
                    email = st.text_input("Email (optional)")
                    phone = st.text_input("Phone (optional)")
                
                st.markdown("#### Seat Selection")
                available_seat_numbers = [seat.seat_number for seat in available_seats]
                if available_seat_numbers:
                    seat_number = st.selectbox("Choose a seat", available_seat_numbers)
                else:
                    st.error("No seats available on this flight")
                    return
                
                st.markdown("#### Payment")
                payment_methods = ["Credit Card", "Momo", "VNPay", "ZaloPay", "Banking Transfer"]
                payment_method = st.selectbox("Payment Method", payment_methods)
                
                submit = st.form_submit_button("Book Flight")
                
                if submit:
                    if not all([first_name, last_name, passport_number]):
                        st.error("Please fill in all required fields")
                        return
                    
                    try:
                        passenger = Passenger(
                            passport_number, first_name, last_name, 
                            age, email, phone
                        )
                        
                        reservation = st.session_state.airline_system.create_reservation(
                            passenger, flight, seat_number, payment_method.lower()
                        )
                        
                        if reservation:
                            st.success(f"""
                                Reservation confirmed!
                                Reservation ID: {reservation._reservation_id}
                                Please save this ID for future reference.
                            """)
                        else:
                            st.error("Failed to create reservation")
                    except Exception as e:
                        st.error(f"Error creating reservation: {str(e)}")
        else:
            st.error("Flight not found. Please check the flight number.")

def show_cancel_page():
    st.markdown("### ❌ Cancel Reservation")
    
    reservation_id = st.text_input("Enter Reservation ID")
    
    if reservation_id:
        found = False
        for reservation in st.session_state.airline_system.reservations:
            if reservation._reservation_id == reservation_id:
                found = True
                
                if reservation.status == "Confirmed":
                    st.write("#### Reservation Details")
                    st.write(f"Passenger: {reservation._passenger.get_full_name()}")
                    st.write(f"Flight: {reservation._flight.get_flight_number()}")
                    st.write(f"Seat: {reservation._seat_number}")
                    
                    if st.button("Cancel Reservation"):
                        if reservation.cancel_reservation():
                            refund_amount = reservation._payment.get_amount()
                            refund_method = reservation._payment.get_payment()
                            
                            st.success("Reservation cancelled successfully")
                            st.write(f"Refund Amount: VND {refund_amount:,.0f}")
                            st.write(f"Refund Method: {refund_method.capitalize()}")
                        else:
                            st.error("Failed to cancel reservation")
                else:
                    st.warning("This reservation is already cancelled or pending")
                break
        
        if not found:
            st.error("Reservation not found. Please check the reservation ID.")

def main():
    st.set_page_config(page_title="Sakura Airlines", layout="wide")
    
    # Custom CSS
    st.markdown("""
        <style>
        .big-font {
            font-size:30px !important;
            font-weight: bold;
            color: #FF69B4;
        }
        .stButton>button {
            background-color: #FF69B4;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown('<p class="big-font">🌸 Sakura Airlines Reservation System</p>', unsafe_allow_html=True)

    # Initialize AirlineSystem if not already initialized
    if st.session_state.airline_system is None:
        st.session_state.airline_system = AirlineSystem()

    # Sidebar navigation
    with st.sidebar:
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSK-8U0esvPeyL2kA8YFdAKy3gHnjBV5WJShQ&s", use_container_width=True)
        st.markdown("### Navigation")
        if st.button("🏠 Home"):
            st.session_state.current_page = 'home'
        if st.button("✈️ Add Flight"):
            st.session_state.current_page = 'add_flight'
        if st.button("🔍 Search Flights"):
            st.session_state.current_page = 'search_flights'
        if st.button("📋 View Flight Details"):
            st.session_state.current_page = 'view_details'
        if st.button("🎫 Book a Flight"):
            st.session_state.current_page = 'book_flight'
        if st.button("❌ Cancel Reservation"):
            st.session_state.current_page = 'cancel'

    # Page content
    if st.session_state.current_page == 'home':
        show_home_page()
    elif st.session_state.current_page == 'add_flight':
        show_add_flight_page()
    elif st.session_state.current_page == 'search_flights':
        show_search_flights_page()
    elif st.session_state.current_page == 'view_details':
        show_flight_details_page()
    elif st.session_state.current_page == 'book_flight':
        show_booking_page()
    elif st.session_state.current_page == 'cancel':
        show_cancel_page()

if __name__ == "__main__":
    main()