def popup(cls):
    '''Функция переделки класса
Передайте ей как аргумент нужный класс (Button, Label, Frame...),
чтобы получить класс Popup (нужный класс со всплывающим окном)'''

    class Popup(cls):
        '''Переделанный класс
При создании укажите popup_text (при желании и popup_font) для
настройки всплывабщего сообщения'''

        def __init__(self, master, cnf={}, **kw):
            from tkinter import Label as l
            self.master = master
            self.tk = master.tk  # Tkinter
            # Получить настройки "всплывайки" и удалить их из настроек
            PT = (kw['popup_text'] if 'popup_text' in kw else '')
            PF = (kw['popup_font'] if 'popup_font' in kw else (None,))
            if 'popup_text' in kw:
                del kw['popup_text']
            if 'popup_font' in kw:
                del kw['popup_font']
            super().__init__(master=master, cnf=cnf, **kw)  # Создать виджет выше
            self.bind('<Enter>', self.UP)
            self.bind('<Motion>', self.UP)
            self.bind('<Leave>', self.DN)  # Реакция на движения
            self.POPUP = l(self.master, text=PT, font=PF)  # Создать "всплывайку"
            self._conf = self.config
            self.config = self.configure = self.nc  # Подмена функций настройки

        def nc(self, **kw):
            # Настройка - текст/шрифт всплывайки? если да, передать всплывайке; если нет - родителю.
            if 'popup_text' in kw:
                self.POPUP.config(text=kw['popup_text'])
                del kw['popup_text']
            if 'popup_font' in kw:
                self.POPUP.config(font=kw['popup_font'])
                del kw['popup_font']
            self._conf(**kw)

        def UP(self, e):
            self.POPUP.place(x=self.winfo_rootx() + e.x, y=self.winfo_rooty() + e.y, anchor='nw')
            self.POPUP.lift()
            # Это может вести себя странно

        def DN(self, e):
            self.POPUP.place_forget()

    return Popup


if __name__ == '__main__':
    from tkinter import Tk, Button, Entry, Label

    tk = Tk()
    tk.title('test Test TeStEs')

    def text_a(event):
        global Button
        Button["text"] = "a"
    def text_del(event):
        global Button
        Button["text"] = ""

    Button = Button(tk)
    Button.bind("<Enter>", text_a)
    Button.bind("<Leave>", text_del)



    Label = popup(Label)
    Entry = popup(Entry)

    Label(tk, text='test', popup_text='test').place(x=34, y=25)
    Button.place(x=50, y=50)
    Entry(tk, popup_text='TESTING').place(x=0, y=100)
    tk.mainloop()