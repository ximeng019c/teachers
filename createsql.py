from asyncio import windows_events
from this import s
import tkinter as tk
import sqlite3
import tkinter.messagebox as messagebox

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # 标签和输入框
        self.name_label = tk.Label(self, text="姓名")
        self.name_label.pack()

        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        self.id_number_label = tk.Label(self, text="身份证号")
        self.id_number_label.pack()

        self.id_number_entry = tk.Entry(self)
        self.id_number_entry.pack()

        self.address_label = tk.Label(self, text="地址")
        self.address_label.pack()

        self.address_entry = tk.Entry(self)
        self.address_entry.pack()

        self.phone_number_label = tk.Label(self, text="电话号码")
        self.phone_number_label.pack()

        self.phone_number_entry = tk.Entry(self)
        self.phone_number_entry.pack()

        self.department_label = tk.Label(self, text="部门")
        self.department_label.pack()

        self.department_entry = tk.Entry(self)
        self.department_entry.pack()

        self.salary_label = tk.Label(self, text="工资")
        self.salary_label.pack()

        self.salary_entry = tk.Entry(self)
        self.salary_entry.pack()

        self.work_time_label = tk.Label(self, text="参加工作时间")
        self.work_time_label.pack()

        self.work_time_entry = tk.Entry(self)
        self.work_time_entry.pack()

        self.major_label = tk.Label(self, text="专业")
        self.major_label.pack()

        self.major_entry = tk.Entry(self)
        self.major_entry.pack()

        self.position_label = tk.Label(self, text="职务")
        self.position_label.pack()

        self.position_entry = tk.Entry(self)
        self.position_entry.pack()

        self.note_label = tk.Label(self, text="备注")
        self.note_label.pack()

        self.note_entry = tk.Entry(self)
        self.note_entry.pack()

        # 按钮
        self.add_button = tk.Button(self)
        self.add_button["text"] = "添加教师信息"
        self.add_button["command"] = self.add_teacher_info
        self.add_button.pack(side="top")

        self.search_button = tk.Button(self)
        self.search_button["text"] = "浏览教师信息"
        self.search_button["command"] = self.search_teacher_info
        self.search_button.pack(side="top")

        self.update_button = tk.Button(self)
        self.update_button["text"] = "查找教师信息"
        self.update_button["command"] = self.update_teacher_info
        self.update_button.pack(side="top")

        self.update_button = tk.Button(self)
        self.update_button["text"] = "修改教师信息"
        self.update_button["command"] = self.edit_teacher_info
        self.update_button.pack(side="top")

        self.delete_button = tk.Button(self)
        self.delete_button["text"] = "删除教师信息"
        self.delete_button["command"] = self.delete_teacher_info
        self.delete_button.pack(side="top")

    def add_teacher_info(self):
    # 获取用户输入的教师信息
        name = self.name_entry.get().strip()
        id_number = self.id_number_entry.get().strip()
        address = self.address_entry.get().strip()
        phone_number = self.phone_number_entry.get().strip()
        department = self.department_entry.get().strip()
        salary = float(self.salary_entry.get())
        work_time = self.work_time_entry.get().strip()
        major = self.major_entry.get().strip()
        position = self.position_entry.get().strip()
        note = self.note_entry.get().strip()

    # 向数据库中插入数据
        conn = sqlite3.connect('teacher.db')
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM teacher_info")
        max_id_result = cursor.fetchone()[0]
        if max_id_result:
            id = int(max_id_result) + 1
        else:
            id = 1
        cursor.execute("INSERT INTO teacher_info(id, name, id_number, address, phone_number, department, salary, work_time, major, position, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                    (id, name, id_number, address, phone_number, department, salary, work_time, major, position, note))
        conn.commit()
        cursor.close()
        conn.close()


    def search_teacher_info(self):
        # 获取用户输入的查询条件
        name = self.name_entry.get()
        id_number = self.id_number_entry.get()
        address = self.address_entry.get()
        phone_number = self.phone_number_entry.get()
        department = self.department_entry.get()

        # 构造SQL查询语句
        select_sql = "SELECT * FROM teacher_info WHERE 1=1"
        

        # 从数据库中查询数据
        conn = sqlite3.connect('teacher.db')
        cursor = conn.cursor()
        cursor.execute(select_sql)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # 将查询结果显示在GUI界面上
        result_window = tk.Toplevel(self)
        for row in rows:
            for info in row:
                tk.Label(result_window, text=info, relief=tk.RIDGE).grid(sticky=tk.W)
            tk.Frame(result_window, height=1, bg='black').grid(row=result_window.grid_size()[1], columnspan=100, sticky=tk.W+tk.E)

    def update_teacher_info(self):
    # 获取用户输入的教师姓名和身份证号
        name = self.name_entry.get().strip()
        id_number = self.id_number_entry.get().strip()

    # 从数据库中查询需要更新的教师信息，并将其填充到GUI界面上
        conn = sqlite3.connect('teacher.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teacher_info WHERE name=? OR id_number=?", (name, id_number))
        rows = cursor.fetchall()
        if not rows:
            tk.messagebox.showerror("错误", "未找到指定的教师信息！")
            return

        for row in rows:
            result_window = tk.Toplevel(self)
            result_label = tk.Label(result_window, text=row[1:-1], relief=tk.RIDGE)
            result_label.pack(padx=10, pady=5)
            select_button = tk.Button(result_window, text="选择", command=lambda x=row, window=result_window: self.fill_teacher_info(x, window))
            select_button.pack(pady=5)
            # 关闭数据库连接
        cursor.close()
        conn.close()


    def fill_teacher_info(self, row,windows):
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, row[1])
        self.id_number_entry.delete(0, tk.END)
        self.id_number_entry.insert(0, row[2])
        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, row[3])
        self.phone_number_entry.delete(0, tk.END)
        self.phone_number_entry.insert(0, row[4])
        self.department_entry.delete(0, tk.END)
        self.department_entry.insert(0, row[5])
        self.salary_entry.delete(0, tk.END)
        self.salary_entry.insert(0, row[6])
        self.work_time_entry.delete(0, tk.END)
        self.work_time_entry.insert(0, row[7])
        self.major_entry.delete(0, tk.END)
        self.major_entry.insert(0,row[8])
        self.position_entry.delete(0, tk.END)
        self.position_entry.insert(0,row[9])
        self.note_entry.delete(0, tk.END)
        self.note_entry.insert(0,row[10])
        # 填充完教师信息后，关闭窗口
        windows.destroy()

    def edit_teacher_info(self):
        # 获取用户输入的教师信息
        name = self.name_entry.get().strip()
        id_number = self.id_number_entry.get().strip()
        address = self.address_entry.get().strip()
        phone_number = self.phone_number_entry.get().strip()
        department = self.department_entry.get().strip()
        salary = float(self.salary_entry.get().strip())
        work_time = self.work_time_entry.get().strip()
        major = self.major_entry.get().strip()
        position = self.position_entry.get().strip()
        note = self.note_entry.get().strip()

        # 更新数据库中对应的教师信息
        conn = sqlite3.connect('teacher.db')
        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE teacher_info SET address=?, phone_number=?, department=?, salary=?, work_time=?, major=?, position=?, note=? WHERE name=? AND id_number=?", (address, phone_number, department, salary, work_time, major, position, note, name, id_number))
            conn.commit()  # 进行 SQL COMMIT 操作

            if cursor.rowcount == 1:
                tk.messagebox.showinfo('提示', '更新成功！')
            else:
                tk.messagebox.showerror('错误', '更新失败，未找到指定的教师记录！')
        except Exception as e:
            conn.rollback()
            tk.messagebox.showerror('错误', f'更新失败，发生以下异常：\n{str(e)}')

        cursor.close()
        conn.close()


   
    def delete_teacher_info(self):
        # 获取用户输入的教师姓名和身份证号
        name = self.name_entry.get()
        id_number = self.id_number_entry.get()

        # 从数据库中查询需要删除的教师信息
        conn = sqlite3.connect('teacher.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teacher_info WHERE name=? AND id_number=?", (name, id_number))
        row = cursor.fetchone()
        if not row:
            tk.messagebox.showerror("错误", "未找到指定的教师信息！")
            return

        # 弹出确认对话框
        confirm = messagebox.askyesno("确认删除", "确认删除该教师信息吗？")
        if confirm:
            # 从数据库中删除指定的教师信息
            cursor.execute("DELETE FROM teacher_info WHERE name=? AND id_number=?", (name, id_number))
            conn.commit()
            tk.messagebox.showinfo("成功", "教师信息删除成功！")
            self.name_entry.delete(0, tk.END)
            self.id_number_entry.delete(0, tk.END)
            self.address_entry.delete(0, tk.END)
            self.phone_number_entry.delete(0, tk.END)
            self.department_entry.delete(0, tk.END)
            self.salary_entry.delete(0, tk.END)
            self.work_time_entry.delete(0, tk.END)
            self.major_entry.delete(0, tk.END)
            self.position_entry.delete(0, tk.END)
            self.note_entry.delete(0, tk.END)

        cursor.close()
        conn.close() 


root = tk.Tk()
app = Application(master=root)
app.mainloop()