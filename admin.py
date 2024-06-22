from flask import Blueprint, render_template, request, jsonify
from models import Customize_files
from __init__ import db
from helper import *


admin_bp = Blueprint('admin', __name__, url_prefix='/xyz')

@admin_bp.route('/')
def admin_home():
    return redirect(url_for("admin.admin_uploads"))
    return render_template("Admin/home.html")

@admin_bp.route('/admin-uploads')
def admin_uploads():
    upload_type = request.args.get('upload_type')
   
    home_carousel_data_list = [custom_file for custom_file in Customize_files.query.filter_by( position="home-carousel").all() ]
    photo_gallery_data_list=[custom_file for custom_file in Customize_files.query.filter_by( position="photo-gallery").all() ]
    insta_posts_data_list=[custom_file for custom_file in Customize_files.query.filter_by( position="insta-posts").all() ]
    return render_template("Admin/uploads-files.html",
                           home_carousel_data_list=home_carousel_data_list,
                           photo_gallery_data_list=    photo_gallery_data_list,
                         insta_posts_data_list=insta_posts_data_list,
                           
                           )

@admin_bp.route('/custom_files', methods=['GET'])
def get_all_custom_files():
    custom_files = Customize_files.query.all()
    custom_files_list = [custom_file.toDict() for custom_file in custom_files]
    return jsonify(custom_files_list)

@admin_bp.route('/custom_files/<customizeId>', methods=['GET'])
def get_custom_file_by_id(customizeId):
    custom_file = Customize_files.query.get(customizeId)
    if custom_file:
        return jsonify(custom_file.toDict())
    return jsonify({'message': 'Custom file not found'}), 404

@admin_bp.route('/custom_files/<customizeId>', methods=['DELETE'])
def delete_custom_file(customizeId):
    custom_file = Customize_files.query.get(customizeId)
    if custom_file:
        
        try:
            delete_file_from_storage(custom_file.fileUrl)
        except:
            pass
        db.session.delete(custom_file)
        db.session.commit()
        return jsonify({'message': 'Custom file deleted successfully'})
    return jsonify({'message': 'Custom file not found'}), 404

@admin_bp.route('/custom_files/<customizeId>', methods=['PUT'])
def update_custom_file(customizeId):
    data = request.json
    custom_file = Customize_files.query.get(customizeId)
    if custom_file:
     
        custom_file.position = data['position']
        custom_file.index = data['index']
        custom_file.title = data['title']
        custom_file.category = data['category']
        custom_file.fileId = data['fileId']
        custom_file.link = data['link']
        db.session.commit()
        return jsonify({'message': 'Custom file updated successfully'})
    return jsonify({'message': 'Custom file not found'}), 404


@admin_bp.route('/custom_files', methods=['POST'])
def create_custom_file():
    data = request.form  # Use request.form to access form data

    position = data.get('position')
    index = data.get('index')
    title = data.get('title')
    category = data.get('category')
      # Changed to match the form field name
    link = data.get('url')  # Changed to match the form field name
    upload_path = f"files/img/{position}/{category}"
    # Handle file upload if needed (assuming the file_input field name)
    uploaded_file = request.files['file_input']
    customizeId=uuid.uuid4()
    if uploaded_file:
        # Handle the file, e.g., save it to a folder and store the file path
        
        file_path, allowed_extensions, tshirt_file =  save_file(uploaded_file, upload_path, 'image')
        if file_path is None:
             return make_response(jsonify({'error': 'Invalid image file'}), 400)
         
        file_url,fileId=save_file_path_to_db(file_path, 'image')
        new_custom_file = Customize_files(
                            customizeId=customizeId,
                          
                            position=position,
                            index=index,
                            title=title,
                            category=category,
                            fileUrl=file_url,
                            link=link
                            )
        db.session.add(new_custom_file)
        db.session.commit()
        return jsonify({'message': 'Custom file created successfully'}), 201
        
   
    return make_response(jsonify({'error': 'Error occured'}), 400)

    # Create a new Customize_files instance and add it to the database
    

    
