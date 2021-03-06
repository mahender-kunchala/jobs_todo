from flask import Flask,render_template
import random

def create_app():
    app=Flask("jobs")

    app.config.from_mapping(
        DATABASE="naukri"
        )

    from . import db
    db.init_app(app)

    from .import jobs
    app.register_blueprint(jobs.bp)
    @app.route("/")
    def main():
        conn=db.get_db()
        curs=conn.cursor()
        curs.execute("select count(*) from openings")
        count=curs.fetchone()[0]
        curs.execute("select crawled_on from crawl_status order by crawled_on desc limit 1")
        crawl_date=curs.fetchone()[0]
        quotes=[["love yourselves","mahi"],["never postpone","mahender"],["know your worth","jesus"]]
        quote, author = random.choice(quotes)

        #return render_template('index.html', quote=quote, author=author, count=count, date = crawl_date)
        return render_template('index.html',quote=quote,author=author,count=count)

    
    from . import crawler
    crawler.init_app(app)
    

    return app

