from flask import Flask, render_template,request,redirect,url_for
import pymysql.cursors,os

application=Flask(__name__)

conn=cursor=None

#fungsi koneksi database
def openDb():
    global conn,cursor
    conn=pymysql.connect(host='localhost',user='root',password='',db='db_mahasiswa' )
    cursor=conn.cursor()

#fungsi koneksi database
def closeDb():
    global conn,cursor
    cursor.close()
    conn.close()

#fungsi view index() untuk menampilkan data dari database
@application.route('/')
def index():
    openDb()
    container = []
    sql = "SELECT * FROM mahasiswa"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
        container.append(data)
        closeDb()
    return render_template('index.html', container=container)

#fungsi view tambah() untuk membuat form tambah
@application.route('/tambah', methods=['GET','POST'])
def tambah():
    if request.method == 'POST':
        nim_mahasiswa = request.form['nim_mahasiswa']
        nama = request.form['nama']
        kelompok= request.form['kelompok']
        jurusan = request.form['jurusan']
        openDb()
        sql = "INSERT INTO mahasiswa (nim_mahasiswa, nama, kelompok,jurusan) VALUES (%s, %s, %s, %s)"
        val = (nim_mahasiswa,nama, kelompok, jurusan)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
        return redirect(url_for('index'))
    else:
        return render_template('tambah.html')

#fungsi view edit() untuk form edit
@application.route('/edit/<nim_mahasiswa>', methods=['GET','POST'])
def edit(nim_mahasiswa):
    openDb()
    cursor.execute('SELECT * FROM mahasiswa WHERE nim_mahasiswa=%s', (nim_mahasiswa))
    data = cursor.fetchone()
    if request.method == 'POST':
        nim_mahasiswa = request.form['nim_mahasiswa']
        nama = request.form['nama']
        kelompok = request.form['kelompok']
        jurusan = request.form['jurusan']
        sql = "UPDATE mahasiswa SET nim_mahasiswa=%s, nama=%s, kelompok=%s, jurusan=%s WHERE nim_mahasiswa=%s"
        val = (nim_mahasiswa,nama,kelompok,jurusan,nim_mahasiswa)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
        return redirect(url_for('index'))
    else:
        closeDb()
        return render_template('edit.html', data=data)

#fungsi untuk menghapus data
@application.route('/hapus/<nim_mahasiswa>', methods=['GET','POST'])
def hapus(nim_mahasiswa):
    openDb()
    cursor.execute('DELETE FROM mahasiswa WHERE nim_mahasiswa=%s', (nim_mahasiswa,))
    conn.commit()
    closeDb()
    return redirect(url_for('index'))
if __name__ == '__main__':
    application.run(debug=True)












