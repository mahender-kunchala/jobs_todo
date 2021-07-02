from flask import render_template,request,redirect,url_for,Blueprint,g
from . import db

bp=Blueprint("jobs","jobs",url_prefix="/jobs")

@bp.route("/")
def alljobs():
    conn=db.get_db()
    cursor=conn.cursor()
    cursor.execute("select id, title,company_name from openings")
    jobs=cursor.fetchall()
    return render_template("jobs/jobslist.html",jobs=jobs)
@bp.route("/<jid>")
def jobdetails(jid):
    conn=db.get_db()
    cursor=conn.cursor()
    cursor.execute(f"select title,company_name,jd_text from openings where id = {jid};")
    title,company,info =cursor.fetchone()
    if int(jid)==1:
        prev=None
    else:
        prev=int(jid)-1
    nxt=int(jid)+1
    return render_template("jobs/jobdetails.html",info=info,nxt=nxt,prev=prev,title=title,company=company)
