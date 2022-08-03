# Importing required libraries
import difflib
from tkinter import *
from tkinter import scrolledtext

# Tkinter GUI window setup - window resolution, background color, and title
window = Tk()
window.geometry("1280x720")
window.configure(bg="white") 
window.title("Spell Check")

# Calculating the width and height center to better position elements
w_center = 1280/2
h_center = 720/2

# Headline Label widget
headline = Label(window,  text="Spell Checker", bg="white", fg="#0e0e0e", font=("Raleway", 48))
headline.place(x = w_center, y = h_center-250, anchor="center")

# List of language options
langs = [ "English", "Slovak", "German" ]

# Setting default language
lang = StringVar(window)
lang.set(langs[0])

# Select language Label widget
select_language = Label(window, text="Select language", bg="white", fg="#0e0e0e", font=("Raleway", 18))
select_language.place(x = w_center, y = h_center-200, anchor="center")

# Language switcher OptionMenu widget
lang_switcher = OptionMenu(window, lang, *langs)
lang_switcher.config(fg="#96b9ec", bg="white")
lang_switcher.place(x = w_center, y = h_center-170, anchor="center")

# Input Label widget
input_label = Label(window, text="Write the text here to check its spelling:", bg="white", fg="#0e0e0e", font=("Raleway", 18))
input_label.place(x = w_center-300, y = h_center-150, anchor="center")
# Input area widget
input_area = scrolledtext.ScrolledText(window,
                                    wrap=WORD, 
                                    bg="#d8dde8",
                                    insertbackground="#0e0e0e",
                                    highlightthickness=0,
                                    bd=0,
                                    fg="#0e0e0e",
                                    padx=20,
                                    pady=20,
                                    width=40,
                                    height=10,
                                    font=("Raleway", 18)
                                )
input_area.place(x = w_center-300, y = h_center, anchor="center")

# Output Label widget
output_label = Label(window, text="Result of spell check:", bg="white", fg="#0e0e0e", font=("Raleway", 18))
output_label.place(x = w_center+300, y = h_center-150, anchor="center")
# Output area widget
output_area = scrolledtext.ScrolledText(window,
                                    wrap=WORD,
                                    state=DISABLED,
                                    bg="#d8dde8",
                                    highlightthickness=0,
                                    bd=0,
                                    fg="#0e0e0e",
                                    padx=20,
                                    pady=20,
                                    width=40,
                                    height=10,
                                    font=("Raleway", 18)
                                )
output_area.place(x = w_center + 300, y = h_center, anchor="center")

# Configuring Output area text to different color based on text tag
output_area.tag_config("correct", foreground="green")
output_area.tag_config("typo", foreground="red")

# Submit button that triggers function submit_input()
submit_button = Button(window,
                    text="Check spelling",
                    width=15,
                    height=2,
                    fg="#96b9ec",
                    highlightbackground="white",
                    font=("Raleway", 18),
                    command=lambda: submit_input())
submit_button.place(x = w_center, y = h_center+200, anchor="center")

# Typos counter Label widget
typos_count_text = StringVar()
typos_count_text.set("Typo count: 0")
typos_count_label = Label(window, textvariable=typos_count_text, bg="white", fg="#0e0e0e", font=("Raleway", 18))
typos_count_label.place(x = w_center+300, y = h_center+200, anchor="center")

# Word counter widget
word_count_text = StringVar()
word_count_text.set("Word count: 0")
word_count_label = Label(window, textvariable=word_count_text, bg="white", fg="#0e0e0e", font=("Raleway", 18))
word_count_label.place(x = w_center+300, y = h_center+240, anchor="center")

# Characters counter widget
character_count_text = StringVar()
character_count_text.set("Character count: 0")
character_count_label = Label(window, textvariable=character_count_text, bg="white", fg="#0e0e0e", font=("Raleway", 18))
character_count_label.place(x = w_center+300, y = h_center+280, anchor="center")


def spell_check(word, dictionary, typo_count):
    # removing trailing non-alphabetic characters from word (removing . ? ! , 0-9 etc.)
    word_alpha = word.lower()
    while not word_alpha[-1].isalpha():
        word_alpha = word_alpha[:-1]
        
        # if word consists only from non-alphabetic characters and we removed all of them
        if word_alpha == "":
            break
    
    for i in range(0, len(dictionary)):
        # if word found in dictionary = insert it in output_area and assign "correct" tag to it
        # (so it will be green color)
        if dictionary[i] == word_alpha:
            output_area.insert(END, word + " ", "correct")
            return typo_count
    
    # word was not found in dictionary = insert it in output_area and assign "typo" tag to it
    # (so it will be red color)
    output_area.insert(END, word + " ", "typo")
    typo_count += 1

    return typo_count

# Function that triggers pressing submit button
def submit_input():
    typo_count = 0
    
    # unlocks editing of output_area so program can insert text in it
    output_area.config(state=NORMAL) 
    # clears output_area
    output_area.delete("1.0", END) 

    # load dictionary file to a list acording to selected language 
    dictionary = [ line.strip().lower() for line in open("dictionary_" + lang.get() + ".txt") ]
    
    # load input as string from input_area widget 
    input = input_area.get("1.0","end-1c")
    
    # separate input string to list of words
    word_list = input.split()
    
    for word in word_list:
        typo_count = spell_check(word, dictionary, typo_count)
    
    # locks editing of output_area so user can not insert text in it = read-only mode
    output_area.config(state=DISABLED)
    
    # Set typos, words, characters counter
    typos_count_text.set("Typo count: " + str(typo_count))
    word_count_text.set("Word count: " + str(len(word_list)))
    character_count_text.set("Character count: " + str(len(input.replace(" ", ""))))

# Tkinter main loop
window.mainloop()