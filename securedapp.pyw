#! python3
# December 5, 2017

from tkinter import *
from stringy import *
from tkinter import ttk, font, messagebox, filedialog
from about_dialog import AboutDialog
from time import strftime
from glob import glob
import threading
import pathlib
import shelve
import shutil
import os


class SecuredApp(ttk.Notebook):

    def __init__(self, master, **kw):
        ttk.Notebook.__init__(self, master, **kw)
        self.grid(column=0, row=0, sticky='NEWS')
        self.root = master
        self.icon_path = os.getcwd() + '\\sa.png'
        # styles
        self.style = ttk.Style()
        self.heading = font.Font(family='Segoe Print', size=20, weight='bold')
        self.text = font.Font(family='Segoe Print', size=11, weight='bold')
        self.status_font = font.Font(family='Comic Sans MS',
                                     size=12, weight='normal')
        self.listbox_font = font.Font(family='Comic Sans MS', size=11)
        self.style.configure('TLabel', font=self.text,
                             padding=5, background='lightgray')
        self.style.configure('TButton', font=self.text,
                             padding=5, background='blue')
        self.style.configure('TFrame', background='lightgray')
        self.style.configure('TNotebook', background='gray')
        self.style.configure('Status.TLabel', font=self.status_font)
        # pages
        self.p1 = ttk.Frame(self, relief='groove', padding=8)
        self.p2 = ttk.Frame(self, relief='groove', padding=8)
        self.p3 = ttk.Frame(self, relief='groove', padding=8)
        self.p4 = ttk.Frame(self, relief='groove', padding=8)
        self.p5 = ttk.Frame(self, relief='groove', padding=8)
        self.p6 = ttk.Frame(self, relief='groove', padding=8)
        self.add(self.p1, text='Home', padding=2)
        # status bar
        self.status = StringVar()
        self.sample_file = None
        self.total_size = 0
        self.all_hidden = []
        # p1 objects
        self.USER_NAME = os.getlogin()
        self.HIDING_PATH = f"C:/Users/{self.USER_NAME}/AppData/Local/SecuredApp"
        self.files_to_be_hidden = None
        self.vid_ex = ['.mp4', '.mkv', '.avi', '.mpg', '.wmv', '.3gp', '.3g2']
        self.pic_ex = ['.jpg', '.png', '.gif']
        self.sound_ex = ['.mp3', '.wav', '.mp2', '.ogg', '.acc', '.m4a', '.ape']
        self.file_ex = ''
        self.total_files = StringVar()
        self.videos = StringVar()
        self.photos = StringVar()
        self.sounds = StringVar()
        self.others = StringVar()
        self.toggle_hide_button = ttk.Button(self.p1, text='Unhidden files',
                                             command=self.toggle_hide)
        # p2 objects
        self.video_head = ttk.Label(self.p2, font=self.heading)
        self.video_files = []
        self.videos_data = StringVar()
        self.videos_listbox = Listbox(self.p2, listvariable=self.videos_data,
                                      height=15, width=30,
                                      font=self.listbox_font)
        self.videos_scrollbar1 = ttk.Scrollbar(self.p2, orient=VERTICAL,
                                               command=self.videos_listbox.yview)
        self.videos_scrollbar2 = ttk.Scrollbar(self.p2, orient=HORIZONTAL,
                                               command=self.videos_listbox.xview)
        self.videos_listbox['yscrollcommand'] = self.videos_scrollbar1.set
        self.videos_listbox['xscrollcommand'] = self.videos_scrollbar2.set
        self.selected_video = StringVar()
        # p3 objects
        self.photo_head = ttk.Label(self.p3, font=self.heading)
        self.photo_files = []
        self.photos_data = StringVar()
        self.photos_listbox = Listbox(self.p3, listvariable=self.photos_data,
                                      height=15, width=30,
                                      font=self.listbox_font)
        self.photos_scrollbar1 = ttk.Scrollbar(self.p3, orient=VERTICAL,
                                               command=self.photos_listbox.yview)
        self.photos_scrollbar2 = ttk.Scrollbar(self.p3, orient=HORIZONTAL,
                                               command=self.photos_listbox.xview)
        self.photos_listbox['xscrollcommand'] = self.photos_scrollbar2.set
        self.photos_listbox['yscrollcommand'] = self.photos_scrollbar1.set
        self.selected_photo = StringVar()
        # p4 objects
        self.sound_head = ttk.Label(self.p4, font=self.heading)
        self.sound_files = []
        self.sounds_data = StringVar()
        self.sounds_listbox = Listbox(self.p4, listvariable=self.sounds_data,
                                      height=15, width=30,
                                      font=self.listbox_font)
        self.sounds_scrollbar1 = ttk.Scrollbar(self.p4, orient=VERTICAL,
                                               command=self.sounds_listbox.yview)
        self.sounds_scrollbar2 = ttk.Scrollbar(self.p4, orient=HORIZONTAL,
                                               command=self.sounds_listbox.xview)
        self.sounds_listbox['xscrollcommand'] = self.sounds_scrollbar2.set
        self.sounds_listbox['yscrollcommand'] = self.sounds_scrollbar1.set
        self.selected_sound = StringVar()
        # p5 objects
        self.other_head = ttk.Label(self.p5, font=self.heading)
        self.other_files = []
        self.others_data = StringVar()
        self.others_listbox = Listbox(self.p5, listvariable=self.others_data,
                                      height=15, width=30,
                                      font=self.listbox_font)
        self.others_scrollbar1 = ttk.Scrollbar(self.p5, orient=VERTICAL,
                                               command=self.others_listbox.yview)
        self.others_scrollbar2 = ttk.Scrollbar(self.p5, orient=HORIZONTAL,
                                               command=self.others_listbox.xview)
        self.others_listbox['xscrollcommand'] = self.others_scrollbar2.set
        self.others_listbox['yscrollcommand'] = self.others_scrollbar1.set
        self.selected_other = StringVar()
        # p6 objects
        self.old_password = StringVar()
        self.new_password = StringVar()
        self.retyped_new_password = StringVar()
        # geometry management
        for i in range(11):  # 10 rows
            self.rowconfigure(i, weight=1)
            self.p1.rowconfigure(i, weight=1)
            if i != 10:
                self.p2.rowconfigure(i, weight=1)
                self.p3.rowconfigure(i, weight=1)
                self.p4.rowconfigure(i, weight=1)
                self.p5.rowconfigure(i, weight=1)
            self.p6.rowconfigure(i, weight=1)
        for i in range(4):  # 3 columns
            self.columnconfigure(i, weight=1)
            self.p1.columnconfigure(i, weight=1)
            if i not in [1, 2]:
                self.p2.columnconfigure(i, weight=1)
                self.p3.columnconfigure(i, weight=1)
                self.p4.columnconfigure(i, weight=1)
                self.p5.columnconfigure(i, weight=1)
            self.p6.columnconfigure(i, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        # Checking if hiding path exists
        self.LAST_LOGIN = None
        if os.path.exists(self.HIDING_PATH):
            dirs = os.listdir(self.HIDING_PATH)
            for i in ["OTHERS", "VIDEOS", "SOUNDS", "PHOTOS"]:
                if i not in dirs:
                    os.mkdir(f'{self.HIDING_PATH}/{i}')
            self.login_password = StringVar()
            self.login_retries = 0
            with shelve.open(f'{self.HIDING_PATH}/password') as p:
                self.PASSWORD = decrypt(p['password'])
                self.LAST_LOGIN = p['last_login']
                p['last_login'] = strftime('%B %d, %Y - %I:%M %p')
            self.log = [
                ttk.Label(self.p1, text=f'Welcome {self.USER_NAME}!',
                          font=self.heading),
                ttk.Label(self.p1, text="Let's log you in!"),
                ttk.Separator(self.p1, orient=HORIZONTAL),
                ttk.Label(self.p1, text='Type your password here.'),
                ttk.Entry(self.p1, show='*', font=self.text,
                          textvariable=self.login_password),
                ttk.Button(self.p1, text='Login', command=self.login)
            ]
            self.login_widgets()
        else:
            self.initial_pass = StringVar()
            self.final_pass = StringVar()
            self.first = [ttk.Label(self.p1, text=f'Welcome {self.USER_NAME}!',
                                    font=self.heading),
                          ttk.Label(self.p1, text="Let's set you up!"),
                          ttk.Separator(self.p1, orient=HORIZONTAL),
                          ttk.Label(self.p1, text='Type your Password'),
                          ttk.Entry(self.p1, show='*', font=self.text,
                                    textvariable=self.initial_pass),
                          ttk.Label(self.p1, text='Retype your Password'),
                          ttk.Entry(self.p1, show='*', font=self.text,
                                    textvariable=self.final_pass),
                          ttk.Separator(self.p1, orient=HORIZONTAL),
                          ttk.Button(self.p1, text='Process',
                                     command=self.process_first)]
            self.first_time_widgets()

    def process_first(self):
        if self.initial_pass.get() != '' and self.final_pass.get() != '':
            if self.initial_pass.get() == self.final_pass.get():
                os.mkdir(self.HIDING_PATH)
                os.mkdir(f'{self.HIDING_PATH}/VIDEOS')
                os.mkdir(f'{self.HIDING_PATH}/PHOTOS')
                os.mkdir(f'{self.HIDING_PATH}/SOUNDS')
                os.mkdir(f'{self.HIDING_PATH}/OTHERS')
                with shelve.open(f'{self.HIDING_PATH}/password') as p:
                    p['password'] = encrypt(self.final_pass.get())
                    p['last_login'] = strftime('%B %d, %Y - %I:%M %p')
                os.chdir(f'{self.HIDING_PATH}/')
                os.system(f'attrib +s +h')
                for i in self.first:
                    i.destroy()
                self.widgets()
            else:
                messagebox.showinfo('Info', 'Password did not match.')
                self.final_pass.set('')
        else:
            messagebox.showinfo('Info', 'Please fill in the fields properly.')

    def login(self, *args):
        if self.login_password.get() != '':
            if self.login_password.get() == self.PASSWORD:
                for i in self.log:
                    i.destroy()
                self.widgets()
                with shelve.open(f'{self.HIDING_PATH}/password') as p:
                    p['last_login'] = strftime('%B %d, %Y - %I:%M %p')
            else:
                self.login_retries += 1
                messagebox.showinfo('Info', 'Password was incorrect.')
                self.login_password.set('')
                if self.login_retries >= 5:
                    messagebox.showinfo(
                        'Info', 'You have reached the maximum number of'
                                ' retries, the program will now terminate.')
                    self.root.destroy()
        return args

    def login_widgets(self):
        self.log[0].grid(column=0, row=0, columnspan=4)
        self.log[1].grid(column=0, row=1, columnspan=4)
        self.log[2].grid(column=0, row=2, columnspan=4, sticky='WE', pady='12 5')
        self.log[3].grid(column=0, row=3, columnspan=4)
        self.log[4].grid(column=0, row=4, columnspan=4, sticky='NEWS', padx=30)
        self.log[5].grid(column=0, row=5, columnspan=4, sticky='NEWS', padx=30,
                         pady='2 0')
        self.log[4].focus()
        self.root.bind('<Return>', self.login)
        self.update_app()

    def first_time_widgets(self):
        self.first[0].grid(column=0, row=0, columnspan=4)
        self.first[1].grid(column=0, row=1, columnspan=4, sticky=N)
        self.first[2].grid(column=0, row=2, columnspan=4, pady='0 12',
                           sticky='WE')
        self.first[3].grid(column=0, row=3, columnspan=4)
        self.first[4].grid(column=0, row=4, columnspan=4, sticky='NEWS', padx=30)
        self.first[5].grid(column=0, row=5, columnspan=4)
        self.first[6].grid(column=0, row=6, columnspan=4, sticky='NEWS', padx=30)
        self.first[7].grid(column=0, row=7, columnspan=4, pady='12 5',
                           sticky='WE')
        self.first[8].grid(column=0, row=8, columnspan=4, sticky='NEWS')

    def hide_secure_thread(self):
        self.files_to_be_hidden = filedialog.askopenfiles()
        for i in self.files_to_be_hidden:
            try:
                self.file_ex = pathlib.Path(i.name).suffix
                i.close()
                os.system(f'attrib +h +s "{i.name}"')
                if self.file_ex.lower() in self.vid_ex:
                    shutil.move(i.name, f'{self.HIDING_PATH}/VIDEOS/')
                elif self.file_ex.lower() in self.pic_ex:
                    shutil.move(i.name, f'{self.HIDING_PATH}/PHOTOS/')
                elif self.file_ex.lower() in self.sound_ex:
                    shutil.move(i.name, f'{self.HIDING_PATH}/SOUNDS/')
                elif self.file_ex.lower() in self.vid_ex:
                    shutil.move(i.name, f'{self.HIDING_PATH}/VIDEOS/')
                else:
                    shutil.move(i.name, f'{self.HIDING_PATH}/OTHERS/')
            except shutil.Error:
                messagebox.showerror('Info', f'{i.name} already exists.')
            self.update_texts()
            self.calculate_size()
        self.update_app()

    def hide_secure(self):
        threading.Thread(target=self.hide_secure_thread).start()

    def toggle_hide(self):
        if self.toggle_hide_button['text'] == 'Unhidden files':
            self.open_hiding_path()
            self.toggle_hide_button['text'] = 'Hide files again'
        else:
            self.hide_again()
            self.toggle_hide_button['text'] = 'Unhidden files'
        self.update_app()

    def open_hiding_path(self):
        os.system(f'start {self.HIDING_PATH}')
        for path in ['VIDEOS', 'PHOTOS', 'SOUNDS', 'OTHERS']:
            os.chdir(f'{self.HIDING_PATH}/{path}/')
            os.system('attrib -s -h')

    def hide_again(self):
        for path in ['VIDEOS', 'PHOTOS', 'SOUNDS', 'OTHERS']:
            os.chdir(f'{self.HIDING_PATH}/{path}/')
            os.system('attrib +s +h')
        os.chdir(f'{self.HIDING_PATH}/')
        os.system(f'attrib +s +h')

    def update_texts(self):
        os.chdir(f'{self.HIDING_PATH}/VIDEOS/')
        self.video_files = sorted(glob('*.*'))
        os.chdir(f'{self.HIDING_PATH}/PHOTOS/')
        self.photo_files = sorted(glob('*.*'))
        os.chdir(f'{self.HIDING_PATH}/SOUNDS/')
        self.sound_files = sorted(glob('*.*'))
        os.chdir(f'{self.HIDING_PATH}/OTHERS/')
        self.other_files = sorted(glob('*.*'))
        self.videos_data.set(self.video_files)
        self.photos_data.set(self.photo_files)
        self.sounds_data.set(self.sound_files)
        self.others_data.set(self.other_files)
        self.videos.set(len(self.video_files))
        self.photos.set(len(self.photo_files))
        self.sounds.set(len(self.sound_files))
        self.others.set(len(self.other_files))
        self.total_files.set(int(self.videos.get()) + int(self.photos.get()) +
                             int(self.sounds.get()) + int(self.others.get()))
        self.video_head['text'] = f'Videos ({self.videos.get()})'
        self.photo_head['text'] = f'Photos ({self.photos.get()})'
        self.sound_head['text'] = f'Sounds ({self.sounds.get()})'
        self.other_head['text'] = f'Others ({self.others.get()})'

    def update_list_boxes(self):
        for listbox in [(self.videos_listbox, len(self.video_files)),
                        (self.photos_listbox, len(self.photo_files)),
                        (self.sounds_listbox, len(self.sound_files)),
                        (self.others_listbox, len(self.other_files))]:
            for i in range(0, listbox[1], 2):
                listbox[0].itemconfigure(i, background='#f0f0ff')

    def check_if_files_are_hidden(self):
        self.all_hidden = []
        for tpl in [(self.video_files, 'VIDEOS'), (self.photo_files, 'PHOTOS'),
                    (self.sound_files, 'SOUNDS'), (self.other_files, 'OTHERS')]:
            if len(tpl[0]) != 0:
                self.sample_file = os.stat(
                    f'{self.HIDING_PATH}/{tpl[1]}/{tpl[0][0]}')
                if self.sample_file.st_file_attributes == 38:
                    self.all_hidden.append(True)
                else:
                    self.all_hidden.append(False)
        if len(self.all_hidden) != 0 and all(self.all_hidden):
            self.style.configure('Status.TLabel', foreground='green')
            self.status.set(f'{self.status.get()} Files are hidden.')
            self.toggle_hide_button['text'] = 'Unhidden files'
            self.toggle_hide_button.state(['!disabled'])
        elif len(self.all_hidden) != 0 and not all(self.all_hidden):
            self.style.configure('Status.TLabel', foreground='red')
            self.status.set(f"{self.status.get()} Files are unhidden!")
            self.toggle_hide_button['text'] = 'Hide files again'
            self.toggle_hide_button.state(['!disabled'])
        if len(self.all_hidden) == 0:
            self.style.configure('Status.TLabel', foreground='black')
            self.status.set(f'{self.status.get()} - You are securing nothing.')
            self.toggle_hide_button['text'] = 'Unhidden files'
            self.toggle_hide_button.state(['disabled'])
        self.status.set(f"{self.status.get()} Last login was {self.LAST_LOGIN}.")

    def calculate_size(self):
        self.total_size = 0
        for path in ['VIDEOS', 'PHOTOS', 'SOUNDS', 'OTHERS']:
            for i in glob(f'{self.HIDING_PATH}/{path}/*.*'):
                self.total_size += os.path.getsize(i)
        if self.total_size < 1024:
            self.status.set(f'{round(self.total_size, 2)} B')
        elif self.total_size < 1048576:
            self.status.set(
                f'{round(self.total_size * 0.000977, 2)} KB')
        elif self.total_size < 1073741824:
            self.status.set(
                f'{round(self.total_size * 0.00000095367432, 2)} MB')
        else:
            self.status.set(
                f'{round(self.total_size * 0.00000000093132, 2)} GB')

    def update_app(self, *args):
        self.update_texts()
        self.calculate_size()
        self.check_if_files_are_hidden()
        self.update_list_boxes()
        return args

    @staticmethod
    def show(listbox, selected, files):
        if len(listbox.curselection()) == 1:
            selected.set(files[int(listbox.curselection()[0])])

    def show_video(self, *args):
        self.show(self.videos_listbox, self.selected_video, self.video_files)
        return args

    def show_photo(self, *args):
        self.show(self.photos_listbox, self.selected_photo, self.photo_files)
        return args

    def show_sound(self, *args):
        self.show(self.sounds_listbox, self.selected_sound, self.sound_files)
        return args

    def show_other(self, *args):
        self.show(self.others_listbox, self.selected_other, self.other_files)
        return args

    def open(self, where, what):
        if what.get():
            os.system(f'start {self.HIDING_PATH}/{where}'
                      f'/"{what.get()}"')
        else:
            messagebox.showinfo('Info', 'Nothing is selected.')

    def open_video(self, *args):
        self.open('VIDEOS', self.selected_video)
        return args

    def open_photo(self, *args):
        self.open('PHOTOS', self.selected_photo)
        return args

    def open_sound(self, *args):
        self.open('SOUNDS', self.selected_sound)
        return args

    def open_other(self, *args):
        self.open('OTHERS', self.selected_other)
        return args

    def delete(self, selected, path):
        if selected.get():
            if messagebox.askokcancel('Info',
                                      f'Delete {selected.get()}'):
                os.remove(f'{self.HIDING_PATH}/{path}'
                          f'/{selected.get()}')
                selected.set('')
                self.update_app()
        else:
            messagebox.showinfo('Info', 'Nothing to delete.')

    def delete_video(self, *args):
        self.delete(self.selected_video, 'VIDEOS')
        return args

    def delete_photo(self, *args):
        self.delete(self.selected_photo, 'PHOTOS')
        return args

    def delete_sound(self, *args):
        self.delete(self.selected_sound, 'SOUNDS')
        return args

    def delete_other(self, *args):
        self.delete(self.selected_other, 'OTHERS')
        return args

    def delete_all(self, selected, what, where):
        if messagebox.askokcancel('Info', f'Delete all {where}?'):
            for item in what:
                os.remove(f'{self.HIDING_PATH}/{where}/{item}')
            selected.set('')
            self.update_app()

    def delete_videos(self):
        self.delete_all(self.selected_video, self.video_files, 'VIDEOS')

    def delete_photos(self):
        self.delete_all(self.selected_photo, self.photo_files, 'PHOTOS')

    def delete_sounds(self):
        self.delete_all(self.selected_sound, self.sound_files, 'SOUNDS')

    def delete_others(self):
        self.delete_all(self.selected_other, self.other_files, 'OTHERS')

    def change_password(self):
        if '' not in [self.old_password.get(), self.new_password.get(),
                      self.retyped_new_password.get()]:
            if self.old_password.get() == self.PASSWORD:
                if self.new_password.get() == self.retyped_new_password.get():
                    os.chdir(f"{self.HIDING_PATH}")
                    os.system(f'attrib -s -h')
                    with open(f'{self.HIDING_PATH}/password.txt', 'w') as p:
                        p.write(encrypt(self.new_password.get()))
                    os.system(f'attrib +s +h')
                    messagebox.showinfo('Info', 'Password has been '
                                                'changed successfully. App '
                                                'will terminate to apply '
                                                'some change.')
                    self.root.destroy()
                else:
                    messagebox.showinfo('Info', 'New password did not match.')
            else:
                messagebox.showinfo('Info', 'Old password is incorrect.')

    def show_about_dialog(self, *args):
        AboutDialog(self, window_title='About SecuredApp',
                    about_title='SecuredApp',
                    content='Developed and written by:\n'
                            '\tDenniel Luis Saway Sadian '
                            '(https://denniel-sadian.github.io)\n\n'
                            'Date of creation:\n'
                            '\tDecember 5, 2017\n\n'
                            'Description:\n'
                            '\tThis application is written to protect your '
                            'precious data, any kinds of files. It is written '
                            'completely in Python Programming Language. It uses '
                            'Tkinter as the GUI framework.',
                    image=self.icon_path).mainloop()
        return args

    def widgets(self):
        # p1
        ttk.Label(self.p1, text='Secured App', font=self.heading).grid(
            column=0, row=0, columnspan=4)
        ttk.Label(self.p1, text=f"Welcome {self.USER_NAME}! Let's hide and "
                                "secure.").grid(
            column=0, row=1, columnspan=4, sticky=N)
        ttk.Separator(self.p1, orient=HORIZONTAL).grid(
            column=0, row=2, columnspan=4, pady='0 12', sticky='WE')
        ttk.Label(self.p1, text='Videos:').grid(column=0, row=3, sticky=E)
        ttk.Label(self.p1, textvariable=self.videos).grid(column=1, row=3,
                                                          columnspan=3)
        ttk.Label(self.p1, text='Photos:').grid(column=0, row=4, sticky=E)
        ttk.Label(self.p1, textvariable=self.photos).grid(column=1, row=4,
                                                          columnspan=3)
        ttk.Label(self.p1, text='Sounds:').grid(column=0, row=5, sticky=E)
        ttk.Label(self.p1, textvariable=self.sounds).grid(column=1, row=5,
                                                          columnspan=3)
        ttk.Label(self.p1, text='Others:').grid(column=0, row=6, sticky=E)
        ttk.Label(self.p1, textvariable=self.others).grid(column=1, row=6,
                                                          columnspan=3)
        ttk.Label(self.p1, text='Total:').grid(column=0, row=7, sticky=E)
        ttk.Label(self.p1, textvariable=self.total_files).grid(column=1, row=7,
                                                               columnspan=3)
        ttk.Separator(self.p1, orient=HORIZONTAL).grid(
            column=0, row=8, columnspan=4, pady='12 6', sticky='WE')
        ttk.Button(self.p1, text='Hide and secure',
                   command=self.hide_secure).grid(
            column=0, row=9, columnspan=4, sticky='NEWS')
        self.toggle_hide_button.grid(
            column=0, row=10, columnspan=4, sticky='NEWS', pady='2 0')
        # p2
        self.video_head.grid(column=0, row=0, columnspan=4)
        ttk.Label(self.p2, text='All of your hidden videos are here.').grid(
            column=0, row=1, columnspan=4, sticky=N)
        ttk.Separator(self.p2, orient=HORIZONTAL).grid(
            column=0, row=2, columnspan=4, pady='0 12', sticky='WE')
        self.videos_listbox.grid(column=0, row=3, rowspan=7, sticky='NEWS')
        self.videos_scrollbar1.grid(column=1, row=3, rowspan=7, sticky='NWS')
        self.videos_scrollbar2.grid(column=0, row=10, sticky='WNE')
        ttk.Separator(self.p2, orient=VERTICAL).grid(
            column=2, row=3, rowspan=8, padx='10 8', sticky='WNS')
        ttk.Label(self.p2, text='Selected:').grid(column=3, row=3, sticky=W)
        ttk.Label(self.p2, textvariable=self.selected_video).grid(
            column=3, row=4)
        ttk.Separator(self.p2, orient=HORIZONTAL).grid(
            column=3, row=5, pady='0 12', sticky='WE')
        ttk.Button(self.p2, text='Watch', command=self.open_video).grid(
            column=3, row=6, sticky='WE')
        ttk.Button(self.p2, text='Delete', command=self.delete_video).grid(
            column=3, row=7, sticky='WE')
        ttk.Separator(self.p2, orient=HORIZONTAL).grid(
            column=3, row=8, pady='20 20', sticky='WE')
        ttk.Button(self.p2, text='Delete all', command=self.delete_videos).grid(
            column=3, row=9, sticky='NEWS')
        # p3
        self.photo_head.grid(column=0, row=0, columnspan=4)
        ttk.Label(self.p3, text='All of your hidden photos are here.').grid(
            column=0, row=1, columnspan=4, sticky=N)
        ttk.Separator(self.p3, orient=HORIZONTAL).grid(
            column=0, row=2, columnspan=4, pady='0 12', sticky='WE')
        self.photos_listbox.grid(column=0, row=3, rowspan=7, sticky='NEWS')
        self.photos_scrollbar1.grid(column=1, row=3, rowspan=7, sticky='NWS')
        self.photos_scrollbar2.grid(column=0, row=10, sticky='WNE')
        ttk.Separator(self.p3, orient=VERTICAL).grid(
            column=2, row=3, rowspan=8, padx='10 8', sticky='WNS')
        ttk.Label(self.p3, text='Selected:').grid(column=3, row=3, sticky=W)
        ttk.Label(self.p3, textvariable=self.selected_photo).grid(
            column=3, row=4)
        ttk.Separator(self.p3, orient=HORIZONTAL).grid(
            column=3, row=5, pady='0 12', sticky='WE')
        ttk.Button(self.p3, text='See', command=self.open_photo).grid(
            column=3, row=6, sticky='WE')
        ttk.Button(self.p3, text='Delete', command=self.delete_photo).grid(
            column=3, row=7, sticky='WE')
        ttk.Separator(self.p3, orient=HORIZONTAL).grid(
            column=3, row=8, pady='20 20', sticky='WE')
        ttk.Button(self.p3, text='Delete all', command=self.delete_photos).grid(
            column=3, row=9, sticky='NEWS')
        # p4
        self.sound_head.grid(column=0, row=0, columnspan=4)
        ttk.Label(self.p4, text='All of your hidden sound files are here.').grid(
            column=0, row=1, columnspan=4, sticky=N)
        ttk.Separator(self.p4, orient=HORIZONTAL).grid(
            column=0, row=2, columnspan=4, pady='0 12', sticky='WE')
        self.sounds_listbox.grid(column=0, row=3, rowspan=7, sticky='NEWS')
        self.sounds_scrollbar1.grid(column=1, row=3, rowspan=7, sticky='NWS')
        self.sounds_scrollbar2.grid(column=0, row=10, sticky='WNE')
        ttk.Separator(self.p4, orient=VERTICAL).grid(
            column=2, row=3, rowspan=8, padx='10 8', sticky='WNS')
        ttk.Label(self.p4, text='Selected:').grid(column=3, row=3, sticky=W)
        ttk.Label(self.p4, textvariable=self.selected_sound).grid(
            column=3, row=4)
        ttk.Separator(self.p4, orient=HORIZONTAL).grid(
            column=3, row=5, pady='0 12', sticky='WE')
        ttk.Button(self.p4, text='Listen', command=self.open_sound).grid(
            column=3, row=6, sticky='WE')
        ttk.Button(self.p4, text='Delete', command=self.delete_sound).grid(
            column=3, row=7, sticky='WE')
        ttk.Separator(self.p4, orient=HORIZONTAL).grid(
            column=3, row=8, pady='20 20', sticky='WE')
        ttk.Button(self.p4, text='Delete all', command=self.delete_sounds).grid(
            column=3, row=9, sticky='NEWS')
        # p5
        self.other_head.grid(column=0, row=0, columnspan=4)
        ttk.Label(self.p5, text='All of your other hidden files are here.').grid(
            column=0, row=1, columnspan=4, sticky=N)
        ttk.Separator(self.p5, orient=HORIZONTAL).grid(
            column=0, row=2, columnspan=4, pady='0 12', sticky='WE')
        self.others_listbox.grid(column=0, row=3, rowspan=7, sticky='NEWS')
        self.others_scrollbar1.grid(column=1, row=3, rowspan=7, sticky='NWS')
        self.others_scrollbar2.grid(column=0, row=10, sticky='WNE')
        ttk.Separator(self.p5, orient=VERTICAL).grid(
            column=2, row=3, rowspan=8, padx='10 8', sticky='WNS')
        ttk.Label(self.p5, text='Selected:').grid(column=3, row=3, sticky=W)
        ttk.Label(self.p5, textvariable=self.selected_other).grid(
            column=3, row=4)
        ttk.Separator(self.p5, orient=HORIZONTAL).grid(
            column=3, row=5, pady='0 12', sticky='WE')
        ttk.Button(self.p5, text='Open', command=self.open_other).grid(
            column=3, row=6, sticky='WE')
        ttk.Button(self.p5, text='Delete', command=self.delete_other).grid(
            column=3, row=7, sticky='WE')
        ttk.Separator(self.p5, orient=HORIZONTAL).grid(
            column=3, row=8, pady='20 20', sticky='WE')
        ttk.Button(self.p5, text='Delete all', command=self.delete_others).grid(
            column=3, row=9, sticky='NEWS')
        # p6
        ttk.Label(self.p6, text='Password Management', font=self.heading).grid(
            column=0, row=0, columnspan=4)
        ttk.Label(self.p6, text='You can change your password here.').grid(
            column=0, row=1, columnspan=4, sticky=N)
        ttk.Separator(self.p6, orient=HORIZONTAL).grid(
            column=0, row=2, columnspan=4, pady='0 12', sticky='WE')
        ttk.Label(self.p6, text='Old password').grid(column=0, row=3)
        ttk.Entry(self.p6, textvariable=self.old_password, font=self.text,
                  show='*').grid(column=1, row=3, sticky='WE', columnspan=3)
        ttk.Label(self.p6, text='New password').grid(column=0, row=4)
        ttk.Entry(self.p6, textvariable=self.new_password, font=self.text,
                  show='*').grid(column=1, row=4, sticky='WE', columnspan=3)
        ttk.Label(self.p6, text='Retype new password').grid(column=0, row=5)
        ttk.Entry(self.p6, textvariable=self.retyped_new_password,
                  font=self.text, show='*').grid(column=1, row=5, sticky='WE',
                                                 columnspan=3)
        ttk.Separator(self.p6, orient=HORIZONTAL).grid(
            column=0, row=6, columnspan=4, pady='0 12', sticky='WE')
        ttk.Button(self.p6, text='Change password',
                   command=self.change_password).grid(
            column=0, row=7, sticky='NEWS', columnspan=4)
        ttk.Label(self.root, textvariable=self.status, relief='sunken',
                  background='white', padding='5 0', style='Status.TLabel').grid(
            column=0, row=1, sticky='NEWS')
        self.add(self.p2, text='Videos', padding=2)
        self.add(self.p3, text='Photos', padding=2)
        self.add(self.p4, text='Sounds', padding=2)
        self.add(self.p5, text='Others', padding=2)
        self.add(self.p6, text='Password', padding=2)
        # events
        self.root.unbind('<Return>')
        self.root.bind('<Enter>', self.update_app)
        self.root.bind('<F1>', self.show_about_dialog)
        # <<ListboxSelect>> bindings
        for listbox, fun in [(self.videos_listbox, self.show_video),
                             (self.photos_listbox, self.show_photo),
                             (self.sounds_listbox, self.show_sound),
                             (self.others_listbox, self.show_other)]:
            listbox.bind('<<ListboxSelect>>', fun)
        # <Double-1> and <Return> bindings
        for listbox, fun in [(self.videos_listbox, self.open_video),
                             (self.photos_listbox, self.open_photo),
                             (self.sounds_listbox, self.open_sound),
                             (self.others_listbox, self.open_other)]:
            listbox.bind('<Double-1>', fun)
            listbox.bind('<Return>', fun)
        # <Delete> bindings
        for listbox, fun in [(self.videos_listbox, self.delete_video),
                             (self.photos_listbox, self.delete_photo),
                             (self.sounds_listbox, self.delete_sound),
                             (self.others_listbox, self.delete_other)]:
            listbox.bind('<Delete>', fun)
        self.update_app()


if __name__ == '__main__':
    root = Tk()
    app = SecuredApp(root, padding='3 5 3 3')
    root.title('Secured App')
    root.mainloop()
