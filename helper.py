from __init__ import app,db
import os
import time
import random
import uuid
from flask import request, jsonify
from werkzeug.utils import secure_filename
from urllib.parse import urlparse

import tempfile
import os
import io
import inspect

from flask import session,request,jsonify,make_response,g,redirect,url_for
from models import *

from functools import wraps,update_wrapper
from  datetime import datetime,timedelta
from functools import wraps
from flask import request, jsonify
import os,csv

def compress_image(image_file, max_size=(None,None), quality=50, target_size_kb=256):
    """
    Compresses an image file by resizing and reducing quality.

    Args:
        image_file (str): The path to the image file.
        max_size (tuple, optional): The maximum size (width, height) allowed for the image. Default is (256, 256).
        quality (int, optional): The image quality to use for compression (0-100). Default is 80.
        target_size_kb (int, optional): The target file size in kilobytes. Default is 256.

    Returns:
        bytes: The compressed image data as a byte array.
    """
    # Open the image file
    image = Image.open(image_file)

    # Resize the image if necessary
    # Resize the image if necessary
    if max_size[0] is not None and max_size[1] is not None:
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size)



    # Set the initial quality range
    quality_lower = 0
    quality_upper = 100

    # Perform binary search to find the optimal quality level
    while quality_lower < quality_upper:
        quality = (quality_lower + quality_upper) // 2
        print(quality)
        # Create a byte array to store the compressed image
        output_buffer = io.BytesIO()

        # Save the image with the current quality level to the byte array
        image.save(output_buffer, format=image.format, optimize=True, quality=quality)

        # Get the byte array data and check the file size
        compressed_data = output_buffer.getvalue()
        file_size_kb = len(compressed_data) / 1024

        if file_size_kb <= target_size_kb:
            # Decrease the upper bound for quality range
            quality_upper = quality
        else:
            # Increase the lower bound for quality range
            quality_lower = quality + 1

        # Reset the byte array for the next compression iteration
        output_buffer.seek(0)
        output_buffer.truncate()

    # Perform one more compression iteration with the final quality level
    image.save(output_buffer, format=image.format, optimize=True, quality=quality_lower)
    compressed_data = output_buffer.getvalue()

    return compressed_data

def save_file(file, upload_path, file_type, compress=True):
    allowed_extensions = get_allowed_extensions(file_type)

    if file and file.filename != '':
        # Validate file extension
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return None, allowed_extensions, None

        # Generate a secure filename
        original_filename = secure_filename(file.filename)
        base_filename, file_extension = os.path.splitext(original_filename)
        timestamp = str(int(time.time()))  # Append timestamp
        random_string = str(random.randint(1, 999999))  # Append random string
        unique_filename = f"Image_{str(uuid.uuid4())}_{timestamp}_{random_string}{file_extension}"

        # Generate the file path
        file_path = os.path.join(upload_path, unique_filename)
        print(file_path)

        # Create the directories if they don't exist
        os.makedirs(upload_path, exist_ok=True)

        # if compress:
        #     # Compress the image
        #     compressed_data = compress_image(file, max_size=(1024, 1024), quality=80)

        #     if compressed_data is None:
        #         return None, allowed_extensions, None

        #     # Save the compressed image data to the file path
        #     with open(file_path, 'wb') as output_file:
        #         output_file.write(compressed_data)

        #     # Return the saved file path, allowed extensions, and the file
        #     return file_path, allowed_extensions, file
        
        # Save the file
        file.save(file_path)
        
        # Return the saved file path, allowed extensions, and the file
        return file_path, allowed_extensions, file

    return None, allowed_extensions, None

