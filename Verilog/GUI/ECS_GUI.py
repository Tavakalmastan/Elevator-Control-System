import tkinter as tk 
import os 
 
# --- File names for communication --- 
REQUEST_FILE = "requests.txt" 
STATUS_FILE = "status.txt" 
 
class ElevatorGUI: 
    def __init__(self, root): 
        self.root = root 
        root.title("Elevator Control") 
        root.geometry("300x450") 
 
        self.floor_buttons = [] 
        self.floor_colors = ["#FFDDC1", "#C1FFD7", "#C1D4FF", "#FBC1FF"] 
 
        # --- Create Floor Buttons (Inside the elevator) --- 
        button_frame = tk.Frame(root, pady=10) 
        button_frame.pack() 
         
        tk.Label(button_frame, text="Request Floor:", font=("Arial", 14)).pack() 
 
        for i in range(3, -1, -1):  # Create buttons from 3 down to 0 
            btn = tk.Button( 
                button_frame, 
                text=f"Floor {i}", 
                font=("Arial", 12), 
                width=15, 
                height=2, 
 
 
                bg=self.floor_colors[i], 
                command=lambda f=i: self.request_floor(f) 
            ) 
            btn.pack(pady=5) 
            self.floor_buttons.append(btn) 
 
        # --- Create Status Display --- 
        status_frame = tk.Frame(root, pady=10) 
        status_frame.pack() 
 
        tk.Label(status_frame, text="Elevator Status", font=("Arial", 14)).pack() 
         
        self.status_label = tk.Label( 
            status_frame, 
            text="Initializing...", 
            font=("Arial", 12, "bold"), 
            bg="#EEEEEE", 
            width=20, 
            height=3, 
            relief="sunken" 
        ) 
        self.status_label.pack(pady=10) 
 
        # --- Start the update loop --- 
        self.update_status() 
 
    def request_floor(self, floor_num): 
        """Writes a request to the requests.txt file.""" 
        print(f"Requesting floor {floor_num}") 
         
        # Create a 4-bit request string, e.g., floor 1 = "0010" 
        request_str = "0000" 
        if floor_num == 0: 
            request_str = "0001" 
 
 
        elif floor_num == 1: 
            request_str = "0010" 
        elif floor_num == 2: 
            request_str = "0100" 
        elif floor_num == 3: 
            request_str = "1000" 
             
        try: 
            with open(REQUEST_FILE, "w") as f: 
                f.write(request_str) 
        except Exception as e: 
            print(f"Error writing to request file: {e}") 
 
    def update_status(self): 
        """Reads status.txt and updates the GUI.""" 
        try: 
            if os.path.exists(STATUS_FILE): 
                with open(STATUS_FILE, "r") as f: 
                    data = f.read().strip() 
                 
                if data: 
                    parts = data.split() 
                    if len(parts) == 3: 
                        floor = int(parts[0]) 
                        direction = int(parts[1]) # 0=IDLE, 1=UP, 2=DOWN 
                        door = int(parts[2])     # 0=CLOSED, 1=OPEN 
 
                        # --- Build the status string --- 
                        status_text = f"Current Floor: {floor}\n" 
                         
                        if door == 1: 
                            status_text += "Door: OPEN" 
                            self.status_label.config(bg="#D4EDDA") # Green 
                        elif direction == 1: 
 
 
                            status_text += "Direction: UP ↑" 
                            self.status_label.config(bg="#FFF3CD") # Yellow 
                        elif direction == 2: 
                            status_text += "Direction: DOWN ↓" 
                            self.status_label.config(bg="#F8D7DA") # Red 
                        else: 
                            status_text += "Status: IDLE" 
                            self.status_label.config(bg="#E2E3E5") # Gray 
 
                        self.status_label.config(text=status_text) 
                     
        except Exception as e: 
            self.status_label.config(text=f"Error reading status:\n{e}") 
 
        # Schedule this function to run again after 500ms 
        self.root.after(500, self.update_status) 
 
 
if __name__ == "__main__": 
    # Ensure the request file exists on startup 
    if not os.path.exists(REQUEST_FILE): 
        with open(REQUEST_FILE, "w") as f: 
            f.write("0000") 
 
    root = tk.Tk() 
    app = ElevatorGUI(root) 
    root.mainloop() 
