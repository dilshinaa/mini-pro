import random 
import threading 
import time 

TOTAL_SEATS = 40 

# Store passenger count per bus 
bus_data = { 
    1: {"passengers": 20}, 
    2: {"passengers": 15}, 
    3: {"passengers": 30} 
} 

def simulate_changes(): 
    while True: 
        for bus_id in bus_data: 
            change = random.randint(-3, 3) 
            new_value = bus_data[bus_id]["passengers"] + change 
            
            # Keep within limits 
            if new_value < 0: 
                new_value = 0 
            if new_value > TOTAL_SEATS: 
                new_value = TOTAL_SEATS 
                
            bus_data[bus_id]["passengers"] = new_value 
            
        time.sleep(5) # update every 5 seconds 
        
def start_simulation(): 
    thread = threading.Thread(target=simulate_changes) 
    thread.daemon = True 
    thread.start() 
    
def get_bus_data(bus_id): 
    passengers = bus_data[bus_id]["passengers"] 
    available = TOTAL_SEATS - passengers 
    
    if passengers < 15: 
        crowd = "Low" 
    elif passengers < 30: 
        crowd = "Medium" 
    else: crowd = "High" 
    
    return { 
        "passengers": passengers, 
        "available": available, 
        "crowd": crowd 
    }