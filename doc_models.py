from uuid import uuid4
from werkzeug.utils import secure_filename
from flask import current_app
from azure.storage.blob import BlockBlobService

ALLOWED_EXTENSIONS = set(['fnt', 'fon', 'otf', 'ttf', 'ai', 'bmp', 'gif', 'ico', 
    'jpeg', 'jpg', 'png', 'ps', 'psd', 'svg', 'tif', 'tiff', 'css', 'key', 'odp', 'pps', 'ppt', 
    'pptx', 'ods', 'xlr', 'xls', 'xlsx', '3g2', '3gp', 'avi', 'flv', 'h264', 'm4v',
    'mkv', 'mov', 'mp4', 'mpg', 'mpeg', 'rm', 'swf', 'vob', 'wmv', 'doc', 'docx', 'odt',
    'pdf', 'rtf', 'tex', 'txt', 'wks', 'wps', 'wpd', 'csv', 'dat', 'log', 'xml', 'json',
    'aif', 'cda', 'mid', 'midi', 'mp3', 'mpa', 'ogg', 'wav', 'wma', 'wpl'])

ACCT_NAME = current_app.config['BLOB_ACCOUNT_NAME']
ACCT_KEY = current_app.config['BLOB_ACCOUNT_KEY']
CONTAINER_NAME = current_app.config['BLOB_CONTAINER_NAME']

block_blob_service = BlockBlobService(account_name=ACCT_NAME, account_key=ACCT_KEY)


class File:
    def __init__(self, filename: str, username: str, client: str, project: string):
        self.file_id = uuid4()
        self.filename = filename
        self.file_extension = self.file_extension()
        self.username = username
        self.client = client
        self.project = project
    
    def file_extension(self):
        return self.filename.rsplit('.', 1)[1]

    def allowed_files(self):
        """Returns True if file is in list ALLOWED_EXTENSIONS, False, otherwise"""
        return '.' in self.filename and self.filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    def validate_filename(self) -> bool:
        if secure_filename(self.filename) and self.allowed_files():
            self.filename = secure_filename(self.filename)
            return True
        return False

    def file_metadata(self):



def upload_files(files, user, project, client):
    if isinstance(files, str):
        if secure_filename(files) and allowed_files(files):
            filename = secure_filename(files)
            meta_data = {'username': user, 'client': client, 'project_name': project}
            name = uuid4()
            block_blob_service.create_blob_from_stream(files, name, filename, metadata=meta_data)
            # Upload to BlobStorage
    elif isinstance(files, list):
        for file in files:
            if secure_filename(file) and allowed_files(file):
                filename = secure_filename(file)
                # Upload file to BlobStorage
