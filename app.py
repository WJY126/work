# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect
import pymysql

# 连接数据库
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    db='students',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor # 返回结果为字典类型
)

# 创建Flask应用
app = Flask(__name__)
import pymysql

app = Flask(__name__)


# MySQL configurations
db = pymysql.connect(host='localhost', user='root', password='123456', database='students', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()


@app.route('/')
def index():
    # 查询所有学生信息
    cursor.execute("SELECT * FROM students_info")
    students = cursor.fetchall()

    return render_template('index.html', students=students)


@app.route('/add', methods=['POST'])
def add():
    # 获取表单中的学生信息
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']

    # 将学生信息插入到数据库中
    cursor.execute("INSERT INTO students_info (name, age, gender) VALUES (%s, %s, %s)", (name, age, gender))
    db.commit()

    return redirect('/')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    # 根据学生ID获取更改前的学生信息
    cursor.execute("SELECT * FROM students_info WHERE id=%s", (id,))
    student = cursor.fetchone()

    if request.method == 'POST':
        # 获取表单中编辑后的学生信息
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']

        # 将新的学生信息更新到数据库中
        cursor.execute("UPDATE students_info SET name=%s, age=%s, gender=%s WHERE id=%s", (name, age, gender, id))
        db.commit()

        return redirect('/')

    return render_template('edit.html', student=student)


@app.route('/delete/<int:id>')
def delete(id):
    # 根据学生ID从数据库中删除学生信息
    cursor.execute("DELETE FROM students_info WHERE id=%s", (id,))
    db.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
