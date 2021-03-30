from flask import Flask, render_template, request, flash
import sqlite3
import os

currentdirectory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/form', methods=["GET", "POST"])
def form():
    if request.method=="GET":
        return render_template("form.html")

    if request.method=="POST":
        
        month_no_form=0
        form_data = []
        query1_data = []
        kid_form = request.form.get("kids")
        form_data.append(kid_form)
        query1_data.append(kid_form)
        year_form = request.form.get("years")
        form_data.append(year_form)
        query1_data.append(year_form)
        month_form = request.form.get("months")
        if month_form == "Jan":
            month_no_form = 1
        if month_form == "Feb":
            month_no_form = 2
        if month_form == "Mar":
            month_no_form = 3
        if month_form == "Apr":
            month_no_form = 4
        if month_form == "May":
            month_no_form = 5
        if month_form == "Jun":
            month_no_form = 6
        if month_form == "Jul":
            month_no_form = 7
        if month_form == "Aug":
            month_no_form = 8
        if month_form == "Sep":
            month_no_form = 9
        if month_form == "Oct":
            month_no_form = 10
        if month_form == "Nov":
            month_no_form = 11
        if month_form == "Dec":
            month_no_form = 12

        form_data.append(month_form)
        query1_data.append(month_form)
        form_data.append(month_no_form)
        day_form = request.form.get("days")
        form_data.append(day_form)
        query1_data.append(day_form)
        lunch_form = request.form.get("lunch")
        if lunch_form != "lunch":
            lunch_form = "-"
        
        form_data.append(lunch_form)
        
        dinner_form = request.form.get("dinner")
        if dinner_form != "dinner":
            dinner_form = "-"
        form_data.append(dinner_form)
         
        connection = sqlite3.connect(currentdirectory + "/whatwaseaten.db")
        cursor = connection.cursor()

        query1 = """SELECT * FROM calendar WHERE Kid = ? AND Year = ? AND Month = ? AND Day = ?"""
        result_query1 = cursor.execute(query1, query1_data) 
        result_query1 = result_query1.fetchall()
        result_query1 = len(result_query1)

        if result_query1 == 0:
            query2 = """INSERT INTO calendar (Kid, Year, Month, Month_no, Day, Lunch, Dinner) VALUES (?,?,?,?,?,?,?)"""
            cursor.execute(query2, form_data)
            connection.commit()
            connection.close()
            msg = "Data entered successfully"

            return render_template ('form.html', msg=msg)

        else:
            msg = "Data for this day is already entered"
            return render_template ("form.html", msg=msg)

@app.route('/calendar', methods=["GET", "POST"])
def calendar():
    if request.method=="GET":
        return render_template("calendar.html")

    if request.method=="POST":
        
        form_data = []
        kid_form = request.form.get("kids")
        form_data.append(kid_form)
        year_form = request.form.get("years")
        form_data.append(year_form)
        month_form = request.form.get("months")
        form_data.append(month_form)
         
        connection = sqlite3.connect(currentdirectory + "/whatwaseaten.db")
        cursor = connection.cursor()

        query1 = """SELECT * FROM calendar WHERE Kid = ? AND Year = ? AND Month = ? ORDER BY Day ASC"""
        result = cursor.execute(query1, form_data)
        rows=result.fetchall()

        connection.commit()
        connection.close()

        return render_template('calendar.html', kid_form=kid_form, year_form=year_form, month_form=month_form, rows=rows)

@app.route('/summary', methods=["GET", "POST"])
def summary():
    if request.method=="GET":
        return render_template("summary.html")

    if request.method=="POST":
        form_data = []
        kid_form = request.form.get("kids")
        form_data.append(kid_form)
        year_form = request.form.get("years")
        form_data.append(year_form)
        month_form = request.form.get("months")
        form_data.append(month_form)
         
        connection = sqlite3.connect(currentdirectory + "/whatwaseaten.db")
        cursor = connection.cursor()

        query1 = """SELECT * FROM calendar WHERE Kid = ? AND Year = ? AND Month = ?"""
        result = cursor.execute(query1, form_data)
        result=result.fetchall()

        lunch_counter = 0
        dinner_counter = 0

        for i in range(len(result)):
            entry = result[i]
            if entry[5] == 'lunch':
                lunch_counter = lunch_counter + 1
            if entry[6] =='dinner':
                dinner_counter = dinner_counter + 1

        connection.commit()
        connection.close()

    return render_template('summary.html', kid_form = kid_form, year_form = year_form, month_form = month_form, lunch_counter=lunch_counter, dinner_counter = dinner_counter)

@app.route('/delete', methods=["GET", "POST"])
def delete():
    if request.method=="GET":
        connection = sqlite3.connect(currentdirectory + "/whatwaseaten.db")
        cursor = connection.cursor()

        query1 = """SELECT * FROM calendar ORDER BY Year DESC, Month_no DESC, Day DESC"""
        result = cursor.execute(query1)
        rows=result.fetchall()
        
        connection.commit()
        connection.close()

        return render_template("delete.html", rows=rows)

    if request.method=="POST":

        connection = sqlite3.connect(currentdirectory + "/whatwaseaten.db")
        cursor = connection.cursor()

        delete = request.form.get("delete")
        string = delete.split()
        
        form_data = []
        kid_form = string[0]
        form_data.append(kid_form)
        year_form = string[1]
        form_data.append(year_form)
        month_form = string[2]
        form_data.append(month_form)
        day_form = string[3]
        form_data.append(day_form)

        query3 = """DELETE from calendar WHERE Kid = ? AND Year = ? AND Month = ? AND Day = ?"""
        cursor.execute(query3, form_data)

        msg = "Entry deleted"

        query1 = """SELECT * FROM calendar ORDER BY Year DESC, Month_no DESC, Day DESC"""
        result = cursor.execute(query1)
        rows=result.fetchall()

        connection.commit()
        connection.close()
        
        return render_template('delete.html', rows=rows, msg=msg)

if __name__ == "__main__":
    app.run()