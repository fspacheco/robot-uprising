"""
Simple GUI for testing the Robot Uprising robot

Fernando
02-2024
"""
import tkinter as tk
import socket

class RobotController:
    def __init__(self, master):
        self.master = master
        self.master.title("Micro Invaders Robot Controller")

        self.right_motor_value = tk.IntVar()
        self.left_motor_value = tk.IntVar()

        self.create_widgets()

    def create_widgets(self):
        # Right motor slider
        right_motor_label = tk.Label(self.master, text="Right Motor")
        right_motor_label.grid(row=0, column=0)
        right_motor_slider = tk.Scale(self.master, from_=-100, to=100, orient=tk.HORIZONTAL, variable=self.right_motor_value)
        right_motor_slider.grid(row=0, column=1)

        # Left motor slider
        left_motor_label = tk.Label(self.master, text="Left Motor")
        left_motor_label.grid(row=1, column=0)
        left_motor_slider = tk.Scale(self.master, from_=-100, to=100, orient=tk.HORIZONTAL, variable=self.left_motor_value)
        left_motor_slider.grid(row=1, column=1)

        # Send button
        send_button = tk.Button(self.master, text="SEND", command=self.send_command)
        send_button.grid(row=2, column=0, columnspan=2)

        # Stop button
        stop_button = tk.Button(self.master, text="STOP", command=self.stop_robot)
        stop_button.grid(row=3, column=0, columnspan=2)

        # IP address setup
        ip_label = tk.Label(self.master, text="IP Address:")
        ip_label.grid(row=4, column=0)
        self.ip_entry = tk.Entry(self.master)
        self.ip_entry.insert(0, "192.168.81.205")  # Default IP
        self.ip_entry.grid(row=4, column=1)

    def send_command(self):
        ip_address = self.ip_entry.get()
        right_motor = self.right_motor_value.get()
        left_motor = self.left_motor_value.get()
        command = f"{left_motor};{right_motor}"

        self.send_udp_packet(ip_address, command)

    def stop_robot(self):
        ip_address = self.ip_entry.get()
        command = "0;0"

        self.send_udp_packet(ip_address, command)

    def send_udp_packet(self, ip_address, command):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.sendto(command.encode(), (ip_address, 3000))
        udp_socket.close()

def main():
    root = tk.Tk()
    app = RobotController(root)
    root.mainloop()

if __name__ == "__main__":
    main()
