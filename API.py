from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    '<secret from service account>.json',
    scopes=['https://www.googleapis.com/auth/androidpublisher'])

service = build('androidpublisher', 'v2', http=credentials.authorize(Http()))

package_name = "<package name>"
reviews_resource = service.reviews()
reviews_page = reviews_resource.list(packageName=package_name, maxResults=100).execute()
reviews_list = reviews_page["reviews"]

infinite_loop_canary = 100
while "tokenPagination" in reviews_page:
    reviews_page = reviews_resource.list(packageName=package_name,
                               token=reviews_page["tokenPagination"]["nextPageToken"],
                               maxResults=100).execute()
    reviews_list.extend(reviews_page["reviews"])
    infinite_loop_canary -= 1
    if infinite_loop_canary < 0:
        break
