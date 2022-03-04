from flask import Flask, redirect, url_for, request, render_template
from cal import calculate_it
from create import create_img
from datetime import datetime
from create import apply_kmeans
from create import mask_superimpose
from create import enhance_image
from create import plot_superimpose
from create import count_greenPixels
from create import intensify_green
from create import trial

import os
app = Flask(__name__)

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/login',methods = ['POST'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      num  = request.form['num']
      return redirect(url_for('success',name = num))


@app.route('/blog/<int:result>')
def blog(result):
	return 'the result is %d' % result

# passing the data to cal.py and adding the numbers
@app.route('/add', methods = ['POST'])
def add():
	 num1 = int(request.form['n1'])
	 num2 = int(request.form['n2'])
	 res = calculate_it(num1, num2)
	 return redirect(url_for('blog', result = res))

picFolder = os.path.join('static', 'pics')
print(picFolder)
app.config['UPLOAD_FOLDER'] = picFolder

 
# to display image in html
@app.route('/index')
def index():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'mask.png')
    return render_template("index.html", user_image=pic1)   


## calling the function to create an inverted image
@app.route('/img')
def display_img():
	create_img()
	return 'img will be save in the spcfiic folder'

@app.route('/date_trial',methods = ['POST'])
def display_date():
	#d = datetime(request.form['date_field'])
	#a = d.strftime("%d-%m-%Y")
	date = request.form['nm']
	plot = request.form['num']
	#return 'the dat is displayed %s' % user
	enhance_image(date)
	apply_kmeans(date)
	intensify_green(date)
	mask_superimpose(date)
	plot_superimpose(date,plot)
	pixel_count = count_greenPixels(date)
	#trial()

	return redirect(url_for('success',name = pixel_count))

 
if __name__ == '__main__':
   app.run(debug = True)