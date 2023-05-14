import tkinter as tk
from tkinter import ttk
import sqlite3 as sql
import time
import os
import webbrowser
import hashlib

con = sql.connect("lgns.db")
cursor = con.cursor()
hash_object = hashlib.sha256()

def open_browser():
    webbrowser.open('http://127.0.0.1:5500/1.html')

def back_button():
    try:
        reg_win.destroy()
    except:
        log_win.destroy()
    try:
        open_chg_win()
    except:
        cng_win.destroy()

if not os.path.exists("lgns.db"):
    cursor.execute("CREATE TABLE logins (lgns TEXT, psws TEXT)")

def register():
    global cursor
    psw = reg_psw_entr.get()
    print(psw)
    lgn = reg_lg_entr.get()
    print(lgn)
    psw_count = len(psw)
    psw_bytes = psw.encode('utf-8')
    hash_object.update(psw_bytes)
    psw = hash_object.hexdigest()
    
    lgn_count = len(lgn)
    print("Длина пароля: ", psw_count)
    print("Длина логина: ", lgn_count)
    if psw_count < 6:
        reg_err_lbl = ttk.Label(reg_win,text = "Минимальная длина логина 4 символа, а минимальная длина пароля 6 символов")
        reg_err_lbl.pack()
        print("Ошибка")
            
    elif lgn_count < 4:
            reg_err_lbl = ttk.Label(reg_win,text = "Минимальная длина логина 4 символа, а минимальная длина пароля 6 символов")
            reg_err_lbl.pack()
            print("Ошибка")
            time.sleep(1)
            reg_err_lbl.destroy         
    else:
        cursor.execute("""INSERT INTO logins (lgns,psws) VALUES (?, ?)""", (lgn, psw))
        con.commit()
        print("Записано")

def check_all(lgnch, pswch):
    print(lgnch)
    print(pswch)
        
def loginister():
    lpe = log_psw_entr.get()
    lle = log_log_entr.get()
    lpe_bytes = lpe.encode('utf-8')
    hash_object.update(lpe_bytes)
    cursor.execute('SELECT * FROM logins WHERE lgns = ? AND psws = ?', [lle, lpe])
    log_chk = cursor.fetchall()
    if log_chk:
        # If a match is found in the database, store the values in variables
        username = log_chk[0][0]
        password = log_chk[0][1]
        print("Username:", username)
        print("Password:", password)
    else:
        print("No match found in the database")

    lle = hash_object.hexdigest()
    print(lpe, lle)


def open_log_win():
    global log_log_entr
    global log_psw_entr
    global log_win
    cng_win.destroy()
    log_win = tk.Tk()
    log_win.geometry("500x500")
    log_win.title("Окно входа")
    log_psw_entr = ttk.Entry(log_win)
    log_psw_entr.pack()
    log_log_entr = ttk.Entry(log_win)
    log_log_entr.pack()
    log_btn1 = ttk.Button(log_win,text = "Залогиниться",command=loginister)
    log_btn1.pack()
    bck_btn1 = ttk.Button(log_win, text = "Назад", command = back_button)
    bck_btn1.pack()
    log_win.mainloop()

def open_reg_win():
    global reg_lg_entr
    global reg_psw_entr
    global reg_win
    cng_win.destroy()
    reg_win = tk.Tk()
    reg_win.geometry("500x500")
    reg_win.title("Окно регистрации")
    reg_lg_entr = ttk.Entry(reg_win)
    reg_lg_entr.pack()
    reg_psw_entr = ttk.Entry(reg_win)
    reg_psw_entr.pack()    
    reg_btn1 = ttk.Button(reg_win,text = "Зарегистрироваться",command=register)
    reg_btn1.pack()
    bck_btn = ttk.Button(reg_win, text = "Назад", command = back_button)
    bck_btn.pack()
    reg_win.mainloop()

def open_chg_win():
    global cng_win
    cng_win = tk.Tk()
    cng_win.geometry("500x500")
    cng_win.title("Окно выбора")
    reg_btn = ttk.Button(cng_win,text="Регистрация",command=open_reg_win)
    reg_btn.pack()
    log_btn = ttk.Button(cng_win,text="Войти",command=open_log_win)
    log_btn.pack()
    cng_win.mainloop()

open_chg_win()
