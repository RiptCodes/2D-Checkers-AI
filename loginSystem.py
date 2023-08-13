import tkinter as tk
from tkinter import *
from tkinter import messagebox
import csv
from main import checkers
import re
from PIL import ImageTk, Image


class system:

  def __init__(self):
    self.users = {}
    self.load_users()

  def load_users(self):
    try:
      with open("users.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
          username = row["username"]
          password = row["password"]
          self.users[username] = password
    except FileNotFoundError:
      pass

  def save_users(self):
    with open("users.csv", "a", newline= '') as f:
      writer = csv.writer(f, delimiter=",")
      for username, password in self.users.items():
        writer.writerow([username, password])

  def add_user(self, username, password):
    if username in self.users:
      return False
    else:
      self.users[username] = password
      self.save_users()
      return True

  def login(self, username, password):
    if username in self.users and self.users[username] == password:
      return True
    else:
      return False


class screen(system):
  def __init__(self, login_system):
    self.login_system = login_system
    super().__init__()

    self.window = tk.Tk()
    self.window.configure(bg="white")
    self.window.title("Sign in")
    self.window.geometry("500x600")

    self.frame = tk.Frame(self.window)
    self.frame.configure(bg="white")
    self.frame.pack(expand=False)
    self.checker_title = tk.Label(self.frame, text = " Checkers",
                fg = "#63b649",
                font = ("Helvetica bold", 50),
                bg="white"
                                 )
    
    self.checker_title.grid(row=0, column=1, pady=10)
    self.username_label = tk.Label(self.frame, text="Username:", bg="white")
    self.username_label.grid(row=1, column=0, pady=10)

    self.username_entry = tk.Entry(self.frame, background="light grey", border=2)
    self.username_entry.grid(row=1, column=1, pady=10)

    self.password_label = tk.Label(self.frame, text="Password:", bg="white")
    self.password_label.grid(row=2, column=0, pady=10)

    self.password_entry = tk.Entry(self.frame, show="*", background="light grey", border=2)
    self.password_entry.grid(row=2, column=1, pady=10)

    self.login_button = tk.Button(self.frame, text="Login", command=self.login, font=("bold"))
    self.login_button.grid(row=3, column=0, pady=10)

    self.signup_button = tk.Button(self.frame, text="Sign up", command=self.signup, font=("bold"))
    self.signup_button.grid(row=3, column=1, pady=10)

    self.window.update_idletasks()
    w = self.window.winfo_width()
    fw = self.frame.winfo_width()
    self.frame.place(x=(w-fw)/2, y=120)
    
    image = Image.open("settings_cog.png")
    image = image.resize((50, 50), Image.ANTIALIAS)
    self.image = ImageTk.PhotoImage(image) 
    self.canvas = tk.Canvas(self.window, width=50, height=50, highlightthickness=0, background="white")
    self.canvas.configure(background="white")
    self.canvas.create_image(25, 25, image=self.image)
    self.canvas.pack(side="right", padx=10)

  
  
  
  
  
  def login(self):
    username = self.username_entry.get()
    password = self.password_entry.get()
    if self.login_system.login(username, password):
      print("Login successful!")
      self.window.destroy()
      checkers.play()
    else:
      messagebox.showerror("Invalid Password", "Invalid username or password!")

  def signup(self):
    username = self.username_entry.get()
    password = self.password_entry.get()
    if not username or not password:
      messagebox.showerror("Error", "Username and password cannot be empty")
    elif not self.check_password(password):
      messagebox.showerror("Error", "Password is too weak")
    elif username in system().users:
      messagebox.showerror("Error", "Username already exists")
    else:
      self.users[username] = password
      self.save_users()
      messagebox.showinfo("Success", "User created successfully")
      checkers.play()

  
  def check_password(self, password):
      # check if password is strong enough
      if len(password) < 8:
          return False
      if re.search("[a-z]", password) is None:
          messagebox.showerror("Error","Your password should contain: \n Lower case(1) \n Upper case(1) \n Numbers(atleast 1) \n Special Character[]")
          return False
      if re.search("[A-Z]", password) is None:
          return False
      if re.search("[\d]", password) is None:
          return False
      if re.search("[\W]", password) is None:
          return False  
      return True


login_system = system()
login_screen = screen(login_system)
login_screen.window.mainloop()
