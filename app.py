import customtkinter as ctk
from PIL import Image
import cohere, json, webbrowser, string, subprocess, random, keyboard, threading, os

def lb_gen_password(length):
    alphabet = " !#$%&'()*+,-./:;<=>?@[]^_`{|}~\\" + string.ascii_letters + string.digits
    pwd = ""
    i = 0
    while i < int(length):
        pwd = pwd + random.choice(alphabet)
        i = i + 1
    return pwd
def lb_vigenere(message, key, direction=1):
    alphabet = " !#$%&'()*+,-./:;<=>?@[]^_`{|}~\\" + string.ascii_letters + string.digits
    key_index = 0
    encrypted_message = ''
    for char in message:
        key_char = key[key_index % len(key)]
        key_index += 1
        offset = alphabet.index(key_char)
        index = alphabet.find(char)
        new_index = (index + offset*direction) % len(alphabet)
        encrypted_message += alphabet[new_index]
    return encrypted_message
def lb_decrypt(message, key):
    return lb_vigenere(message, key, -1)
def lb_encrypt(message, key):
    return lb_vigenere(message, key)
def lb_autocomplete(search, key):
    possible_search = []
    for i in key_words:
        if i["name"][:len(search)] == search:
            possible_search.append(i)
    if len(possible_search) != 0 and search != "":
        label_autocomplete.configure(text=possible_search[0]["name"][len(search):])
        label_autocomplete.place(x=(130 + 8.8 * len(search)), y=8.5)
    elif search != "":
        label_autocomplete.configure(text="")
        label_autocomplete.place(x=1000, y=1000)
    else:
        label_autocomplete.configure(text="Enter a command")
        label_autocomplete.place(x=130, y=8.5)
    if key.char == "\r" and len(possible_search) != 0:
        to_do_request.set(possible_search[0]["name"] + " ")
        lb_reset_colors(possible_search)
        to_do.icursor("end")
    elif key.char == '\r':
        global found_command
        request = to_do_request.get().strip().split(" ")
        command = request.pop(0)
        found_command = False
        for i in key_words:
            if i["name"] == command:
                if i["type"] == "Website":
                    lb_to_website(request, i)
                elif i["type"] == "AI":
                    lb_cohere_request(request)
                elif i["type"] == "Software":
                    lb_to_software(i)
                found_command = True
        if not found_command:
            found_command = True
            PopUp(root, "Error", "200x100", "This command doesn't exist", color_index)
        for i in console_element_list:
            i.pack_forget()
            i.pack(fill="x", pady=10)
        to_do_request.set(command + " ")
def lb_cohere_request(request):
    separator = " "
    request = separator.join(request)
    console_response = ctk.CTkTextbox(console_box, fg_color="#2E2E2E", text_color=colors[key_words[0]["index_color"]]["color_text_input"], font=("Monospace", 18), corner_radius=20)
    console_element_list.insert(0, console_response)
    try:
        response = co.chat(message=request).text
        console_response.insert("0.0", f'Question : {request}\n\n' + response)
    except:
        console_response.insert("0.0", "ERROR")
    console_response.configure(state="disabled")
def lb_to_website(request, e):
    lb_send_log(e, f"   Search \"{" ".join(request)}\" on {e["name"]} ({e["adress"]})")
    separator = "+"
    request = separator.join(request)
    webbrowser.open(f"https://www.{e["adress"]}/{e["search_query"] + request}")
def lb_to_software(e):
    lb_send_log(e, f"   Execute \"{e["name"]}\"")
    try:
        subprocess.Popen([e["path"]])
    except:
        try:
            os.startfile(e["path"])
        except:
            PopUp(root, "Error", "200x100", "Wrong path to executable file", color_index)
def lb_send_log(e, message):
    try:
        image = Image.open(e["icon"])
    except:
        image = Image.open("./assets/img/iconDefault.jpg")
    console_response = ctk.CTkLabel(console_box, image=ctk.CTkImage(light_image=image, dark_image=image, size=(48, 48)), compound="left", text=message, fg_color="#2E2E2E", text_color="#ffffff", font=("Monospace", 18), corner_radius=20)
    console_element_list.insert(0, console_response)
