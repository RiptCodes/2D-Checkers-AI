import tkinter as tk
from tkinter import *

class screen():
  def __init__(self):
    self.window = tk.Tk()
    self.window.title("Sign in")
    self.window.minsize(600, 600)
    self.window.maxsize(600, 600)
    
    self.username_label = tk.Label(self.window, text="Username:")
    self.username_label.grid(column=2, row=4, padx=60)

    self.username_entry = tk.Entry(self.window)
    self.username_entry.grid(column=3, row=4, ipadx=50)

    self.password_label = tk.Label(self.window, text="Password:")
    self.password_label.grid(column=2, row=5, padx=60)

    self.password_entry = tk.Entry(self.window, show="*")
    self.password_entry.grid(column=3, row=5, ipadx=50)

    self.login_button = tk.Button(self.window,
                                  text="Login",
                                  command=self.login)
    self.login_button.grid(row=2, column=2)

    self.signup_button = tk.Button(self.window,
                                   text="Sign up",
                                   command=self.signup)
    self.signup_button.grid(row=3, column=2)