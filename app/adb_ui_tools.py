import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import ttkbootstrap as tb
from PIL import Image, ImageTk
import threading
import os

command_history = []

# Run adb command function
def run_adb_command(command, success_msg="", error_msg="ADB command failed", capture_output=True):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=capture_output)
        if success_msg:
            messagebox.showinfo("Success", success_msg)
        return result.stdout.strip() if capture_output else ""
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"{error_msg}\n{e}")
        return ""

# New Feature: Uninstall APK with user input for package name
def uninstall_apk():
    # Create a new top-level window for package input
    input_window = tk.Toplevel(app)
    input_window.title("Uninstall APK")

    # Create the text box for package input
    package_textbox = tk.Text(input_window, height=4, width=40)
    package_textbox.pack(pady=10)

    # Add placeholder text to the text box
    placeholder = "Enter Package Name"
    package_textbox.insert("1.0", placeholder)
    package_textbox.config(fg="grey")  # Set placeholder color

    # Function to handle focus-in event
    def on_focus_in(event):
        if package_textbox.get("1.0", "end-1c") == placeholder:
            package_textbox.delete("1.0", "end")
            package_textbox.config(fg="black")  # Change text color to black when typing starts

    # Function to handle focus-out event
    def on_focus_out(event):
        if package_textbox.get("1.0", "end-1c") == "":
            package_textbox.insert("1.0", placeholder)
            package_textbox.config(fg="grey")  # Reapply placeholder color

    # Bind focus events to remove or restore the placeholder text
    package_textbox.bind("<FocusIn>", on_focus_in)
    package_textbox.bind("<FocusOut>", on_focus_out)

    # Function to handle confirmation and uninstall
    def confirm_uninstall():
        # Get package name from the text box
        package_name = package_textbox.get("1.0", "end-1c").strip()

        if package_name != placeholder and package_name:
            # Confirmation dialog before uninstalling
            confirm = messagebox.askyesno("Confirm Uninstall", f"Are you sure you want to uninstall the app: {package_name}?")
            if confirm:
                run_adb_command(f'adb uninstall {package_name}', f"Uninstalled package: {package_name}")
                input_window.destroy()  # Close the input window after uninstall
        else:
            messagebox.showwarning("Invalid Input", "Please enter a valid package name.")

    # Button to confirm uninstall
    ttk.Button(input_window, text="Uninstall", command=confirm_uninstall).pack(pady=10)
    ttk.Button(input_window, text="Cancel", command=input_window.destroy).pack(pady=5)

    # Create a new top-level window for package input
    input_window = tk.Toplevel(app)
    input_window.title("Uninstall APK")

    # Label and entry for package name
    ttk.Label(input_window, text="Enter Package Name:").pack(pady=10)
    
    # Package entry text box
    package_entry = ttk.Entry(input_window, width=40)
    package_entry.pack(pady=5)
    
    # Textbox for accepting input package name
    package_textbox = tk.Text(input_window, height=4, width=40)
    package_textbox.pack(pady=10)
    
    # Function to handle confirmation and uninstall
    def confirm_uninstall():
        # Get package name from the text box
        package_name = package_textbox.get("1.0", "end-1c").strip()
        
        if package_name:
            # Confirmation dialog before uninstalling
            confirm = messagebox.askyesno("Confirm Uninstall", f"Are you sure you want to uninstall the app: {package_name}?")
            if confirm:
                run_adb_command(f'adb uninstall {package_name}', f"Uninstalled package: {package_name}")
                input_window.destroy()  # Close the input window after uninstall

    # Button to confirm uninstall
    ttk.Button(input_window, text="Uninstall", command=confirm_uninstall).pack(pady=10)
    ttk.Button(input_window, text="Cancel", command=input_window.destroy).pack(pady=5)

# New Feature: Push file to device
def push_file_to_device():
    file_path = filedialog.askopenfilename()
    if file_path:
        target_path = filedialog.askdirectory()
        if target_path:
            run_adb_command(f'adb push "{file_path}" "{target_path}"', f"Pushed file to: {target_path}")

# Function to send adb input text
def send_adb_input():
    text = input_entry.get()
    if text:
        run_adb_command(f'adb shell input text "{text}"', f"Sent text: {text}")

# Function to open language settings
def set_language():
    run_adb_command("adb shell am start -a android.settings.LOCALE_SETTINGS", "Opened language settings.")

# Function to reboot device
def reboot_device():
    run_adb_command("adb reboot", "Device rebooting...")

# Function to clear app data
def clear_app_data():
    package = package_entry.get()
    if package:
        run_adb_command(f'adb shell pm clear {package}', f"Cleared data for: {package}")

# Function to install APK
def install_apk():
    apk_path = filedialog.askopenfilename(filetypes=[("APK files", "*.apk")])
    if apk_path:
        run_adb_command(f'adb install "{apk_path}"', "APK installed successfully")

# Function to take screenshot
def take_screenshot():
    output_path = filedialog.asksaveasfilename(defaultextension=".png")
    if output_path:
        run_adb_command('adb shell screencap -p /sdcard/screen.png', capture_output=False)
        run_adb_command(f'adb pull /sdcard/screen.png "{output_path}"', f"Screenshot saved to: {output_path}")

# Function to record screen
def record_screen():
    output_path = filedialog.asksaveasfilename(defaultextension=".mp4")
    if output_path:
        run_adb_command('adb shell screenrecord /sdcard/recording.mp4', capture_output=False)
        run_adb_command(f'adb pull /sdcard/recording.mp4 "{output_path}"', f"Recording saved to: {output_path}")

