import sys

from flask import Blueprint, jsonify, g, request, url_for
from flask.views import MethodView
from auth import login_required

manager = Blueprint('file_manager', __name__)

class ProjectView(MethodView):
    decorators = [login_required]

    def get(self):
        json_data = request.get_json()

    def post(self):
        json_data = request.get_json()

class UploadView(MethodView):
    decorators = [login_required]

    def post(self):
        if 'file' not in request.files:
            return jsonify({'errors': 'No file was provided.'}), 422
        # need client name, project name
        files = request.files['files']
        print("The length of the files are: ".format(len(files)), file=sys.stderr)
        print("The files are:\n\n".format(files), file=sys.stderr)
        


project_view = ProjectView.as_view('project')
file_view = UploadView.as_view('upload')
manager.add_url_rule('/upload', view_func=file_view, methods=['POST'])
manager.add_url_rule('/project', view_func=file_view, methods=['GET', 'POST'])