from tkinter import *
from time import sleep

# Constants
PINK = '#e2979c'
RED = "#e7385b"
GREEN = '#76ABAE'
YELLOW = '#C7B7A3'
BLACK = '#31363F'
BLUE = '#124076'
FONT_NAME = 'Courier'
WORK_MIN = .2
SHORT_BREAK_MIN = .1
LONG_BREAK_MIN = 20
LAST_MIN = 5
COUNTER = 0
REPS = 0
WORK_COUNT = 0
timer = None

# ----------Timer reset

# --------- Timer mechanism


def start_countdown(**kwargs):
    global REPS
    global WORK_COUNT

    if timer:
        reset_timer()

    work_done.config(text=f"{'✔'*WORK_COUNT}")
    work_sec = WORK_MIN*60
    short_break_sec = SHORT_BREAK_MIN*60
    long_break_sec = LONG_BREAK_MIN*60
    REPS += 1

    if REPS % 8 == 0:
        timer_label.config(text='Long Break ', foreground=BLUE)
        countdown(long_break_sec)
    elif REPS % 2 == 0:
        timer_label.config(text='Break', foreground=GREEN)
        countdown(short_break_sec)
    else:
        timer_label.config(text='Work', foreground=RED)
        countdown(work_sec)

        WORK_COUNT += 1


def reset_timer():
    global REPS
    global WORK_COUNT

    WORK_COUNT = 0
    REPS = 0
    window.after_cancel(timer)
    timer_label.config(text='Timer', foreground=GREEN)
    canvas.itemconfig(timer_count, text='0:00')
    work_done.config(text='')


# ---------- Countdown Mechanism

def countdown(count):
    global timer
    count_min = int(count / 60)
    count_sec = str(int(count % 60))
    if len(count_sec) == 1:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_count, text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(1000, countdown, count-1)
    else:
        start_countdown()

# ---------- UI Setup


window = Tk()
window.title('Work timer')
window.config(padx=75, pady=25, bg=YELLOW)

# ---------------

canvas = Canvas(width=150, height=250, bg=YELLOW, highlightthickness=0)
stopwatch_img = PhotoImage(file='stopwatch.png')
canvas.create_image(75, 125, image=stopwatch_img)
timer_count = canvas.create_text(75, 130, text='00:00',
                                 font=(FONT_NAME, 22, 'bold'))
canvas.grid(column=1, row=1)

# -------------- labels

timer_label = Label(text='Timer', fg=GREEN,
                    background=YELLOW, font=(FONT_NAME, 25, 'bold'))
timer_label.grid(column=1, row=0)

work_done = Label(text="", background=YELLOW)
work_done.grid(column=1, row=2)

# -------------- buttons

start_button = Button(text='Start', width=10,
                      command=start_countdown)
start_button.grid(column=0, row=2)

reset_button = Button(text='Reset', width=10, command=reset_timer)
reset_button.grid(column=2, row=2)


window.mainloop()
