import flask
from flask import Blueprint, Response, stream_with_context
import ckan.model as model
import ckan.lib.helpers as h
import ckan.lib.uploader as uploader
import ckan.lib.base as base
import ckan.logic as logic
from ckan.common import _, g
from ckan.plugins import toolkit as tk

big_resources = Blueprint("big_resources", __name__)
get_action = logic.get_action
NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized

CHUNK_SIZE = int(tk.config.get('ckanext.big_resources.chunk_download', 2048))


@big_resources.route("/dataset/<id>/resource/<resource_id>/download")
@big_resources.route("/dataset/<id>/resource/<resource_id>/download/<filename>")
def download(id, resource_id, filename=None, package_type='dataset'):
    """
    Provides a direct download by either redirecting the user to the url
    stored or downloading an uploaded file directly.
    """
    context = {
        u'model': model,
        u'session': model.Session,
        u'user': g.user,
        u'auth_user_obj': g.userobj
    }

    try:
        rsc = get_action(u'resource_show')(context, {u'id': resource_id})
        get_action(u'package_show')(context, {u'id': id})
    except NotFound:
        return base.abort(404, _(u'Resource not found'))
    except NotAuthorized:
        return base.abort(403, _(u'Not authorized to download resource'))

    if rsc.get(u'url_type') == u'upload':
        upload = uploader.get_resource_uploader(rsc)
        
        ########################################
        # rewrite download function from resource.py
        def streaming_response(
                data, mimetype=u'application/octet-stream', with_context=False):
            iter_data = iter(data)

            if with_context:
                iter_data = flask.stream_with_context(iter_data)
            resp = flask.Response(iter_data, mimetype=mimetype)

            return resp

        def stream_file(f_path):
            u'''File stream. Just do not close it until response finished'''

            def gen():
                with open(f_path, 'rb') as fd:
                    while 1:
                        buf = fd.read(CHUNK_SIZE)
                        if buf:
                            yield buf
                        else:
                            break

            return streaming_response(gen())
        
        filepath = upload.get_path(rsc[u'id'])

        
        ##########################################
    elif u'url' not in rsc:
        return base.abort(404, _(u'No download is available'))
    return stream_file(filepath)


def get_blueprints():
    return [big_resources]