def store_image_data(image_data, image_type,customizeId,is_image_binary=False):
    # try:
        # Debugging: Print the value of image_data
        # print(f"Image Data: {image_data}")
    if is_image_binary:
        image_binary =image_data
        
    else:
        
        
        # Split the image_data and retrieve the base64-encoded part
        image_parts = image_data.split(',')
        # if len(image_parts) < 2:
        #     raise ValueError("Invalid image data format")

        image_binary = base64.b64decode(image_parts[-1])
    
    # Create a unique file ID (you can use your existing logic)
    file_id = str(uuid.uuid4())
    
    # Specify the file URL based on the file ID
    file_url = f"/api/files/{file_id}"
    
    # Create an instance of the Files model
    new_file = Files(fileId=file_id, fileData=image_binary, fileUrl=file_url,customizeId=customizeId, fileType=image_type)
    
    # Add the new image data to the database
    db.session.add(new_file)
    db.session.commit()
    
    return file_id, file_url,new_file
    # except Exception as e:
    #     print(f"Error storing image data: {str(e)}")
    #     return None, None


def save_file_path_to_db(file_path, file_type,):
    # Save the file path and file type to the database
    fileId = str(uuid.uuid4())
    domain,port = request.host.split(':')[0],request.host.split(':')[1]

    # Generate the file URL based on the fileId and the domain
    
    # file_url = f"http://{domain}:{port}/api/files/{fileId}"
    
    file_url = f"/api/files/{fileId}"

    
    # # Generate the file URL based on the fileId
    # file_url = f"http://127.0.0.1:5000/api/files/{fileId}"

    # Create a new instance of the Files model
    new_file = Files(fileId=fileId,fileType=file_type, filepath=file_path, fileUrl=file_url)

    # Add the new file to the database
    db.session.add(new_file)
    db.session.commit()

    # Return the file URL
    return file_url,fileId

def get_allowed_extensions(file_type):
    allowed_extensions = set()

    if file_type == 'image':
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif','webp'}
    elif file_type == 'document':
        allowed_extensions = {'doc', 'docx', 'pdf', 'txt'}
    elif file_type == 'video':
        allowed_extensions = {'mp4', 'mov', 'avi', 'mkv'}
    # Add more file types and their corresponding allowed extensions as needed
    elif file_type == 'audio':
        allowed_extensions = {'mp3', 'wav', 'ogg'}

    return allowed_extensions

def delete_file_from_storage(file_url):
    if file_url:
        file=Files.query.filter_by(fileUrl=file_url).first()
        if file:
            # Get the absolute file path
            abs_file_path = os.path.abspath(file.filepath)
            
            try:
                # Delete the file if it exists
                if os.path.exists(abs_file_path):
                    os.remove(abs_file_path)
            except:
                print("File path doesnt exists")
                
            db.session.delete(file)
            
                





def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return make_response(jsonify({'error': 'Admin access denied'}), 401)
        try:
            # Verify and decode the JWT
            payload = jwt.decode(token, app.secret_key, algorithms=["HS256"])
            email = payload["email"]
            adminId = payload["adminId"]
            username=payload["username"]

            # Find the user by email
            admin = Admin.query.filter_by(adminId=adminId,email=email,username=username).first()

            
            if not admin:
                return make_response(jsonify({'error': 'Admin access denied'}), 401)

            # Attach the admin object to the request context
            request.admin = admin

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated_function


def utc_to_ist(utc_date):
        ist_offset = timedelta(hours=5, minutes=30)
        ist_date = utc_date + ist_offset
        ist_date = ist_date.strftime('%Y-%m-%d %H:%M:%S')
        return ist_date
    

class AuthenticationRequired(Exception):
    pass

class InvalidUserEmail(Exception):
    pass

class TokenExpired(Exception):
    pass

class InvalidToken(Exception):
    pass


# def checkUser():
#     token = session.get("token")
#     if not token:
#         raise AuthenticationRequired("Authentication required")

#     try:
#         # Verify and decode the JWT
#         payload = jwt.decode(token, app.secret_key, algorithms=["HS256"])
#         email = payload["email"]
        
#         # Find the user by email
#         user = Users.query.filter_by(email=email).first()
#         if not user:
#             raise InvalidUserEmail("Unauthorized")
#         return user

#     except jwt.ExpiredSignatureError:
#         raise TokenExpired("Token expired")
#     except jwt.InvalidTokenError:
#         raise InvalidToken("Invalid token")



def process_list_field(field_value):
    if field_value:
        field_list = [item.strip() for item in field_value.split(',') if item.strip()]
        return field_list
    return []

