from tkinter import *
import tkinter as tk
from tkinter import filedialog as fd
# from tkinter.ttk import Frame, Button, Style
from tkinter import messagebox
from db_connect import On_bd
from pathlib import Path
from PIL import Image, ImageTk
import datetime
import PIL
import os
import psycopg2

all_tests_list = {1:"Опросник школьной тревожности Филлипса",
                  2:"Оценка уровня школьной мотивации",
                  3:"ТЕСТ «ДЕРЕВО»",
                  4:"Методика для диагностики школьной тревожности",
                  5:"Творческий потенциал ребенка"}



class MainApp(Tk):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        self.width = 680
        self.height = 620
        img = PhotoImage(file="main.png")
        self.iconphoto(False, img)
        self.des = []
        self.name_user = None
        self.date_user = None
        self.test_name = None
        self.configure(bg="#5FD2B5")
        self.title("Психологические тесты")  # устанавливаем заголовок main
        self.minsize(width=self.width, height=self.height)  # устанавливаем ширину и высоту
        self.up_menu()
        self.main_window()
        self.cursor = On_bd().cursor

    def main_window(self):
        self.destroyed()
        # img = ImageTk.PhotoImage(self.resize_image(300, Path("main.png")))
        # label_main = Label(self,
        #               image=img,
        #               bg="#5FD2B5")
        # label_main.image = img

        frame = Frame(self,
                      bg="#5FD2B5")

        label1 = Label(frame,
                       text="Добрый день! Для продолжения работы\n выберите нужный раздел",
                       font="Times 16",
                       bg="#5FD2B5")

        button_go_test = Button(frame,
                                text="Пройти тест",
                                width=40,
                                font="Times 14",
                                height=2,
                                command=self.check_user)

        button_history = Button(frame,
                                text="Открыть историю",
                                width=40,
                                font="Times 14",
                                height=2,
                                command=self.all_histori)

        button_list_test = Button(frame,
                                  text="Список тестов",
                                  width=40,
                                  font="Times 14",
                                  height=2,
                                  command=self.list_test_info)

        # self.add_destroyed(label_main)
        self.add_destroyed(label1)
        self.add_destroyed(button_go_test)
        self.add_destroyed(button_history)
        self.add_destroyed(button_list_test)
        self.add_destroyed(frame)



        frame.pack()
        label1.grid(row=0, column=2, pady=20)
        button_go_test.grid(row=1, column=2, pady=10)
        button_history.grid(row=2, column=2, pady=10)
        button_list_test.grid(row=3, column=2, pady=10)

        # label_main.place(x=20, y=80)

    def up_menu(self):
        # Иницилизация верхнего меню
        mainmenu = Menu(self)
        # второй уровень меню Файлы
        filemenu = Menu(mainmenu, tearoff=0)
        filemenu.add_command(label="Открыть историю", command=self.all_histori)
        filemenu.add_command(label="Пройти тест", command=self.check_user)
        filemenu.add_command(label="Список тестов", command=self.list_test_info)
        filemenu.add_separator()
        filemenu.add_command(label="Выход")

        # Второй уровень меню Справка
        helpmenu = Menu(mainmenu, tearoff=0)
        helpmenu.add_command(label="Помощь")
        helpmenu.add_command(label="О программе", command=self.new_window)

        # Главное меню, добавление пунктов Файлы и Справка
        mainmenu.add_cascade(label="Главная", command=self.main_window)
        mainmenu.add_cascade(label="Тесты",
                             menu=filemenu)
        mainmenu.add_cascade(label="Справка",
                             menu=helpmenu)

        self.config(menu=mainmenu)

    def list_test_info(self):
        self.destroyed()

        scrollbar = Scrollbar(self)

        def callback():
            for i in reversed(lbox.curselection()):
                os.startfile(Path("files", str(lbox.get(i))))

        lbox = Listbox(self,
                       width=80,
                       height=28,
                       selectmode=SINGLE,
                       yscrollcommand=scrollbar.set)

        button_seal = Button(self,
                                text="Открыть",
                                width=12,
                                height=2,
                                command=callback)
        dest = []
        def on_event_button_seal(event):
            label = Label(self,
                          text="Открывает файл для ознакомления",
                          font="Times 11",
                          bg="#5FD2B5")
            label.place(x=220, y=570)
            dest.append(label)

        def off_event_button_seal(event):
            for obj in dest:
                obj.destroy()

        button_seal.bind("<Enter>", on_event_button_seal)
        button_seal.bind("<Leave>", off_event_button_seal)

        dirname = "files"
        files = os.listdir(dirname)

        for row in files:
            lbox.insert(0, row)

        self.add_destroyed(lbox)
        self.add_destroyed(scrollbar)
        self.add_destroyed(button_seal)
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.config(command=lbox.yview)

        lbox.place(x=100, y=60)
        button_seal.place(x=300, y=524)

    def all_histori(self):
        self.destroyed()  # уничтожаем элементы, которые были до этого

        def callback():
            try:
                for i in reversed(lbox.curselection()):
                    self.cursor.execute(f"""DELETE FROM save_result WHERE id = {lbox.get(i)[0]};""")
                    lbox.delete(i)
            except:
                pass

        def callback_all():
            try:
                self.cursor.execute("""TRUNCATE save_result;""")
                lbox.delete(0, END)
            except:
                pass

        def callback_result():
            for i in reversed(lbox.curselection()):
                self.cursor.execute(f"""SELECT info_result FROM save_result WHERE id = {lbox.get(i)[0]};""")

            for row in self.cursor:
                Info_result(row[0]).mainloop()

        scrollbar = Scrollbar(self)

        label_info = Label(self,
                       text="База данных истории прохождения тестов",
                       font="16",
                       height=2,
                       bg="#5FD2B5")

        lbox = Listbox(self,
                       width=80,
                       height=28,
                       selectmode=SINGLE,
                       yscrollcommand=scrollbar.set)

        button_main = Button(self,
                                text="Главная",
                                width=12,
                                height=2,
                                command=self.main_window)

        button_one_del = Button(self,
                                text="Удалить",
                                width=12,
                                height=2,
                                command=callback)
        dest = []
        def on_event_button_one_del(event):
            label = Label(self,
                          text="Удаляет выделенный объект",
                          font="Times 11",
                          bg="#5FD2B5")
            label.place(x=340, y=570)
            dest.append(label)

        def off_event_button_one_del(event):
            for obj in dest:
                obj.destroy()

        button_one_del.bind("<Enter>", on_event_button_one_del)
        button_one_del.bind("<Leave>", off_event_button_one_del)


        button_clear = Button(self,
                              text="Очистить",
                              width=12,
                              height=2,
                              command=callback_all)

        button_result = Button(self,
                              text="Результат",
                              width=12,
                              height=2,
                              command=callback_result)

        def on_button_clear(event):
            label = Label(self,
                          text="Очищает всю базу данных",
                          font="Times 11",
                          bg="#5FD2B5")
            label.place(x=450, y=570)
            dest.append(label)

        def off_button_clear(event):
            for obj in dest:
                obj.destroy()

        button_clear.bind("<Enter>", on_button_clear)
        button_clear.bind("<Leave>", off_button_clear)

        try:
            self.cursor.execute("""SELECT id, name, name_test, date  FROM save_result""")
            for row in self.cursor:
                lbox.insert(0, row)
        except:
            pass

        self.add_destroyed(label_info)
        self.add_destroyed(lbox)
        self.add_destroyed(scrollbar)
        self.add_destroyed(button_one_del)
        self.add_destroyed(button_clear)
        self.add_destroyed(button_main)
        self.add_destroyed(button_result)


        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.config(command=lbox.yview)
        label_info.place(x=140, y=2)
        button_main.place(x=100, y=524)
        button_result.place(x=240, y=524)
        button_one_del.place(x=360, y=524)
        button_clear.place(x=490, y=524)
        lbox.place(x=100, y=60)

    def new_window(self):
        Window().mainloop()

    def check_user(self):
        self.destroyed()

        frame_first = Frame(self,
                            bg="#5FD2B5",
                            height=250)
        frame_between_buttons = Frame(self,
                                      height=12,
                                      bg="#5FD2B5")

        if self.date_user != None and self.name_user != None:
            button1 = Button(self,
                            text="Продолжить",
                            width=20,
                            height=1,
                            font="12",
                            command=self.list_test
                            )
            button2 = Button(self,
                            text="Новый пользователь",
                            width=20,
                            height=1,
                            font="12",
                            command=self.user_name_date
                            )

            self.add_destroyed(button1)
            self.add_destroyed(button2)
            self.add_destroyed(frame_between_buttons)
            self.add_destroyed(frame_first)

            frame_first.pack()
            button1.pack()
            frame_between_buttons.pack()
            button2.pack()

        else:
            self.user_name_date()

    def list_test(self):
        self.destroyed() # уничтожаем элементы, которые были до этого
        frame1 = Frame(self,
                       height=10,
                       bg="#5FD2B5")
        frame11 = Frame(self,
                       height=10,
                       bg="#5FD2B5")
        frame2 = Frame(self,
                       height=15,
                       bg="#5FD2B5")

        frame_between_text_and_buttons = Frame(self,
                                               height=12,
                                               bg="#5FD2B5")

        label1 = Label(self,
                       text="Возраст от 11 до 18 лет:",
                       foreground="#FFF",
                       bg="#5FD2B5",
                       font="16")

        label2 = Label(self,
                       text="Возраст от 6 до 9 лет:",
                       foreground="#FFF",
                       bg="#5FD2B5",
                       font="16")

        label3 = Label(self,
                       text="Возраст от 7 до 13 лет:",
                       foreground="#FFF",
                       bg="#5FD2B5",
                       font="16")


        button1 = Button(self,
                         text=all_tests_list[1],
                         height=int(self.height/300),
                         width=int(self.width/16),
                         padx="20",
                         pady="8",
                         font="16",
                         command=self.define1)

        button2 = Button(self,
                         text=all_tests_list[2],
                         height=int(self.height/300),
                         width=int(self.width/16),
                         padx="20",
                         pady="8",
                         font="16",
                         command=self.define2)

        button3 = Button(self,
                         text=all_tests_list[3],
                         height=int(self.height/300),
                         width=int(self.width/16),
                         padx="20",
                         pady="8",
                         font="16",
                         command=self.define3)

        button4 = Button(self,
                         text=all_tests_list[4],
                         height=int(self.height / 300),
                         width=int(self.width / 16),
                         padx="20",
                         pady="8",
                         font="16",
                         command=self.define4)

        frame15 = Frame(self,
                        height=10,
                        bg="#5FD2B5")
        frame5 = Frame(self,
                       height=15,
                       bg="#5FD2B5")

        button5 = Button(self,
                         text=all_tests_list[5],
                         height=int(self.height / 300),
                         width=int(self.width / 16),
                         padx="20",
                         pady="8",
                         font="16",
                         command=self.define5)

        self.add_destroyed(label1)
        self.add_destroyed(label2)
        self.add_destroyed(frame2)
        self.add_destroyed(frame_between_text_and_buttons)
        self.add_destroyed(button1)
        self.add_destroyed(button2)
        self.add_destroyed(button3)
        self.add_destroyed(button4)
        self.add_destroyed(button5)
        self.add_destroyed(frame11)
        self.add_destroyed(frame15)
        self.add_destroyed(frame5)
        self.add_destroyed(label3)


        frame1.pack(fill=BOTH)
        label1.pack()
        frame_between_text_and_buttons.pack()
        button1.pack()
        button2.pack()
        button3.pack()
        frame2.pack(fill=BOTH)
        label2.pack()
        frame11.pack()
        button4.pack()
        frame15.pack()
        label3.pack()
        frame5.pack()
        button5.pack()


    def save_name(self):
        if self.message.get() == "" or self.message1.get() == "":
            messagebox.showinfo("Внимание!", "Пожалуйста, заполните пустое поле")
            self.user_name_date()
        else:
            self.name_user = self.message.get()
            self.date_user = self.message1.get()
            self.list_test()

    def user_name_date(self):
        self.destroyed()
        frame_first = Frame(self,
                            bg="#5FD2B5",
                            height=160)
        frame = Frame(self,
                      bg="#5FD2B5")
        label_name = Label(frame,
                           text="Введите имя:",
                           font="12",
                           bg="#5FD2B5")

        label_date = Label(frame,
                           text="Дата:",
                           font="12",
                           bg="#5FD2B5")

        self.message = StringVar()
        self.message1 = StringVar()
        enter_FIO = Entry(frame,
                          textvariable=self.message,
                          width=40)

        enter_date = Entry(frame,
                           textvariable=self.message1,
                           width=40)

        enter_date.insert(0, datetime.date.today().strftime("%Y-%d-%m"))

        # Строку с датой делаем только для чтения
        enter_date['state'] = "readonly"

        button = Button(frame,
                        text="Далее",
                        width=12,
                        height=1,
                        font=6,
                        command=self.save_name)

        button_main = Button(frame,
                             text="Главная",
                             width=12,
                             height=1,
                             font=6,
                             command=self.main_window)

        self.add_destroyed(frame_first)
        self.add_destroyed(label_name)
        self.add_destroyed(label_date)
        self.add_destroyed(enter_FIO)
        self.add_destroyed(enter_date)
        self.add_destroyed(button)
        self.add_destroyed(frame)

        frame_first.pack()
        frame.pack()
        enter_FIO.grid(row=2, column=3) #.place(x=160, y=22)
        enter_date.grid(row=3, column=3) #.place(x=160, y=52)
        label_name.grid(row=2, column=2) #.place(x=10, y=15)
        label_date.grid(row=3, column=2) #.place(x=10, y=45)
        button.grid(row=4, column=3, pady=10, sticky=tk.W) #.place(x=140, y=88)
        button_main.grid(row=5, column=3, sticky=tk.W)

    def open_file(self, file_name):
        list_questions = []
        with open(file_name, "r", encoding="UTF-8") as f:
            for line in f:
                list_questions.append(line.strip())
        return list_questions

    def save_result_button(self):
        file_name = fd.asksaveasfilename(
            filetypes=(("TXT files", "*.txt"),
                       ("All files", "*.*")))
        try:
            with open(file_name, "w", encoding="UTF-8") as f:
                f.write(self.global_text)
        except:
            pass

    def save_result_button_history(self):
        try:
            self.cursor.execute(f"""INSERT INTO save_result (name, date, name_test, info_result)
                                Values('{self.name_user}', '{datetime.datetime.today()}', '{self.test_name}', '{self.global_text}')""")
        except:
            pass

    def resize_image(self, size, img):
        width = size
        image = Image.open(img)
        ratio = (width / float(image.size[0]))
        height = int((float(image.size[1]) * float(ratio)))
        image = image.resize((width, height), PIL.Image.ANTIALIAS)
        return image

    def define1(self):
        self.test_name = all_tests_list[1]
        true_answer = [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,1,0,1,1,0,0,0,0,1,0,0,0,0,1,1,0,1,1,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.number_question = 0
        self.destroyed() # уничтожаем элементы, которые были до этого

        phillips_school = self.open_file("Phillips_School.txt")

        count_answer = len(phillips_school)
        answers = {a:0 for a in range(count_answer)}

        def print_end():
            p_list = []
            text = ""
            label3 = Label(self,
                           text="",
                           font="16",
                           height=10,
                           bg="#5FD2B5")

            for i in range(count_answer):
                if answers[i] != true_answer[i]:
                    p_list.append(i+1)
            def result(x, text_s):
                a = True
                for i in x:
                    if i not in p_list:
                         a = False
                         break
                if a == True:
                    return(text_s + "\n")
                else:
                    return ""

            text += result([2,3,7,12,16,21,23,26,28,46,47,48,49,50,51,52,53,54,55,56,57,58], "Общая школьная тревожность:")
            text += result([5, 10, 15, 20, 24, 30, 33, 36, 39, 42, 44 ], "Переживание социального стресса:")
            text += result([1, 3, 6, 11, 17, 19,25, 29, 32, 35, 38, 41, 43], "Фрустрация потребности в достижении успеха:")
            text += result([27, 31, 34, 37, 40, 45], "Страх самовыражения:")
            text += result([2, 7, 12, 16, 21, 26], "Страх ситуации проверки знаний:")
            text += result([3, 8, 13, 17, 22], "Страх несоответствия ожиданиям окружающих:")
            text += result([9, 14, 18, 23, 28], "Низкая физиологическая сопротивляемость стрессу:")
            text += result([2, 6, 11, 32, 35, 41, 44,  47], "Проблемы и страхи в отношениях с учителями:")
            text += "\n" + "Кол-во несовпадений: " + str(len(p_list)) + "/58" +"\n"
            text += "Значения показателей тревожности, превышающие 50-ти процентный рубеж, позволяют" + "\n"
            text += "говорить о повышенной тревожности, а превышающие 75 % — о высокой тревожности" + "\n"
            text += "ребенка." + "\n"
            label3["text"] = text
            self.global_text = text

            self.add_destroyed(label3)

            label3.pack()

        def change():
            answers[self.number_question] = var.get()

            if self.number_question + 1 != count_answer:
                self.number_question += 1
                if len(phillips_school[self.number_question]) <= 57:
                    label["text"] = phillips_school[self.number_question]
                else:
                    text_r = phillips_school[self.number_question][:57] + "\n"
                    text_r += phillips_school[self.number_question][57:]
                    label["text"] = text_r

            else:
                self.destroyed()
                label2 = Label(self,
                               text="Тест завершён",
                               font="16",
                               height=2,
                               bg="#5FD2B5")
                self.add_destroyed(label2)
                label2.pack(side=TOP)
                print_end()
                self.end_test()

        frame1 = Frame(self,
                      height=140,
                      bg="#5FD2B5")

        frame = Frame(self,
                      height=5,
                      bg="#5FD2B5")

        var = IntVar()
        var.set(0)
        No = Radiobutton(frame,
                         text="Нет",
                         variable=var,
                         font="11",
                         value=0,
                         bg="#5FD2B5")

        Yes = Radiobutton(frame,
                          text="Да",
                          font="11",
                          variable=var,
                          value=1,
                          bg="#5FD2B5")

        button = Button(frame,
                        text="Далее",
                        width=16,
                        height=1,
                        font=12,
                        command=change)




        label = Label(frame,
                      text=phillips_school[self.number_question],
                      font="14",
                      height=2,
                      foreground="#FFF",
                      bg="#5FD2B5")

        self.add_destroyed(label)
        self.add_destroyed(button)
        self.add_destroyed(frame)
        self.add_destroyed(Yes)
        self.add_destroyed(No)
        self.add_destroyed(frame1)

        frame1.pack()
        frame.pack()
        label.grid(row=0, column=1)
        Yes.grid(row=1, column=1)
        No.grid(row=2, column=1)
        button.grid(row=3, column=1)

    def define2(self):
        self.test_name = all_tests_list[2]
        self.destroyed() # уничтожаем элементы, которые были до этого
        self.number_question = 0
        text_answer = [["не очень", "нравится", "не нравится"],
                       ["чаще хочется остаться дома", "бывает по-разному", "иду с радостью"],
                       ["не знаю", "остался бы дома", "пошел бы в школу"],
                       ["не нравится", "бывает по-разному", "нравится"],
                       ["хотел бы", "не хотел бы", "не знаю"],
                       ["не знаю", "не хотел бы", "хотел бы"],
                       ["часто", "редко", "не рассказываю"],
                       ["точно не знаю", "хотел бы", "не хотел бы"],
                       ["мало", "много", "нет друзей"],
                       ["да", "не очень", "нет"]]
        # true_answer = [[1, 3, 0], [0, 1, 3], [1, 0, 3], [3, 1, 0], [0, 3, 1], [1, 3, 1], [3, 1, 0], [1, 0, 3], [1, 3, 0], [3, 1, 0]]

        phillips_school = self.open_file("level_school.txt")

        count_answer = len(phillips_school)
        answers = {a:0 for a in range(count_answer)}

        def print_end():
            true_answer = [[1, 3, 0], [0, 1, 3], [1, 0, 3], [3, 1, 0], [0, 3, 1], [1, 3, 1], [3, 1, 0], [1, 0, 3],
                           [1, 3, 0], [3, 1, 0]]
            count = 0
            text = ""
            label3 = Label(self,
                           text="",
                           font="16",
                           height=10,
                           bg="#5FD2B5")


            for i in range(count_answer):
                count += true_answer[i][answers[i]]

            text += "Всего набрано баллов: " + str(count) + "/30" + "\n" + "\n"
            if count >= 25:
                text += "высокий уровень школьной мотивации, учебной активности." + "\n" \
                    "Такие дети отличаются наличием высоких познавательных мотивов," + "\n" \
                    "стремлением наиболее успешно выполнять все предъявляемые школой" + "\n" \
                    "требования. Они очень четко следуют всем указаниям учителя," + "\n" \
                    "добросовестны и ответственны, сильно переживают, если получают" + "\n" \
                    "неудовлетворительные оценки или замечания педагога."
            elif count >= 20:
                text += "хорошая школьная мотивация. Подобные показатели" + "\n" \
                        "имеют большинство учащихся начальных классов, успешно справляющихся с учебной" + "\n" \
                        "деятельностью. Подобный уровень мотивации является средней нормой."
            elif count >= 15:
                text += "положительное отношение к школе, но школа" + "\n" \
                        "привлекает больше внеучебными сторонами. Такие дети достаточно благополучно" + "\n" \
                        "чувствуют себя в школе, однако чаще ходят в школу, чтобы общаться с друзьями, с учителем." + "\n" \
                        "Им нравится ощущать себя учениками, иметь красивый портфель, ручки, тетради." + "\n" \
                        "Познавательные мотивы у них сформированы в меньшей степени и учебный процесс их мало привлекает."
            elif count >= 10:
                text += "низкая школьная мотивация. Подобные школьники" + "\n" \
                        "посещают школу неохотно, предпочитают пропускать занятия. На уроках часто занимаются" + "\n" \
                        "посторонними делами, играми. Испытывают серьезные затруднения в учебной деятельности." + "\n" \
                        "Находятся в состоянии неустойчивой адаптации к школе."
            else:
                text += "негативное отношение к школе, школьная" + "\n" \
                        "дезадаптация. Такие дети испытывают серьезные трудности в школе: они не справляются с" + "\n" \
                        "учебной деятельностью, испытывают проблемы в общении с одноклассниками, во" + "\n" \
                        "взаимоотношениях с учителем. Школа нередко воспринимается ими как враждебная среда," + "\n" \
                        "пребывание в которой для них невыносимо. Маленькие дети (5 – 6 лет) часто плачут, просятся" + "\n" \
                        "домой. В других случаях ученики могут проявлять агрессивность, отказываться выполнить те" + "\n" \
                        "или иные задания, следовать тем или иным нормам и правилам. Часто у подобных школьников" + "\n" \
                        "отмечаются нарушения нервно – психического здоровья."


            label3["text"] = text
            self.global_text = text

            self.add_destroyed(label3)

            label3.pack()

        def change():
            answers[self.number_question] = var.get()
            if self.number_question + 1 != count_answer:
                self.number_question += 1
                if len(phillips_school[self.number_question]) <= 57:
                    label["text"] = phillips_school[self.number_question]
                else:
                    if len(phillips_school[self.number_question]) >= 100:
                        text_r = phillips_school[self.number_question][:57] + "\n"
                        text_r += phillips_school[self.number_question][57:120] + "\n"
                        text_r += phillips_school[self.number_question][120:]
                    else:
                        text_r = phillips_school[self.number_question][:57] + "\n"
                        text_r += phillips_school[self.number_question][57:]
                    label["text"] = text_r


                number1["text"] = text_answer[self.number_question][0]
                number2["text"] = text_answer[self.number_question][1]
                number3["text"] = text_answer[self.number_question][2]

            else:
                self.destroyed()
                label2 = Label(self,
                               text="Тест завершён",
                               font="16",
                               height=2,
                               bg="#5FD2B5")
                self.add_destroyed(label2)
                label2.pack(side=TOP)
                print_end()
                self.end_test()

        var = IntVar()
        var.set(0)
        number1 = Radiobutton(self,
                         text=text_answer[0][0],
                         variable=var,
                         font="11",
                         value=0,
                         bg="#5FD2B5")

        number2 = Radiobutton(self,
                          text=text_answer[0][1],
                          font="11",
                          variable=var,
                          value=1,
                          bg="#5FD2B5")

        number3 = Radiobutton(self,
                          text=text_answer[0][2],
                          font="11",
                          variable=var,
                          value=2,
                          bg="#5FD2B5")

        button = Button(self,
                        text="Далее",
                        width=16,
                        height=1,
                        font=12,
                        command=change)
        frame = Frame(self, height=5, bg="#5FD2B5")

        label = Label(self,
                      text=phillips_school[self.number_question],
                      font="14",
                      height=3,
                      foreground="#FFF",
                      bg="#5FD2B5")

        self.add_destroyed(label)
        self.add_destroyed(button)
        self.add_destroyed(frame)
        self.add_destroyed(button)
        self.add_destroyed(number1)
        self.add_destroyed(number2)
        self.add_destroyed(number3)

        label.place(x=10, y=30)
        number1.place(x=20, y=100)
        number2.place(x=20, y=130)
        number3.place(x=20, y=160)
        frame.pack()
        button.place(x=380, y=200)

    def define3(self):
        self.test_name = all_tests_list[3]
        self.destroyed() # уничтожаем элементы, которые были до этого


        self.number_question = 0
        answers = [0,0]
        count_answer = 2

        def result(an):
            text2 = ""
            if an in [1, 3, 6, 7]:
                text2 += "характеризует установку на преодоление препятствий"
            elif an in [2, 11, 12, 18, 19]:
                text2 += "общительность, дружескую поддержку"
            elif an == 4:
                text2 += "устойчивость положения (желание добиваться успехов, не преодолевая трудности)"
            elif an == 5:
                text2 += "утомляемость, общая слабость, небольшой запас сил, застенчивость"
            elif an == 9:
                text2 += "мотивация на развлечения"
            elif an == 8:
                text2 += "отстраненность от учебного процесса, уход в себя"
            elif an == 14:
                text2 += "кризисное состояние, «падение в пропасть»"
            elif an == 20:
                text2 += "часто выбирают как перспективу учащиеся с завышенной самооценкой и установкой на лидерство."
            return text2

        def print_end():
            text = ""
            label3 = Label(self,
                           text="",
                           font="16",
                           height=10,
                           bg="#5FD2B5")

            text += "Характеристика: " + "\n" + "\n"
            text += "Вы на данный момент обладаете следующим - " + "\n"
            text += result(int(answers[0])) + "\n"
            text += "Но вот то, куда вы хотели бы стремиться -" + "\n"
            text += result(int(answers[1]))

            label3["text"] = text
            self.global_text = text

            self.add_destroyed(label3)

            label3.pack()

        def change():
            if self.number_question + 1 != count_answer:
                if self.message.get() != "":
                    if not self.message.get().isdigit():
                        messagebox.showinfo("Внимание!", "Пожалуйста, введите номер человечка.")
                    else:
                        if (int(self.message.get()) not in [x for x in range(1, 21)]):
                            messagebox.showinfo("Внимание!", "Упс, такого номера человечка нет :(")
                        else:
                            answers[self.number_question] = self.message.get()
                            self.number_question += 1
                            enter_date.delete(0, END)
                            label_text["text"] = """Введите в поле ниже номер того человечка, которым вы хотели\n бы быть и на чьем месте вы хотели бы находиться."""
                else:
                    messagebox.showinfo("Внимание!", "Пожалуйста, заполните пустое поле")
            else:
                answers[self.number_question] = self.message.get()
                self.destroyed()

                label2 = Label(self,
                               text="Тест завершён",
                               font="16",
                               height=2,
                               bg="#5FD2B5")
                self.add_destroyed(label2)

                label2.pack(side=TOP)
                print_end()
                self.end_test()

        var = IntVar()
        var.set(0)

        img = ImageTk.PhotoImage(self.resize_image(420, Path("Derevo_Pon.jpg")))
        label = Label(self,
                      image=img)
        label.image = img

        label_text = Label(self,
                           text="""Введите в поле ниже номер того человечка, кто напоминает вам себя,\n похож на вас, ваше настроение в школе и ваше положение.""",
                           bg="#5FD2B5",
                           font="Times 16")


        frame = Frame(self,
                      bg="#5FD2B5")

        label_inp = Label(frame,
                          text="Ваш ответ: ",
                          font="Times 10",
                          bg="#5FD2B5")


        button = Button(frame,
                        text="Далее",
                        width=8,
                        height=1,
                        font=12,
                        command=change)

        self.message = StringVar()
        enter_date = Entry(frame,
                           textvariable=self.message,
                           width=30)

        self.add_destroyed(label)
        self.add_destroyed(label_text)
        self.add_destroyed(button)
        self.add_destroyed(frame)
        self.add_destroyed(enter_date)

        label_text.pack()
        label.pack()
        frame.pack()
        enter_date.grid(row=0, column=1, pady=10, padx=10)
        label_inp.grid(row=0, column=0, pady=10)
        button.grid(row=1, column=1, pady=10)

    def define4(self):
        self.test_name = all_tests_list[4]
        self.destroyed() # уничтожаем элементы, которые были до этого

        self.number_question = 0
        answers = [0,0,0,0,0,0,0,0,0,0]
        count_answer = 12

        def print_end():
            count = 0
            text = ""

            label3 = Label(self,
                           text="",
                           font="16",
                           height=10,
                           bg="#5FD2B5")

            for i in range(count_answer - 2):
                count += answers[i]

            text += "Всего набрано баллов: " + str(count) + "/10" + "\n" + "\n"
            text += "Общий уровень тревожности моэно вычислить по ответам," + "\n"
            text += "характеризующим настроение персонажа рисунка как грустное, " + "\n"
            text += "недовольное, печальное, сердитое, скучное, испуганное." + "\n"
            text += "Тревожным можно считать человека, набравшего 7 и более подобных в данном тесте."

            label3["text"] = text
            self.global_text = text

            self.add_destroyed(label3)

            label3.pack()

        def change():
            if 10 >= self.number_question >= 1:
                answers[self.number_question-1] = var.get()
            if self.number_question + 1 != count_answer:
                self.number_question += 1
                img = ImageTk.PhotoImage(self.resize_image(420, Path("test4", str(self.number_question) + ".jpg")))
                label.configure(image = img)
                label.image = img

            else:
                self.destroyed()

                label2 = Label(self,
                               text="Тест завершён",
                               font="16",
                               height=2,
                               bg="#5FD2B5")
                self.add_destroyed(label2)

                label2.pack(side=TOP)

                print_end()
                self.end_test()


        var = IntVar()
        var.set(0)

        img = ImageTk.PhotoImage(self.resize_image(420, Path("test4", "0.jpg")))
        label = Label(self,
                      image=img)
        label.image = img

        label_text = Label(self,
                           text="""Что выражает лицо ребёнка на рисунке?\nОпиши вслух, почему""",
                           bg="#5FD2B5",
                           font="Times 16")

        frame = Frame(self,
                      bg="#5FD2B5")

        number1 = Radiobutton(frame,
                              text="Радость или спокойствие",
                              variable=var,
                              font="Times 11",
                              value=0,
                              bg="#5FD2B5")

        number2 = Radiobutton(frame,
                              text="Грусть или раздражение",
                              font="Times 11",
                              variable=var,
                              value=1,
                              bg="#5FD2B5")

        button = Button(frame,
                        text="Далее",
                        width=8,
                        height=1,
                        font=12,
                        command=change)

        self.add_destroyed(label)
        self.add_destroyed(number1)
        self.add_destroyed(number2)
        self.add_destroyed(button)
        self.add_destroyed(frame)
        self.add_destroyed(label_text)

        label.pack()
        label_text.pack()
        frame.pack()
        number1.grid(row=0, column=0, sticky=E, pady=20)
        number2.grid(row=0, column=2, sticky=W, pady=20)
        button.grid(row=1, column=1, pady=10)

    def define5(self):
        self.test_name = all_tests_list[5]
        true_answer = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.number_question = 0
        self.destroyed() # уничтожаем элементы, которые были до этого

        phillips_school = self.open_file("creative.txt")

        count_answer = len(phillips_school)

        def print_end():
            count = 0
            text = ""
            label3 = Label(self,
                           text="",
                           font="16",
                           height=10,
                           bg="#5FD2B5")

            for i in true_answer:
                count += int(i)

            text += "Всего набрано баллов: " + str(count) + "/23" + "\n" + "\n"
            if count >= 23:
                text += "Ребенок очень сообразителен, способен иметь собственную точку" + "\n"
                text += "зрения на окружающее, и следует помогать ему в этом." + "\n"
                text += "Все задатки творческой личности."
            elif count >= 15:
                text += "Ребенок не всегда обнаруживает свои способности, он находчив" + "\n"
                text += "и сообразителен, лишь когда чем-нибудь заинтересован." + "\n"
                text += "Помогайте ему добиваться успеха в интересующей его области."
            elif count >= 9:
                text += "Большая сообразительность, достаточная для многих областей знаний," + "\n"
                text += "где не обязателен собственный взгляд на вещи." + "\n"
                text += "Но для занятий творчеством многого не хватает."
            elif count >= 4:
                text += "Большая сообразительность, достаточная для многих областей знаний," + "\n"
                text += "где не обязателен собственный взгляд на вещи." + "\n"
                text += "Но для занятий творчеством многого не хватает."
            elif count >= 0:
                text += "Ребенку не хватает изобретательности, но он может достичь" + "\n"
                text += "успеха как хороший исполнитель, даже в сложных профессиях."

            label3["text"] = text
            self.global_text = text

            self.add_destroyed(label3)

            label3.pack()

        def change():
            true_answer[self.number_question] = var.get()

            if self.number_question + 1 != count_answer:
                self.number_question += 1
                if len(phillips_school[self.number_question]) <= 57:
                    label["text"] = phillips_school[self.number_question]
                else:
                    text_r = phillips_school[self.number_question][:57] + "\n"
                    text_r += phillips_school[self.number_question][57:]
                    label["text"] = text_r

            else:
                self.destroyed()
                label2 = Label(self,
                               text="Тест завершён",
                               font="16",
                               height=2,
                               bg="#5FD2B5")
                self.add_destroyed(label2)
                label2.pack(side=TOP)
                print_end()
                self.end_test()

        frame1 = Frame(self,
                       height=140,
                       bg="#5FD2B5")

        frame = Frame(self,
                      height=5,
                      bg="#5FD2B5")

        var = IntVar()
        var.set(0)
        No = Radiobutton(frame,
                         text="Нет",
                         variable=var,
                         font="11",
                         value=0,
                         bg="#5FD2B5")

        Yes = Radiobutton(frame,
                          text="Да",
                          font="11",
                          variable=var,
                          value=1,
                          bg="#5FD2B5")

        button = Button(frame,
                        text="Далее",
                        width=16,
                        height=1,
                        font=12,
                        command=change)




        label = Label(frame,
                      text=phillips_school[self.number_question][:34] + "\n" + phillips_school[self.number_question][34:],
                      font="14",
                      height=2,
                      foreground="#FFF",
                      bg="#5FD2B5")

        self.add_destroyed(label)
        self.add_destroyed(button)
        self.add_destroyed(frame)
        self.add_destroyed(Yes)
        self.add_destroyed(No)
        self.add_destroyed(frame1)

        frame1.pack()
        frame.pack()
        label.grid(row=0, column=1)
        Yes.grid(row=1, column=1)
        No.grid(row=2, column=1)
        button.grid(row=3, column=1)

    def end_test(self):
        frame = Frame(self,
                      height=10,
                      bg="#5FD2B5")

        frame2 = Frame(self,
                      height=10,
                      bg="#5FD2B5")


        button_save_txt = Button(self,
                                 text="Сохранить ответы в файл",
                                 width=30,
                                 height=2,
                                 font="Times 14",
                                 command=self.save_result_button)

        button_save_history = Button(self,
                                     text="Сохранить ответы в истории",
                                     width=30,
                                     font="Times 14",
                                     height=2,
                                     command=self.save_result_button_history)

        button_main = Button(self,
                             text="Главная",
                             width=30,
                             font="Times 14",
                             height=2,
                             command=self.main_window)


        self.add_destroyed(button_save_txt)
        self.add_destroyed(button_save_history)
        self.add_destroyed(frame)
        self.add_destroyed(frame2)
        self.add_destroyed(button_main)

        button_save_txt.pack()
        frame.pack()
        button_save_history.pack()
        frame2.pack()
        button_main.pack()

    def add_destroyed(self, object):
        self.des.append(object)

    def destroyed(self):
        for obj in self.des:
            obj.destroy()


class Window(Tk):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.width = 450
        self.height = 140
        self.minsize(width=self.width, height=self.height)  # устанавливаем ширину и высоту
        self.title("О программе")  # устанавливаем заголовок main

        text = "Данная программа предназначена для психологического" + "\n" \
                "тестирования и не является конечным средством для" + "\n" \
                "постановки диагноза или исчерпывающей оценки состояния" + "\n" \
                "человека." + "\n" + "\n" + "Автор программы - Осадчий И.А."
        label = Label(self,
                      text=text)
        frame1 = Frame(self,
                       height=20)
        frame2 = Frame(self,
                       height=20)

        frame1.pack(fill=BOTH)
        label.pack()
        frame2.pack(fill=BOTH)

class Info_result(Tk):
    def __init__(self, text, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.width = 450
        self.height = 450
        self.minsize(width=self.width, height=self.height)  # устанавливаем ширину и высоту
        self.title("Результат теста")  # устанавливаем заголовок main
        label = Label(self,
                      text=text)

        frame1 = Frame(self,
                       height=20)

        frame2 = Frame(self,
                       height=20)

        frame1.pack(fill=BOTH)
        label.pack()
        frame2.pack(fill=BOTH)

if __name__ == '__main__':
    MainApp().mainloop()

