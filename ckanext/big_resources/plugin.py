import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.uploader import ResourceUpload as DefaultResourceUpload
import ckanext.big_resources.views as views
import os
import requests
from requests_toolbelt.multipart import encoder
from ckan.lib.uploader import _copy_file
import ckan.logic as logic
from ckan.common import g, request
from requests_toolbelt.multipart.encoder import (
    MultipartEncoder,
    MultipartEncoderMonitor,
)


class BigResourcesPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IUploader, inherit=True)
    plugins.implements(plugins.IBlueprint)

    def get_resource_uploader(self, data_dict):
        return ResourceUpload(data_dict)
    
    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'big_resources')
        
    # IBlueprint
        
    def get_blueprint(self):
        return views.get_blueprints()


class ResourceUpload(DefaultResourceUpload):

    def upload(self, id, max_size=10):
        '''Actually upload the file.

        :returns: ``'file uploaded'`` if a new file was successfully uploaded
            (whether it overwrote a previously uploaded file or not),
            ``'file deleted'`` if an existing uploaded file was deleted,
            or ``None`` if nothing changed
        :rtype: ``string`` or ``None``

        '''
        if not self.storage_path:
            return

        # Get directory and filepath on the system
        # where the file for this resource will be stored
        directory = self.get_directory(id)
        filepath = self.get_path(id)

        # If a filename has been provided (a file is being uploaded)
        # we write it to the filepath (and overwrite it if it already
        # exists). This way the uploaded file will always be stored
        # in the same location
        if self.filename:
            try:
                os.makedirs(directory)
            except OSError as e:
                # errno 17 is file already exists
                if e.errno != 17:
                    raise
            tmp_filepath = filepath + '~'
            with open(tmp_filepath, 'wb+') as output_file:
                try:
                    _copy_file(self.upload_file, output_file, max_size)
                except logic.ValidationError:
                    os.remove(tmp_filepath)
                    raise
                finally:
                    self.upload_file.close()
            os.rename(tmp_filepath, filepath)
            return

        # The resource form only sets self.clear (via the input clear_upload)
        # to True when an uploaded file is not replaced by another uploaded
        # file, only if it is replaced by a link to file.
        # If the uploaded file is replaced by a link, we should remove the
        # previously uploaded file to clean up the file system.
        if self.clear:
            try:
                os.remove(filepath)
            except OSError as e:
                pass
        
    