# Function to list connected devices
def list_devices():
    output = run_adb_command("adb devices")
    messagebox.showinfo("Connected Devices", output if output else "No devices found.")

# Function to view logcat
def run_logcat():
    def open_logcat():
        log_window = tk.Toplevel(app)
        log_window.title("ADB Logcat")
        text_area = scrolledtext.ScrolledText(log_window, width=100, height=30)
        text_area.pack()
        process = subprocess.Popen("adb logcat", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            text_area.insert(tk.END, line)
            text_area.yview(tk.END)
    threading.Thread(target=open_logcat, daemon=True).start()

# Function to run custom adb commands
def run_custom_command():
    cmd = custom_entry.get().strip()
    if cmd:
        # Remove any leading "adb" to prevent duplication
        if cmd.lower().startswith("adb "):
            cmd = cmd[4:].strip()
        command_history.append(cmd)
        update_history()
        output = run_adb_command(f'adb {cmd}', f"Executed: adb {cmd}")
        if output:
            messagebox.showinfo("Output", output)

# Function to update history of executed commands
def update_history():
    history_box.delete(0, tk.END)
    for cmd in command_history[::-1]:
        history_box.insert(tk.END, cmd)

# Function to reuse command from history
def reuse_command(event):
    selection = history_box.get(history_box.curselection())
    custom_entry.delete(0, tk.END)
    custom_entry.insert(0, selection)

# Function to refresh device information
def refresh_device_info():
    ram = get_mem_available()
    cpu = run_adb_command('adb shell top -n 1 -b | head -n 10')
    info_label.config(text=f"📊 RAM: {ram.strip()} | {cpu.strip()}" if ram and cpu else "Device info unavailable")
    app.after(5000, refresh_device_info)

# Function to get available memory
def get_mem_available():
    output = run_adb_command('adb shell cat /proc/meminfo')
    for line in output.splitlines():
        if "MemAvailable" in line:
            return line.strip()
    return "MemAvailable info not found"

# Function to toggle theme
def toggle_theme():
    current = style.theme.name
    style.theme_use("darkly" if current == "flatly" else "flatly")

# Setup UI
style = tb.Style("flatly")
app = tb.Window(themename="flatly")
app.title("ADB Pro Dashboard")
app.geometry("800x700")

# Set custom icon using Pillow
icon_path = "ic_adb_ui_tools.jpeg"  # Path to your .jpeg icon file
try:
    image = Image.open(icon_path)
    photo = ImageTk.PhotoImage(image)
    app.iconphoto(True, photo)  # Set the icon
except Exception as e:
    print(f"Error setting app icon: {e}")

frame = ttk.Frame(app, padding=10)
frame.pack(fill="both", expand=True)

# Group 1: Device Manipulation
ttk.Label(frame, text="Device Manipulation").grid(row=0, column=0, columnspan=3, sticky="w", pady=10)
ttk.Button(frame, text="ADB Language Setting", command=set_language).grid(row=1, column=0, sticky="w", pady=5)
ttk.Button(frame, text="ADB Reboot", command=reboot_device).grid(row=1, column=1, sticky="w", pady=5)
ttk.Button(frame, text="Clear App Data", command=clear_app_data).grid(row=1, column=2, sticky="w", pady=5)
ttk.Button(frame, text="Uninstall APK", command=uninstall_apk).grid(row=2, column=0, sticky="w", pady=5)

# Group 2: Input Commands
ttk.Label(frame, text="Input Commands").grid(row=3, column=0, columnspan=3, sticky="w", pady=10)
ttk.Label(frame, text="ADB Input:").grid(row=4, column=0, sticky="e")
input_entry = ttk.Entry(frame, width=40)
input_entry.grid(row=4, column=1)
ttk.Button(frame, text="Send", command=send_adb_input).grid(row=4, column=2)

# Group 3: APK, Screenshot, Record
ttk.Label(frame, text="APK & Media").grid(row=5, column=0, columnspan=3, sticky="w", pady=10)
ttk.Button(frame, text="Install APK", command=install_apk).grid(row=6, column=0, sticky="w")
ttk.Button(frame, text="Screenshot", command=take_screenshot).grid(row=6, column=1, sticky="w")
ttk.Button(frame, text="Record Screen", command=record_screen).grid(row=6, column=2, sticky="w")
ttk.Button(frame, text="Push File to Device", command=push_file_to_device).grid(row=7, column=0, sticky="w")

# Group 4: Logs & Devices
ttk.Label(frame, text="Logs & Devices").grid(row=8, column=0, columnspan=3, sticky="w", pady=10)
ttk.Button(frame, text="View Logcat", command=run_logcat).grid(row=9, column=0, sticky="w")
ttk.Button(frame, text="List Devices", command=list_devices).grid(row=9, column=1, sticky="w")

# Group 5: Custom Commands
ttk.Label(frame, text="Custom ADB Cmd:").grid(row=10, column=0, sticky="e")
custom_entry = ttk.Entry(frame, width=40)
custom_entry.grid(row=10, column=1)
ttk.Button(frame, text="Run", command=run_custom_command).grid(row=10, column=2)

# Command History
ttk.Label(frame, text="History:").grid(row=11, column=0, sticky="ne", pady=10)
history_box = tk.Listbox(frame, height=5)
history_box.grid(row=11, column=1, columnspan=2, sticky="ew", pady=10)
history_box.bind('<<ListboxSelect>>', reuse_command)

# Device Info Label
info_label = ttk.Label(frame, text="📊 Device info will appear here", font=("Courier", 10))
info_label.grid(row=12, column=0, columnspan=3, pady=10)

# Start polling device info
refresh_device_info()

app.mainloop()
