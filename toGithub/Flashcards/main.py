# did not finish this sadly

import customtkinter as ctk
from customtkinter import *
from PIL import Image
import pandas
import random
import os
from CTkMessagebox import CTkMessagebox
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')


MODES = ['Light', 'Dark']
CURRENT_TOPIC = None


logo = CTkImage(light_image=Image.open('images/icon.png'),
                dark_image=Image.open('images/icon.png'),
                size=(200, 200))

check = CTkImage(light_image=Image.open('images/check.png'),
                 dark_image=Image.open('images/check.png'),
                 size=(100, 100))

wrong = CTkImage(light_image=Image.open('images/wrong.png'),
                 dark_image=Image.open('images/wrong.png'),
                 size=(100, 100))

finished = CTkImage(light_image=Image.open('images/finished.png'),
                    dark_image=Image.open('images/finished.png'),
                    size=(250, 250))


def get_topics():
    subjects = os.listdir('data')
    topics = []
    for file in subjects:
        topics.append(file.strip('.csv').capitalize())
    return topics


TOPICS = get_topics()


def all_children(window):
    _list = window.winfo_children()

    for i in _list:
        if i.winfo_children():
            _list.extend(i.winfo_children())
    return _list


def end(window):
    window.destroy()
    window.quit()


def app_finished(frame, window, wrong=0, correct=0):

    def close_app():
        window.destroy()
        window.quit()

    done_img = CTkLabel(master=frame, text='', image=finished, width=400)
    done_img.grid(column=0, row=0, columnspan=3, padx=50, pady=50)

    right_lbl = CTkLabel(master=frame, text=f'Correct : {correct}')
    right_lbl.grid(column=0, row=1, padx=75, pady=20)

    wrong_lbl = CTkLabel(master=frame, text=f'Mistakes : {wrong}')
    wrong_lbl.grid(column=2, row=1, pady=20)

    quit_btn = CTkButton(master=frame, text='Quit', command=close_app)
    quit_btn.grid(column=1, row=2, padx=20, pady=20)


def center_window(window, width=650, height=500, padx=0, pady=0):
    window.title('Flashcards')
    window.config(padx=padx, pady=pady)
    # get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # calculate position x and y windowoordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))


