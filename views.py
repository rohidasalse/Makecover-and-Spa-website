
import os

from werkzeug.utils import secure_filename

import json

from flask import Flask, make_response,render_template,abort,session,redirect,send_file, request,flash,jsonify,Response,url_for

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect,text,func
import uuid
from io import BytesIO
# from flask_mail import Mail

from sqlalchemy.orm import load_only

from models import *


from __init__ import app,db
from helper import *


import json


from admin import admin_bp
app.register_blueprint(admin_bp, url_prefix='/xyz')





with open("config.json","r") as c:
    params=json.load(c)['params']
with open("config.json","r") as d:
    directories=json.load(d)['directories']    
with open("config.json","r") as s:
    social=json.load(s)['social']
    


@app.route("/",methods=['GET'])   
def home():
    main_title="Anvi Makeover & Spa | Home"
    home_slider=[custom_file for custom_file in Customize_files.query.filter_by( position="home-carousel").all()]
    return render_template("index.html" ,
                           main_title=main_title,
                           home_slider=home_slider,
                            show_footer=False,
                            no_header_img=True
                           )
    
    

@app.route("/bridal_makeup",methods=['GET'])   
def bridal_makeup():
    

    return render_template("bridal.html" ,
                             show_footer=True
                           )
@app.route("/facial_skin",methods=['GET'])   
def facial_skin():
    

    return render_template("facial.html" ,
                             show_footer=True
                           )
@app.route("/hair_spa",methods=['GET'])   
def hair_spa():
    

    return render_template("hair.html" ,
                             show_footer=True
                           )
    
@app.route("/haircur_haircolor",methods=['GET'])   
def haircur_haircolor():
    

    return render_template("hair-cut.html" ,
                             show_footer=True
                           )
    
@app.route("/bodyspa_dtan",methods=['GET'])   
def bodyspa_dtan():
    

    return render_template("body.html" ,
                             show_footer=True
                           )

@app.route("/menucure_pedicure",methods=['GET'])   
def menucure_pedicure():
    

    return render_template("manicure.html" ,
                             show_footer=True
                           )
@app.route("/keratin_smoothing",methods=['GET'])   
def keratin_smoothing():
    

    return render_template("keretin.html" ,
                             show_footer=True
                           )

    
@app.route("/services/*",methods=['GET'])   
def services():
    

    return render_template("services.html" ,
                             show_footer=True
                           )
    

@app.route("/photo-gallery",methods=['GET'])   
def photo_gallery():
     
    main_title="Anvi Makeover & Spa | Portfolio"
    photo_gallery=[custom_file for custom_file in Customize_files.query.filter_by( position="photo-gallery").all() ]
    return render_template("photogallery.html" ,
                           main_title=main_title,
                            photo_gallery= photo_gallery,
                             show_footer=True
                           )

@app.route("/testimonial",methods=['GET'])   
def testimonial():
    main_title="Anvi Makeover & Spa | Blog"

    return render_template("testimonial.html" ,
                           main_title=main_title,
                             show_footer=True
                           )
    
@app.route("/contact",methods=['GET'])   
def contact():
    main_title="Anvi Makeover & Spa | Contact"
    insta_posts=[custom_file for custom_file in Customize_files.query.filter_by( position="insta-posts").all() ]
    return render_template('contact.html' ,
                          main_title=main_title ,
                          insta_posts=insta_posts,
                            show_footer=True
                           )



@app.route('/about')
def about():
    main_title="Anvi Makeover & Spa | About Me"
    insta_posts=[custom_file for custom_file in Customize_files.query.filter_by( position="insta-posts").all() ]
    return render_template('about.html',
                           main_title=main_title,
                           insta_posts=insta_posts,
                           show_footer=True                       
  )



    


     


  



def process_list_field(field_value):
    if field_value:
        field_list = [item.strip() for item in field_value.split(',') if item.strip()]
        return field_list
    return []











@app.route('/api/files/<fileId>', methods=['GET'])
def get_file(fileId):
    file_entry = Files.query.get(fileId)

    if file_entry is None:
        return jsonify({"error": "File could not be found"}), 400
        # abort(404)

    try:
        return send_file(file_entry.filepath, mimetype=file_entry.fileType, as_attachment=False)
    except Exception as e:
        abort(500)



# @app.route('/api/files/<fileId>', methods=['GET'])
# def get_file_by_id(fileId):
#     try:
#         file_entry = Files.query.get(fileId)

#         if file_entry is None:
#             return jsonify({"error": "File could not be found"}), 400

#         return send_file(BytesIO(file_entry.fileData), mimetype=file_entry.fileType, as_attachment=False)
#     except Exception as e:
#         abort(500)


        
















#  **************************************ERRORS**********************************************

# handles error 400
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html',error=error), 404

# handles error 400
@app.route("/error")
def error():
    error=400
    return render_template('page_not_found.html',error=error), 404


# @app.context_processor
# def inject_optional_user():
    user= checkUser()
    if user:
        userId=user.userId
        user=Users.get_by_id(userId).toDictExceptPassword()
        if user:
            cart_count = Carts.query.filter_by(userId=userId).count()
            wishlist_count = Wishlist.query.filter_by(userId=userId).count()
            addresses=[address.toDict() for address in Addresses.query.filter_by(userId=userId).all()]
            
            return dict(params=params,social=social, user=user, addresses=addresses, cart_count=cart_count, wishlist_count=wishlist_count)
    user = None
    cart_count=None
    wishlist_count=None
    return dict(params=params, social=social,user=user, cart_count=cart_count, wishlist_count=wishlist_count)