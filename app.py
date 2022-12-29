#app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2 #pip install psycopg2 
import psycopg2.extras
 
app = Flask(__name__)
app.secret_key = "cairocoders-ednalan"
 
DB_HOST = "localhost"
DB_NAME = "sampledb"
DB_USER = "postgres"
DB_PASS = "123456"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
 
@app.route('/')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM todo"
    cur.execute(s) # Execute the SQL
    list_users = cur.fetchall()
    return render_template('index.html', list_users = list_users)
 
@app.route('/add_todo', methods=['POST'])
def add_todo():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        title = request.form['title']
        status = request.form['status']
        priorty = request.form['priorty']
        cur.execute("INSERT INTO todo (title, status, priorty) VALUES (%s,%s,%s)", (title, status, priorty))
        conn.commit()
        flash('Todo Added successfully')
        return redirect(url_for('Index'))
 
@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_employee(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('SELECT * FROM todo WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', todo = data[0])

@app.route('/search', methods = ['POST'])
def search():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        searchElement = request.form['searchElement']
        
        likeString = "'%" + searchElement + "%'"

        cur.execute("""SELECT * FROM todo WHERE title LIKE {0};""".format(likeString))
        list_users = cur.fetchall()
        #flash('Todo Added successfully')
        return render_template('index.html', list_users = list_users, searchElement = True)

@app.route('/done/<string:id>', methods = ['POST','GET'])
def done_todo(id):

    status="Done"
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("""
            UPDATE todo
            SET status = %s
            WHERE id = %s
        """, (status,id))
    conn.commit()
    flash('Todo Marked as Complete')
    return redirect(url_for('Index'))


@app.route('/update/<id>', methods=['POST'])
def update_todo(id):
    if request.method == 'POST':
        title = request.form['title']
        status = request.form['status']
        priorty = request.form['priorty']
         
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE todo
            SET title = %s,
                status = %s,
                priorty = %s
            WHERE id = %s
        """, (title, status, priorty, id))
        flash('Todo Updated Successfully')
        conn.commit()
        return redirect(url_for('Index'))
 
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_todo(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('DELETE FROM todo WHERE id = {0}'.format(id))
    conn.commit()
    flash('Todo Removed Successfully')
    return redirect(url_for('Index'))
 
if __name__ == "__main__":
    app.run(debug=True)
# </string:id></id></id>