def main_app(topic):
    correct_answers = 0
    wrong_answers = 0
    window = CTk()
    center_window(window, width=800)
    flashcard_data = pandas.read_csv(f"data/{topic}.csv").to_dict()

    def random_question(**kwargs):
        nonlocal current_question, current_answer, current

        if len(done) >= 5:  # the number of questions til end

            widget_list = all_children(window=main_frame)
            for item in widget_list:
                item.grid_forget()
            app_finished(main_frame, window, wrong=wrong_answers,
                         correct=correct_answers)
            return
        while True:
            random_pairnum = random.randint(
                0, len(flashcard_data['questions'])-1)
            if random_pairnum in done or flashcard_data['questions'][random_pairnum] == current:
                continue
            break
        question = flashcard_data['questions'][random_pairnum]
        answer = flashcard_data['answers'][random_pairnum]
        done.append(random_pairnum)
        try:
            flashcard.configure(text=question)
        except NameError:
            pass
        current_question, current_answer, current = question, answer, question

    def selected_mode(mode):
        print(mode)

    done = []
    answers = []
    skipped = []
    current_question, current_answer, current = None, None, None
    random_question()

    def flip_flashcard():
        nonlocal current
        if current == current_question:
            flashcard.configure(text=current_answer)
            current = current_answer
            return
        if current == current_answer:
            flashcard.configure(text=current_question)
            current = current_question
            return

    def next_flashcard(answer):
        nonlocal wrong_answers, correct_answers
        status = answer
        if status == 'wrong':
            wrong_answers += 1
        elif status == 'right':
            correct_answers += 1
        else:  # code to return to skipped cards
            done.pop()
        random_question()

    def wrong_answer():
        next_flashcard(answer='wrong')

    def right_answer():
        next_flashcard(answer='right')

    def skip_question():
        next_flashcard(answer='skip')

    # ------- Frames

    main_frame = CTkFrame(window, width=640, height=500,
                          fg_color='#151515', corner_radius=0)
    main_frame.pack(side='right', ipadx=10, ipady=50)
    main_frame.grid_propagate(False)

    side_frame = CTkFrame(window, width=160, height=500,
                          fg_color='#1A1A1B', corner_radius=0)
    side_frame.pack(side='left')
    side_frame.pack_propagate(False)

    # ------- Buttons

    flashcard = CTkButton(main_frame, text=current_question,
                          height=275, width=400, fg_color='#50727B', command=flip_flashcard)
    flashcard.grid(column=0, row=0, columnspan=3, padx=125, pady=40)

    check_btn = CTkButton(main_frame, text='', image=check,
                          width=50, command=right_answer)
    check_btn.grid(column=2, row=1, padx=10, pady=20)

    wrong_btn = CTkButton(main_frame, text='', image=wrong,
                          width=50, command=wrong_answer)
    wrong_btn.grid(column=0, row=1, padx=10, pady=20)

    skip_btn = CTkButton(main_frame, text='skip',
                         width=200, height=100, fg_color='#50727B', command=skip_question)
    skip_btn.grid(column=1, row=1, padx=10, pady=10)

    # ------- Menu

    appearance_menu = CTkOptionMenu(side_frame, values=MODES,
                                    width=120, command=selected_mode)
    appearance_menu.pack(side='bottom', padx=10, pady=20)
    appearance_menu.set('Mode')

    # ------ Labels

    appearance_lbl = CTkLabel(side_frame, text='Appearance')
    appearance_lbl.pack(side='bottom', padx=10)

    window.mainloop()

    # design later layout first


def add_flashcards(master):
    # goal is to finish the add flashcards window
    subjects = get_topics()
    selected_topic = None

    def move_window(master, window, width=550, height=300, padx=0, pady=0):
        # get screen width and height
        window.config(padx=padx, pady=pady)
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # calculate position x and y coordinates
        x = screen_width - width - 50
        y = (screen_height/2) - height
        window.geometry('%dx%d+%d+%d' % (width, height, x, y))
        window.wm_transient(master)

    def selected_sub(selected):
        nonlocal selected_topic
        selected_topic = selected

    def add_topic():

        def added_topic():
            new_topic = topic_entry.get().capitalize()
            msg = CTkMessagebox(
                title='Info', message=f"Are you sure you want to add {new_topic}?", option_2='Ok', option_1='Cancel')
            response = msg.get()

            if response == 'Ok':
                # if the file exists make one else tell them it already exists
                with open(f"data/{new_topic}.csv", 'w') as file:
                    file.write('questions,answers\n')
                topic_entry.delete(0, "end")

        def done_adding():
            end(topic_window)
            end(add_window)
            add_flashcards(master=master)

        topic_window = CTkToplevel()
        topic_window.title('Add Topic')
        center_window(window=topic_window, width=350,
                      height=200, padx=20, pady=20)
        topic_window.wm_transient(master=add_window)

        topic_entry = CTkEntry(
            master=topic_window, placeholder_text='What topic do you want to add', width=200)
        topic_entry.grid(column=0, row=0, padx=20, pady=20)

        done_btn1 = CTkButton(master=topic_window,
                              text='Done', command=done_adding)
        done_btn1.grid(column=0, row=1, padx=20, pady=20)

        add_btn = CTkButton(master=topic_window, text='Add',
                            width=10, command=added_topic)
        add_btn.grid(column=1, row=0, padx=20, pady=20)

    def finished():
        end(add_window)

    def add_question():
        question, answer = question_entry.get().capitalize(), answer_entry.get().capitalize()

        if question and answer:
            data = {'questions': [question], 'answers': [answer]}
            df = pandas.DataFrame(data)
            df.to_csv(f"data/{selected_topic}.csv",
                      mode='a', index=False, header=False)
            question_entry.delete(0, 'end')
            answer_entry.delete(0, 'end')

    add_window = CTkToplevel()
    add_window.title('Add flashcards')
    move_window(master=master, window=add_window, padx=20, pady=20)

    # ------ Labels

    sub_label = CTkLabel(add_window, text='Choose Topic :', font=('Arial', 15))
    sub_label.grid(column=0, row=0, padx=20, pady=20)

    add_question_lbl = CTkLabel(
        add_window, text='Question :', font=('Arial', 15))
    add_question_lbl.grid(column=0, row=1, padx=20, pady=20)

    add_answer = CTkLabel(add_window, text='Answer :', font=('Arial', 15))
    add_answer.grid(column=0, row=2, padx=20, pady=20)

    # ------ Entries

    question_entry = CTkEntry(
        add_window, width=200)
    question_entry.grid(column=1, row=1, padx=20, pady=20)
    question_entry.focus()

    answer_entry = CTkEntry(add_window, width=200)
    answer_entry.grid(column=1, row=2, padx=20, pady=20)

    # ------ Buttons

    add_btn = CTkButton(add_window, text='Add', width=50, command=add_question)
    add_btn.grid(column=2, row=2, padx=20, pady=20)

    done_btn = CTkButton(add_window, text='Done',
                         width=200, command=finished)
    done_btn.grid(column=1, row=3, columnspan=2, padx=20, pady=20)

    topic_btn = CTkButton(add_window, text='Add Topic',
                          width=75, command=add_topic)
    topic_btn.grid(column=2, row=0, padx=20, pady=20)

    # ------ Menu

    menu = CTkOptionMenu(add_window, values=subjects,
                         width=200, command=selected_sub)
    menu.grid(column=1, row=0, padx=20, pady=20)
    menu.set('Choose Subject')

    add_window.mainloop()
    # get back to this later


