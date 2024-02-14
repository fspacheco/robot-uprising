"""
Simple GUI for testing the Robot Uprising robot

Fernando
02-2024
"""
import tkinter as tk
import socket
import time
from threading import Thread

class RobotController:
    def __init__(self, master):
        self.master = master
        self.master.title("Micro Invaders Robot Controller")

        self.right_motor_value = tk.IntVar()
        self.left_motor_value = tk.IntVar()
        self.ip_value = tk.StringVar()
        self.ip_value.set("192.168.81.205")  # Default IP
        self.port_value = tk.StringVar()
        self.port_value.set("3000")  # Default port        

        self.create_widgets()

    def create_widgets(self):
        # IP address setup
        ip_label = tk.Label(self.master, text="IP Address:")
        ip_label.grid(row=0, column=0)
        self.ip_entry = tk.Entry(self.master, textvariable=self.ip_value)
        self.ip_entry.grid(row=0, column=1)

        # Port setup
        port_label = tk.Label(self.master, text="Port:")
        port_label.grid(row=1, column=0)
        self.port_entry = tk.Entry(self.master, textvariable=self.port_value)
        self.port_entry.grid(row=1, column=1)

        # Default values for real robot and simulation
        real_label = tk.Button(self.master, text="Real robot", command=self.set_ip_real)
        real_label.grid(row=0, column=2)
        simulator_label = tk.Button(self.master, text="Simulator", command=self.set_ip_simulator)
        simulator_label.grid(row=1, column=2)

        # Left motor slider
        left_motor_label = tk.Label(self.master, text="Left Motor")
        left_motor_label.grid(row=2, column=0)
        left_motor_slider = tk.Scale(self.master, from_=-100, to=100, orient=tk.HORIZONTAL, variable=self.left_motor_value, length=300)
        left_motor_slider.grid(row=2, column=1)

        # Right motor slider
        right_motor_label = tk.Label(self.master, text="Right Motor")
        right_motor_label.grid(row=3, column=0)
        right_motor_slider = tk.Scale(self.master, from_=-100, to=100, orient=tk.HORIZONTAL, variable=self.right_motor_value, length=300)
        right_motor_slider.grid(row=3, column=1)
        
        # Send button
        send_button = tk.Button(self.master, text="SEND", command=self.send_command)
        send_button.grid(row=4, column=0, columnspan=2)

        # Stop button
        stop_button = tk.Button(self.master, text="STOP", command=self.stop_robot)
        stop_button.grid(row=5, column=0, columnspan=2)

        # Square movement button
        square_button = tk.Button(self.master, text="Move Square", command=self.move_square_thread)
        square_button.grid(row=6, column=0, columnspan=2)

        # Circle movement button
        circle_button = tk.Button(self.master, text="Move Circle", command=self.move_circle_thread)
        circle_button.grid(row=7, column=0, columnspan=2)        

        # Forward button
        forward_button = tk.Button(self.master, text="Forward", command=self.move_forward)
        forward_button.grid(row=8, column=1)

        # Backward button
        backward_button = tk.Button(self.master, text="Backward", command=self.move_backward)
        backward_button.grid(row=10, column=1)

        # Left button
        left_button = tk.Button(self.master, text="Left", command=self.move_left)
        left_button.grid(row=9, column=0)

        # Right button
        right_button = tk.Button(self.master, text="Right", command=self.move_right)
        right_button.grid(row=9, column=2)

    def set_ip_real(self):
        self.ip_value.set("192.168.81.205")
        self.port_value.set("3000")

    def set_ip_simulator(self):
        self.ip_value.set("127.0.0.1")
        self.port_value.set("3001")

    def move_forward(self):
        self.right_motor_value.set(100)
        self.left_motor_value.set(100)
        self.send_command()

    def move_backward(self):
        self.right_motor_value.set(-100)
        self.left_motor_value.set(-100)
        self.send_command()

    def move_left(self):
        self.left_motor_value.set(-25)
        self.right_motor_value.set(+50)
        self.send_command()

    def move_right(self):
        self.left_motor_value.set(+50)
        self.right_motor_value.set(-25)
        self.send_command()

    def send_command(self):
        left_motor = self.left_motor_value.get()
        right_motor = self.right_motor_value.get()
        command = f"{left_motor};{right_motor}"
        self.send_udp_packet(command)

    def stop_robot(self):
        command = "0;0"
        self.send_udp_packet(command)

    def send_udp_packet(self, command):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.sendto(command.encode(), (self.ip_value.get(), int(self.port_value.get())))
        udp_socket.close()

    def move_square_thread(self):
        # Create a new thread to move the robot in a square pattern
        Thread(target=self.move_square).start()

    def move_square(self):
        # Function to move the robot in a square pattern
        step_time = 1.5

        for i in range(4): # 4 sides
            self.move_forward()
            time.sleep(step_time)
            self.move_right()
            time.sleep(0.3*step_time)
        self.stop_robot()

    def move_circle_thread(self):
        # Create a new thread to move the robot in a circle pattern
        Thread(target=self.move_circle).start()

    def move_circle(self):
        # Function to move the robot in a circle pattern
        speed = 100  # Speed of the motors
        self.send_udp_packet(f"{int(speed)};{int(0.5*speed)}")        

def main():
    root = tk.Tk()
    app = RobotController(root)
    root.mainloop()

if __name__ == "__main__":
    main()