def lb_reset_colors(possible_search):
    global color_index
    color_index = possible_search[0]["index_color"]
    to_do.configure(fg_color=colors[color_index]["fg_color"], border_color=colors[color_index]["border_color"], text_color=colors[color_index]["color_text_input"])
    label_autocomplete.configure(text="", fg_color=colors[color_index]["fg_color"])
    console_box.configure(fg_color=colors[color_index]["fg_color"], border_color=colors[color_index]["border_color"], scrollbar_button_color=colors[color_index]["border_color"], scrollbar_button_hover_color=colors[color_index]["hover"])
    tabs.configure(text_color=colors[color_index]["color_text_input"], segmented_button_fg_color=colors[color_index]["fg_color"], segmented_button_selected_color=colors[color_index]["border_color"], segmented_button_selected_hover_color=colors[color_index]["border_color"], segmented_button_unselected_color=colors[color_index]["fg_color"], segmented_button_unselected_hover_color=colors[color_index]["hover"])
    back_grounder.configure(scrollbar_button_color=colors[color_index]["border_color"], scrollbar_button_hover_color=colors[color_index]["hover"])
    label_add_action.configure(fg_color=colors[color_index]["hover"], text_color=colors[color_index]["color_text_input"])
    name_add_action.configure(fg_color=colors[color_index]["fg_color"], text_color=colors[color_index]["color_text_input"], border_color=colors[color_index]["border_color"])
    name_label.configure(fg_color=colors[color_index]["fg_color"])
    icon_add_action.configure(fg_color=colors[color_index]["fg_color"], text_color=colors[color_index]["color_text_input"], border_color=colors[color_index]["border_color"])
    icon_label.configure(fg_color=colors[color_index]["fg_color"])
    combo_add_action.configure(fg_color=colors[color_index]["fg_color"], text_color=colors[color_index]["color_text_input"], border_color=colors[color_index]["border_color"], button_color=colors[color_index]["fg_color"], dropdown_fg_color=colors[color_index]["fg_color"], dropdown_hover_color=colors[color_index]["hover"], dropdown_text_color=colors[color_index]["color_text_input"])
    color_add_action.configure(fg_color=colors[color_index]["fg_color"], text_color=colors[color_index]["color_text_input"], border_color=colors[color_index]["border_color"], button_color=colors[color_index]["fg_color"], dropdown_fg_color=colors[color_index]["fg_color"], dropdown_hover_color=colors[color_index]["hover"], dropdown_text_color=colors[color_index]["color_text_input"])
    adress_add_action.configure(fg_color=colors[color_index]["fg_color"], text_color=colors[color_index]["color_text_input"], border_color=colors[color_index]["border_color"])
    adress_label.configure(fg_color=colors[color_index]["fg_color"])
    query_add_action.configure(fg_color=colors[color_index]["fg_color"], text_color=colors[color_index]["color_text_input"], border_color=colors[color_index]["border_color"])
    query_label.configure(fg_color=colors[color_index]["fg_color"])
    path_add_action.configure(fg_color=colors[color_index]["fg_color"], text_color=colors[color_index]["color_text_input"], border_color=colors[color_index]["border_color"])
    path_label.configure(fg_color=colors[color_index]["fg_color"])
    button_add_action.configure(fg_color=colors[color_index]["fg_color"], text_color=colors[color_index]["color_text_input"], border_color=colors[color_index]["border_color"], hover_color=colors[color_index]["hover"])
    label_remove_action.configure(fg_color=colors[color_index]["hover"], text_color=colors[color_index]["color_text_input"])
    num_remove_action.configure(fg_color=colors[color_index]["fg_color"], border_color=colors[color_index]["border_color"])
    num_label.configure(fg_color=colors[color_index]["fg_color"])
    button_remove_action.configure(fg_color=colors[color_index]["fg_color"], text_color=colors[color_index]["color_text_input"], border_color=colors[color_index]["border_color"], hover_color=colors[color_index]["hover"])
