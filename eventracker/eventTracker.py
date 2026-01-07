Events = []

def add_event(name, date, time):
    event = {
        'name':name,
        'date':date,
        'time':time
    }
    
    Events.append(event)

def add_new_event():
    name = input("Event Name : ")
    date = input("Date (dd/mm/yyyy) : ")
    time = input("Time (hh/mm): ")
    
    add_event(name,date,time)

def show_events():
    for event in Events:
        print(f"{event['name']:20} {event['date']:20} {event['time']}")    


def main():
    while True:
        print("\n==============Welcome, To Event Tracker==============")   
        
        print("1. Add Event")
        print("2. Show Events")
        print("3. Quit")
        
        choice = int(input("choice : "))
    
    
        if choice == 1:
            add_new_event()
        elif choice == 2:
            show_events()
        elif choice == 3:
            print("Thank you for using Event Tracker You you next time time")
            break
        else:
            print("Invalid choice")
            
main()