def starting_page():

    main_window = CTk()
    center_window(main_window)
    main_window.config(padx=50, pady=50)

    def launch_app():

        def selected_topic():
            global CURRENT_TOPIC
            CURRENT_TOPIC = radio_var.get()

        def done_choosing():
            end(window=window)
            if CURRENT_TOPIC is None:  # if true send info if not launch main app
                CTkMessagebox(
                    title="Error", message='Please choose a topic', icon='warning')
                launch_app()
            else:
                end(main_window)
                main_app(topic=CURRENT_TOPIC)

        window = CTk()
        radio_var = StringVar()
        center_window(window=window, width=300,
                      height=len(TOPICS)*100, padx=10, pady=10)
        window.title('Choose')

        for subject in TOPICS:
            topic = CTkRadioButton(
                window, text=subject, command=selected_topic, variable=radio_var, value=subject)
            topic.pack(padx=10, pady=10)

        done = CTkButton(window, text='Done', command=done_choosing)
        done.pack(side='bottom', pady=20)

        window.mainloop()

    def add():
        add_flashcards(main_window)

    # ------ labels

    # the icon still bad and i dont have money for photoshop
    icon_labels = CTkLabel(main_window, text='',  image=logo)
    icon_labels.grid(column=1, row=0, pady=50)

    # ----- buttons

    start_btn = CTkButton(main_window, text='Start', width=200,
                          height=50, corner_radius=32, fg_color='transparent',  border_color='#496989', border_width=3, command=launch_app)
    start_btn.grid(column=1, row=1, padx=10, pady=10)

    add_btn = CTkButton(main_window, text='Add Flashcards',
                        corner_radius=32, fg_color='transparent',  border_color='#496989', border_width=2, command=add)
    add_btn.grid(column=0, row=1, padx=10, pady=10)

    quit_btn = CTkButton(main_window, text='Quit',
                         corner_radius=32, fg_color='transparent',  border_color='#496989', border_width=2, command=quit)
    quit_btn.grid(column=2, row=1, padx=10, pady=10)

    main_window.mainloop()


starting_page()