def lb_handle_type_action(value):
    combo_add_action.pack_forget()
    color_add_action.pack_forget()
    button_add_action.pack_forget()
    label_remove_action.pack_forget()
    num_remove_action.pack_forget()
    num_label.place(x=1000, y=1000)
    info_remove_action.pack_forget()
    button_remove_action.pack_forget()
    if value == "Website":
        adress_add_action.pack(pady=5)
        query_add_action.pack(pady=5)
        adress_label.place(x=269, y=133)
        query_label.place(x=269, y=171)
        path_add_action.pack_forget()
        path_label.place(x=1000, y=1000)
        num_label.place(x=269, y=406)
    else:
        adress_add_action.pack_forget()
        query_add_action.pack_forget()
        path_add_action.pack(pady=5)
        adress_label.place(x=1000, y=1000)
        query_label.place(x=1000, y=1000)
        path_label.place(x=269, y=133)
        num_label.place(x=269, y=369)
    combo_add_action.pack(pady=5)
    color_add_action.pack(pady=5)
    button_add_action.pack(pady=15)
    label_remove_action.pack(pady=10)
    num_remove_action.pack(pady=20)
    info_remove_action.pack()
    button_remove_action.pack(pady=10)
def lb_show_placeholder(value, text, label, x, y):
    if text == 'Num':
        if combo_add_action.get() == 'Software':
            x, y = 269, 369
        else:
            x, y = 269, 406
    if value.get() == "":
        label.configure(text=text, font=("Monospace", 15))
        label.place(x=x, y=y)
    else:
        label.configure(text="", font=("Monospace", 1))
        label.place(x=1000, y=1000)
def lb_add_new_action():
    global index
    index = 0
    for i in range(len(colors)):
        if colors[i]["name"] == color_add_action.get():
            index = i
    if combo_add_action.get() == "Website":
        if name_new_action.get() != "" and adress_new_action.get() != "" and query_new_action.get() != "":
            key_words.append({"name": name_new_action.get(), "type": combo_add_action.get(), "index_color": index, "adress": adress_new_action.get(), "search_query": query_new_action.get(), "icon": icon_add_action.get(), "path": ""})
            adress_new_action.set("")
            query_new_action.set("")
            lb_show_placeholder(adress_new_action, "Adress", adress_label, 250, 133)
            lb_show_placeholder(query_new_action, "Search query", query_label, 250, 171)
        else:
            PopUp(root, "Error", "200x100", "Missing arguments", color_index)
            return
    elif combo_add_action.get() == "Software":
        if name_new_action.get() != "" and path_add_action.get() != "":
            key_words.append({"name": name_new_action.get(), "type": combo_add_action.get(), "index_color": index, "adress": "", "search_query": "", "icon": icon_add_action.get(), "path": path_add_action.get()})
        else:
            PopUp(root, "Error", "200x100", "Missing arguments", color_index)
            return
        path_new_action.set("")
        lb_show_placeholder(path_new_action, "Path's file", path_label, 250, 133)
    with open("./assets/json/command_info.json", "w", encoding="utf-8") as data:
        data.write(lb_encrypt(f'{key_words}', encrypt_key))
    info_remove_action.configure(text=lb_refresh_command())
    name_new_action.set("")
    icon_new_action.set("")
    lb_show_placeholder(name_new_action, "Command's name", name_label, 269, 58)
    lb_show_placeholder(icon_new_action, "Icon's path", icon_label, 269, 95)
    combo_add_action.set("Software")
    color_add_action.set("Red")
    lb_handle_type_action("Software")
def lb_new_key(data):
    data["DECRYPT"] = lb_gen_password(random.randint(100, 150))
    with open("./assets/json/env_var.json", "w", encoding="utf-8") as sens:
        sens.write(json.dumps(data))
def lb_listen_key():
    keyboard.add_hotkey('ctrl+shift+x', lb_handle_window)
    keyboard.wait()
def lb_handle_window():
    if root.state() == "normal":
        root.withdraw()
    else:
        root.deiconify()
        root.lift()
def lb_refresh_command():
    stringer = ''
    for i in range(len(key_words)):
        stringer += f'[{i}] - {key_words[i]['name']}\n'
    return stringer
