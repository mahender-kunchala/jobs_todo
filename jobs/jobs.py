from flask import render_template,request,redirect,url_for,Blueprint,g
from . import db

bp=Blueprint("jobs","jobs",url_prefix="/jobs")

@bp.route("/")
def alljobs():
    conn=db.get_db()
    cursor=conn.cursor()
    cursor.execute("select o.id,o.title,o.company_name,s.name from openings o,job_status s where s.id=o.status order by s.name")
    jobs=cursor.fetchall()
    cursor.execute(
        "select crawled_on from crawl_status order by crawled_on desc limit 1");
    crawl_date=cursor.fetchone()[0]
    
    return render_template("jobs/jobslist.html",jobs=jobs,count=len(jobs),date=crawl_date)


@bp.route("/<jid>")
def jobdetails(jid):
    conn=db.get_db()
    cursor=conn.cursor()
    cursor.execute("select o.title, o.company_name, s.name, o.jd_text, o.crawled_on from openings o, job_status s where o.id = %s and s.id = o.status", (jid,))
    job=cursor.fetchone()
    if not job:
        return render_template("job/jobdetails.html"),404
    title,company,status,info,crawled_on=job
    jid=int(jid)
    
        
    if (jid)==1:
        prev=None
    else:
        prev=jid-1
    nxt=jid+1
    classes = {"crawled": "primary",
               "applied" : "secondary",
               "ignored" : "dark",
               "selected" : "success",
               "rejected" : "danger"}

    return render_template("jobs/jobdetails.html", 
                           jid = jid,
                           info = info, 
                           nxt=nxt, 
                           prev=prev, 
                           title = title, 
                           company=company, 
                           status=status, 
                           cls=classes[status], 
                           crawled_on=crawled_on)




@bp.route("/<jid>/edit",methods=["GET","POST",])

def edit_job(jid):
    conn=db.get_db()
    cursor=conn.cursor()
    cursor.execute("select o.title, o.company_name, s.name, o.jd_text, o.crawled_on from openings o, job_status s where o.id = %s and s.id = o.status", (jid,))
    job=cursor.fetchone()
    if not job:
        return render_template("jobs/jobdetails.html"),404

    if request.method=="GET":
        title,company_name,status,jd,crawled_on=job
        cursor.execute("select id,name from job_status")
        statuses = cursor.fetchall()
        return render_template("jobs/jobedit.html", 
                               jid = jid,
                               info=jd,
                               statuses = statuses,
                               status = status,
                               title = title, 
                               crawled_on = crawled_on)
    elif request.method == "POST":
        status = request.form.get("status")
        jd = request.form.get("jd")
        cursor.execute("update openings set jd_text = %s, status=%s where id=%s", (jd, status, jid))
        conn.commit()
        return redirect(url_for("jobs.jobdetails", jid=jid), 302)

    
