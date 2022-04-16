import os
import hashlib
from db import *


def hashPassword(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    storage = salt + key
    return storage


def checkUsername(username):
    users_ref = db.collection(u'users')
    docs = users_ref.stream()
    for doc in docs:
        if doc.id == username:
            return True
    return False


def checkPassword(password, username):
    ref = db.collection(u'users').document(username).get()
    if ref.exists:
        salt = ref.to_dict()['salt']
        key = ref.to_dict()['key']
        password.encode("utf-8")
        new_key = hashlib.pbkdf2_hmac(
            "sha256", password.encode('utf-8'), salt, 100000)
        if new_key == key:
            return True
        else:
            return False


running = True
while running:
    userInput = input("Press 1 to login, 2 to register, 3 to exit: ")
    if userInput == "1":
        print("Login")
        username = input("Enter username: ")
        password = input("Enter password: ")
        if not checkUsername(username):
            print("Username does not exist")
        if checkPassword(password, username):
            print(f"Password is correct, welcome {username}")

    elif userInput == "2":
        print("Sign up")
        username = input("Enter username: ")
        password = input("Enter password: ")
        if checkUsername(username):
            print("Username already exists")
            running = False
        storage = hashPassword(password)
        username.encode("utf-8")
        doc_ref = db.collection(u"users").document(username)
        doc_ref.set({
            u'key': storage[32:],
            u'salt': storage[:32]
        })
    elif userInput == "3":
        print("Bye bye!")
        running = False