def lb_remove_action():
    if num_delete_action.get() != '':
        try:
            key_words.pop(int(num_delete_action.get()))
            num_delete_action.set('')
            lb_show_placeholder(num_delete_action, "Num", num_label, 0, 0)
            info_remove_action.configure(text=lb_refresh_command())
            with open("./assets/json/command_info.json", "w", encoding="utf-8") as data:
                data.write(lb_encrypt(f'{key_words}', encrypt_key))
        except:
            PopUp(root, "Error", "200x100", "Invalid argument", color_index)
    else:
        PopUp(root, "Error", "200x100", "Missing argument", color_index)

class App(ctk.CTk):
    def __init__(self, title, dimension):
        super().__init__()
        self.title(title)
        self.iconbitmap("./assets/img/logoRaycast.ico")
        self.geometry(dimension)
        self.resizable(width=False, height=False)
        self.configure(fg_color="#1D1D1D")
        self.actived = False
    def activerter(self):
        super().__init__()
        if self.actived:
            self.actived = False
            self.withdraw()
        else:
            self.actived = True
            self.deiconify()
            self.lift()
class PopUp(ctk.CTkToplevel):
    def __init__(self, master, title, dimension, message, color):
        super().__init__(master)
        self.title(title)
        self.iconbitmap("./assets/img/logoRaycast.ico")
        self.geometry(dimension)
        self.grab_set()
        self.label = ctk.CTkLabel(self, text=message, text_color=colors[color]["color_text_input"]).pack(pady=20)
        self.button = ctk.CTkButton(self, text="Ok", border_width=2, text_color=colors[color]["color_text_input"], fg_color=colors[color]["fg_color"], hover_color=colors[color]["hover"], border_color=colors[color]["border_color"], command=self.destroyer).pack()
    def destroyer(self):
        self.destroy()

with open("./assets/json/env_var.json", "r") as env:
    config_env = json.load(env)
    try:
        if config_env["DECRYPT"] == "":
            lb_new_key(config_env)
    except:
        lb_new_key(config_env)
encrypt_key = config_env["DECRYPT"]
try:
    with open("./assets/json/command_info.json", "r") as data:
        try:
            key_words = json.loads(lb_decrypt(data.read(), encrypt_key).replace("'", '"'))
        except:
            key_words = config_env["DEFAULT_KEY"]
except:
    key_words = config_env["DEFAULT_KEY"]
co = cohere.Client(config_env["KEY_API"])

colors = [{"name": "Red", "fg_color": "#2E1A1A", "border_color": "#C91616", "color_text_input": "#ffffff", "hover": "#7C1818"}, {"name": "Orange", "fg_color": "#2E221A", "border_color": "#C95516", "color_text_input": "#ffffff", "hover": "#7C3C18"}, {"name": "Yellow", "fg_color": "#2E2B1A", "border_color": "#C9AF16", "color_text_input": "#ffffff", "hover": "#7C6D18"}, {"name": "Green", "fg_color": "#1B2E1A", "border_color": "#1FC916", "color_text_input": "#ffffff", "hover": "#1D7C18"}, {"name": "Cyan", "fg_color": "#1A2E2C", "border_color": "#16C9BB", "color_text_input": "#ffffff", "hover": "#187C74"}, {"name": "Blue", "fg_color": "#1C1A2E", "border_color": "#2516C9", "color_text_input": "#ffffff", "hover": "#21187C"}, {"name": "Purple", "fg_color": "#2A1A2E", "border_color": "#7316C9", "color_text_input": "#ffffff", "hover": "#4F187C"}, {"name": "Pink", "fg_color": "#2E1A29", "border_color": "#C916A3", "color_text_input": "#ffffff", "hover": "#7C1866"}, {"name": "Dark pink", "fg_color": "#2E1A1F", "border_color": "#C9164C", "color_text_input": "#ffffff", "hover": "#7C1836"}, {"name": "White", "fg_color": "#BEBEBE", "border_color": "#ffffff", "color_text_input": "#000000", "hover": "#DFDFDF"}, {"name": "Black", "fg_color": "#000000", "border_color": "#3C3C3C", "color_text_input": "#ffffff", "hover": "#1E1E1E"}]
possible_search = []
console_element_list = []
color_index = len(colors) - 1

