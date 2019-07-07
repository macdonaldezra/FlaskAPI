import sys

from flask import Blueprint, jsonify, g, request, url_for
from flask.views import MethodView
from auth import login_required

file_manager = Blueprint('file_manager', __name__)

class Upload(MethodView):
    # decorators = [login_required]

    def post(self):
        if 'file' not in request.files:
            return jsonify({'errors': 'No file was provided.'}), 422
        files = request.files['files']
        print("The length of the files are: ".format(len(files)), file=sys.stderr)
        print("The files are:\n\n".format(files), file=sys.stderr)

file_view = Upload.as_view('upload')
file_manager.add_url_rule('/upload', view_func=file_view, methods=['POST'])