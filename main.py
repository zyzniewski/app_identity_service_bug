import datetime

from google.appengine.api import app_identity
import google.cloud.storage

import webapp2

storage = google.cloud.storage.Client()
bucket = storage.bucket(
    '{}.appspot.com'.format(
        app_identity.get_application_id(),
    ),
)


class MainHandler(webapp2.RequestHandler):

    def get(self):

        token, ttl = app_identity.get_access_token_uncached(
            (
                'https://www.googleapis.com/auth/devstorage.full_control',
                'https://www.googleapis.com/auth/devstorage.read_only',
                'https://www.googleapis.com/auth/devstorage.read_write',
            ),
        )

        blob = bucket.blob('NotAllowed')
        blob.upload_from_string(
            '123',
            content_type='image/jpeg',
        )

        self.response.json = {
            'token': token,
            'ttl': ttl,
            'url': blob.generate_signed_url(datetime.timedelta(minutes=1)),
        }


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
])
