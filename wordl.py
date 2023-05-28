import tkinter as tk
from tkinter import ttk
import random

DB = (#https://7esl.com/5-letter-words/
    'Apple','Beach','Brain','Bread','Brush','Chair','Chest','Chord','Click',
    'Clock','Cloud','Dance','Diary','Drink','Earth','Flute','Fruit','Ghost',
    'Grape','Green','Happy','Heart','House','Juice','Light','Money','Music',
    'Party','Pizza','Plant','Radio','River','Salad','Sheep','Shoes','Smile',
    'Snack','Snake','Spice','Spoon','Storm','Table','Toast','Tiger','Train',
    'Water','Whale','Wheel','Woman','World','Write','Youth',
#uncommon
    'Abyss','Ample','Ankle','Aroma','Aural','Began','Blunt','Braid','Brisk',
    'Bumpy','Chive','Clasp','Crave','Crest','Cumin','Drape','Dregs','Dumpy',
    'Dusky','Dwell','Elite','Ember','Enact','Evade','Evoke','Fable','Flair',
    'Fluke','Folly','Gauze','Giddy','Gloom','Gorge','Gusty','Haste','Hilly',
    'Hippy','Hovel','Hunch','Icily','Inept','Inert','Irate','Ivory','Jaded',
    'Jazzy','Jolly','Joust','Jumpy','Kinky','Knack','Knave','Knead','Kudos',
    'Lanky','Latch','Lolly','Lurid','Mirth','Moody','Mourn','Mower','Muggy',
    'Nanny','Nappy','Nerve','Nifty','Nudge','Olive','Onset','Oomph','Ounce',
    'Ovals','Peppy','Pious','Pique','Plush','Poise','Quail','Quake','Quell',
    'Quill','Quirk','Ravel','Reedy','Ruddy','Runic','Sable','Spicy','Stilt',
    'Swath','Swirl','Toast','Tonic','Triad','Tryst','Tweak',
    )

remaining = list(DB)
GUESSES = 6
WORD_LENGTH = 5

def next_word():
    RANGE = len(DB)+1
    for word in range(RANGE):
        random_index = random.randint(0,RANGE)
        yield remaining.pop(random_index)
generator = next_word()

def new_word():
    try:
        return next(generator)
    except StopIteration:
        print('out of words')
        root.destroy()
    else: pass

class GuessingLine(tk.Frame):

    def __init__(self, master):
        super().__init__(master,relief='raised',bd=2)
        e_config = {
            'font'      : ('Helvetica', 32, 'bold'),
            'text'      : ' ',
            'justify'   : tk.CENTER,
            'width'     : 2,
            }
        p_config = {
            'side' : tk.LEFT,
            'padx' : (2,2),
            }

        def lock(w):
            existing    = 'EXISTING.TEntry'
            right       = 'RIGHT.TEntry'
            [e.configure(state='disabled') for e in self.entries]
            goal        = master.master.goal.upper()
            for idx,(c1,c2) in enumerate(zip(w,goal)):
                style = None
                if c1 in goal:
                    style = existing
                if c1 == c2:
                    style = right
                    master.master.insert_letter(idx, c1)
                if style:
                    self.entries[idx].configure(style=style)
            master.master.evaluate(w)
                
        
        def validate(e):
            if e.char.isalpha():
                if e.widget.get(): clear(e)
                if e.char.isupper(): char = e.char
                else: char = e.char.upper()
                e.widget.insert(tk.END, char)
                if e.widget is not self.entries[-1]:
                    e.widget.tk_focusNext().focus()
                else:
                    chars = [e.get() for e in self.content]
                    final = ''.join(chars)
                    if final.lower().title() in DB:
                        e.widget.tk_focusNext().focus()
                        lock(final)
            if e.keysym != 'Return':
                return 'break'
        
        def clear(e):
            if e.widget.get():
                e.widget.delete(0, tk.END)
            else:
                if e.widget is not self.entries[0]:
                    e.widget.tk_focusPrev().focus()
            return 'break'
                
        
        self.entries = []
        self.content = []

        def delegate(e):
            for entry in reversed(self.entries):
                if entry is not e.widget:
                    entry.delete(0, tk.END)
                else: break                
        
        for i in range(WORD_LENGTH):
            sv = tk.StringVar(self)
            self.content.append(sv)
            e = ttk.Entry(self, **e_config, textvariable=sv)
            self.entries.append(e)
            e.bind('<Key>', validate)
            e.bind('<BackSpace>', clear)
            e.bind('<Delete>', clear)
            e.bind('<FocusIn>', delegate)
            e.pack(**p_config)
            
    def clear(self):
        for e in self.entries:
            e.configure(style='TEntry', state='normal')
            e.delete(0, tk.END)

class AnswerFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master,relief='raised',bd=2)
        e_config = {
            'font'      : ('Helvetica', 32, 'bold'),
            'text'      : ' ',
            'justify'   : tk.CENTER,
            'width'     : 2,
            'state'     : 'readonly',
            'style'     : 'ANSWER.TEntry',
            }
        p_config = {
            'side' : tk.LEFT,
            'padx' : (2,2),
            'expand' : True,
            }
        self.content = []
        for i in range(WORD_LENGTH):
            sv = tk.StringVar(self)
            self.content.append(sv)
            e = ttk.Entry(self, **e_config, textvariable=sv)
            e.pack(**p_config)
    def clear(self):
        for sv in self.content:
            sv.set('')
        

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.configure(bd=2)
        self.try_frame = tk.Frame(self,relief='sunken',bd=2)
        for i in range(GUESSES):
            GuessingLine(self.try_frame).pack(ipadx=1,ipady=2)
        self.answ_frame = AnswerFrame(self)
        
        self.try_frame.pack()
        self.answ_frame.pack(ipadx=1,ipady=2,fill=tk.X, expand=True)
        
        self.focus_upper_left()
        self.goal = new_word()
        self.bind_all('<Return>', self.change_goal)
        

    def focus_upper_left(self):
        w = self.try_frame.winfo_children()[0].winfo_children()[0]
        w.focus()

    def insert_letter(self, idx, char):
        self.answ_frame.content[idx].set(char)

    def change_goal(self, event):
        if self.solved:
            for child in self.try_frame.winfo_children():
                child.clear()
            self.answ_frame.clear()
            self.focus_upper_left()
            self.goal = new_word()
            self.solved = False

    def evaluate(self, word):
        if self.goal.upper() == word:
            self.solved = True

root = App()
style = ttk.Style(root)
style.element_create("plain.field", "from", "clam")
style.layout("RIGHT.TEntry",
             [('Entry.plain.field', {'children': [(
                 'Entry.background', {'children': [(
                     'Entry.padding', {'children': [(
                         'Entry.textarea', {'sticky': 'nswe'})],
                                       'sticky': 'nswe'})], 'sticky': 'nswe'})],
                                     'border':'2', 'sticky': 'nswe'})])
style.configure("RIGHT.TEntry",
                 foreground="white",
                 fieldbackground="green")
style.map('RIGHT.TEntry',
          foreground = [('disabled', '#ffffff')])
style.layout("EXISTING.TEntry",
             [('Entry.plain.field', {'children': [(
                 'Entry.background', {'children': [(
                     'Entry.padding', {'children': [(
                         'Entry.textarea', {'sticky': 'nswe'})],
                                       'sticky': 'nswe'})], 'sticky': 'nswe'})],
                                     'border':'2', 'sticky': 'nswe'})])
style.configure("EXISTING.TEntry",
                 foreground="white",
                 fieldbackground="orange")
style.layout("ANSWER.TEntry",
             [('Entry.plain.field', {'children': [(
                 'Entry.background', {'children': [(
                     'Entry.padding', {'children': [(
                         'Entry.textarea', {'sticky': 'nswe'})],
                                       'sticky': 'nswe'})], 'sticky': 'nswe'})],
                                     'border':'2', 'sticky': 'nswe'})])
style.map('ANSWER.TEntry',
          foreground = [('readonly', '#000000')],
          fieldbackground = [('readonly', '#5fffa3')],
          )
root.mainloop()

