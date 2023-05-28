import tkinter as tk

q_and_a = {
    'How old are you?' : [
        16, #0
        18, #1
        21, #2
        48],#3
    'Where do you live?' : [
        'USA',
        'India',
        'England',
        'Syria'],
    }

right_answer = {
    'How old are you?' : 0,
    'Where do you live?' : 2,
    }

def generate_q_and_a():
    for k,v in q_and_a.items():
        yield k,v
generator = generate_q_and_a()

def next_question():
    try:
        q, a = next(generator)
    except StopIteration:
        print('all questions have solved')
        root.destroy()
    else:
        question.config(text = q)
        for idx,child in enumerate(answer_frame.winfo_children()):
            child.config(text=a[idx])

def answer_selected(n):
    current_question = question.cget('text')
    valid = n == right_answer[current_question]
    if valid:
        next_question()
    else:
        print('wrong answer')

BACKGROUND = 'grey'
FOREGROUND = 'black'

root = tk.Tk()
#content of root
question = tk.Label(
    root, text='', bg=BACKGROUND, fg=FOREGROUND, relief=tk.RIDGE)
answer_frame = tk.Frame(
    root, bg = BACKGROUND, borderwidth=2, relief=tk.SUNKEN)
#geometry of root
question.pack(fill=tk.BOTH, expand=True)
answer_frame.pack(fill=tk.BOTH, expand=True)
#content of answer_frame
choice_config = {
    'master' : answer_frame,
    'text' : '',
    'relief' : tk.RAISED,
    'borderwidth' : 1,
    'background' : 'grey',
    'foreground' : 'white',
    }
for i in range(4):
    callback = lambda n=i: answer_selected(n)
    choice = tk.Button(**choice_config, command=callback)
    choice.pack(fill=tk.BOTH, expand=True)
#start application
next_question()
root.mainloop()

