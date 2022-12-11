#from flask import Flask,render_template,request
 
#app = Flask(__name__)
 
#@app.route('/data/', methods = ['POST', 'GET'])
#def data():
#    if request.method == 'GET':
#        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
#    if request.method == 'POST':
#        form_data = request.form
#        return render_template('data.html',form_data = form_data)
 
 
#app.run(host='localhost', port=5501)



#If you have the debugger disabled or trust the users on your network, you can make the server publicly available simply by adding 
#--host=0.0.0.0 to the command line:
#$ flask run --host=0.0.0.0

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home ():
	return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/alphademo')
def alphademo():
    return render_template('alphademo.html')

@app.route('/blog-home')
def blog_home():
    return render_template('blog-home.html')

@app.route('/blog-post')
def blog_post():
    return render_template('blog-post.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/scorecard')
def scorecard():
    return render_template('scorecard.html')

@app.route('/portfolio-item')
def portfolio_item():
    return render_template('portfolio-item.html')

@app.route('/portfolio-overview')
def portfolio_overview():
    return render_template('portfolio-overview.html')




if __name__ == "__main__":
    app.run()