root = App("Raycast", "800x340")
tabs = ctk.CTkTabview(root, width=700, height=300, text_color="#ffffff", segmented_button_fg_color="#000000", segmented_button_selected_color="#3C3C3C", segmented_button_selected_hover_color="#3C3C3C", segmented_button_unselected_color="#000000", segmented_button_unselected_hover_color="#1E1E1E")
tabs.add("Console")
tabs.add("Options")
tabs.pack()

to_do_request = ctk.StringVar()
name_new_action = ctk.StringVar()
icon_new_action = ctk.StringVar()
adress_new_action = ctk.StringVar()
query_new_action = ctk.StringVar()
path_new_action = ctk.StringVar()
num_delete_action = ctk.StringVar()

to_do = ctk.CTkEntry(tabs.tab("Console"), width=500, textvariable=to_do_request, placeholder_text="Enter a command", fg_color="#000000", border_color="#3C3C3C", text_color="white", font=("Monospace", 18))
to_do.pack(pady=6)
to_do.bind("<KeyRelease>", lambda key: lb_autocomplete(to_do_request.get(), key))
label_autocomplete = ctk.CTkLabel(tabs.tab("Console"), height=20, text="Enter a command", text_color="#5A5A5A", fg_color="#000000", font=("Monospace", 16))
label_autocomplete.place(x=130, y=8.5)
console_box = ctk.CTkScrollableFrame(tabs.tab("Console"), border_width=2, width=720, height=200, fg_color="#000000", border_color="#3C3C3C", scrollbar_button_color="#3C3C3C", scrollbar_button_hover_color="#3C3C3C")
console_box.pack(pady=6)

back_grounder = ctk.CTkScrollableFrame(tabs.tab('Options'), width=720, height=200, fg_color="#3C3C3C", scrollbar_button_color="#000000", scrollbar_button_hover_color="#1E1E1E")
label_add_action = ctk.CTkLabel(back_grounder, fg_color="#1E1E1E", text_color="#ffffff", corner_radius=10, text="------------Add a command------------", font=("Monospace", 18))
name_add_action = ctk.CTkEntry(back_grounder, fg_color="#000000", text_color="#ffffff", border_color="#3C3C3C", width=200, textvariable=name_new_action, placeholder_text="Command's name", font=("Monospace", 18))
name_label = ctk.CTkLabel(back_grounder, fg_color="#000000", text_color="#5A5A5A", width=10, height=10, text="Command's name", font=("Monospace", 15))
icon_add_action = ctk.CTkEntry(back_grounder, fg_color="#000000", text_color="#ffffff", border_color="#3C3C3C", width=200, textvariable=icon_new_action, placeholder_text="Icon's path", font=("Monospace", 18))
icon_label = ctk.CTkLabel(back_grounder, fg_color="#000000", text_color="#5A5A5A", width=10, height=10, text="Icon's path", font=("Monospace", 15))
combo_add_action = ctk.CTkComboBox(back_grounder, fg_color="#000000", text_color="#ffffff", border_color="#3C3C3C", button_color="#000000", dropdown_fg_color="#000000", dropdown_hover_color="#1E1E1E", dropdown_text_color="#ffffff", values=["Software", "Website"], state="readonly", font=("Monospace", 18), command=lambda value: lb_handle_type_action(value))
combo_add_action.set("Software")
color_add_action = ctk.CTkComboBox(back_grounder, fg_color="#000000", text_color="#ffffff", border_color="#3C3C3C", button_color="#000000", dropdown_fg_color="#000000", dropdown_hover_color="#1E1E1E", dropdown_text_color="#ffffff", values=["Red", "Orange", "Yellow", "Green", "Cyan", "Blue", "Purple", "Pink", "Dark pink", "White", "Black"], font=("Monospace", 18), state="readonly")
color_add_action.set("Red")
adress_add_action = ctk.CTkEntry(back_grounder, fg_color="#000000", text_color="#ffffff", border_color="#3C3C3C", width=200, textvariable=adress_new_action, placeholder_text="Adress", font=("Monospace", 18))
adress_label = ctk.CTkLabel(back_grounder, fg_color="#000000", text_color="#5A5A5A", width=10, height=10, text="Adress", font=("Monospace", 15))
query_add_action = ctk.CTkEntry(back_grounder, fg_color="#000000", text_color="#ffffff", border_color="#3C3C3C", width=200, textvariable=query_new_action, placeholder_text="Search query", font=("Monospace", 18))
query_label = ctk.CTkLabel(back_grounder, fg_color="#000000", text_color="#5A5A5A", width=10, height=10, text="Search query", font=("Monospace", 15))
path_add_action = ctk.CTkEntry(back_grounder, fg_color="#000000", text_color="#ffffff", border_color="#3C3C3C", width=200, textvariable=path_new_action, placeholder_text="Path's file", font=("Monospace", 18))
path_label = ctk.CTkLabel(back_grounder, fg_color="#000000", text_color="#5A5A5A", width=10, height=10, text="Path's file", font=("Monospace", 15))
button_add_action = ctk.CTkButton(back_grounder, border_width=2, fg_color="#000000", text_color="#ffffff", border_color="#3C3C3C", hover_color="#1E1E1E", text="Add", font=("Monospace", 18), cursor="hand2", command=lb_add_new_action)
name_add_action.bind("<KeyRelease>", lambda key: lb_show_placeholder(name_new_action, "Command's name", name_label, 269, 58))
icon_add_action.bind("<KeyRelease>", lambda key: lb_show_placeholder(icon_new_action, "Icon's path", icon_label, 269, 95))
adress_add_action.bind("<KeyRelease>", lambda key: lb_show_placeholder(adress_new_action, "Adress", adress_label, 269, 133))
query_add_action.bind("<KeyRelease>", lambda key: lb_show_placeholder(query_new_action, "Search query", query_label, 269, 171))
path_add_action.bind("<KeyRelease>", lambda key: lb_show_placeholder(path_new_action, "Path's file", path_label, 269, 133))
label_remove_action = ctk.CTkLabel(back_grounder, fg_color="#1E1E1E", text_color="#ffffff", corner_radius=10, text="------------Remove a command------------", font=("Monospace", 18))
num_remove_action = ctk.CTkEntry(back_grounder, textvariable=num_delete_action, fg_color="#000000", text_color="#ffffff", border_color="#3C3C3C", width=200, placeholder_text="Adress", font=("Monospace", 18))
num_label = ctk.CTkLabel(back_grounder, fg_color="#000000", text_color="#5A5A5A", width=10, height=10, text="Num", font=("Monospace", 15))
info_remove_action = ctk.CTkLabel(back_grounder, text=lb_refresh_command(), text_color="#ffffff", font=('Monospcae', 18))
button_remove_action = ctk.CTkButton(back_grounder, border_width=2, fg_color="#000000", text_color="#ffffff", border_color="#3C3C3C", hover_color="#1E1E1E", text="Remove", font=("Monospace", 18), cursor="hand2", command=lb_remove_action)
num_remove_action.bind("<KeyRelease>", lambda key: lb_show_placeholder(num_delete_action, "Num", num_label, 0, 0))
back_grounder.pack()
label_add_action.pack(pady=10)
name_add_action.pack(pady=5)
name_label.place(x=269, y=58)
icon_add_action.pack(pady=5)
icon_label.place(x=269, y=95)
adress_add_action.pack_forget()
adress_label.pack_forget()
query_add_action.pack_forget()
query_label.pack_forget()
path_add_action.pack(pady=5)
path_label.place(x=269, y=133)
combo_add_action.pack(pady=5)
color_add_action.pack(pady=5)
button_add_action.pack(pady=15)
label_remove_action.pack(pady=10)
num_remove_action.pack(pady=20)
num_label.place(x=269, y=369)
info_remove_action.pack()
button_remove_action.pack(pady=10)

threading.Thread(target=lb_listen_key, daemon=True).start()

root.mainloop()
