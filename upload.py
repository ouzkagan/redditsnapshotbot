#!/usr/bin/env python3

'''
	Here's how you upload an image. For this example, put the cutest picture
	of a kitten you can find in this script's folder and name it 'Kitten.jpg'
	For more details about images and the API see here:
		https://api.imgur.com/endpoints/image
'''

# Pull authentication from the auth example (see auth.py)
from auth import authenticate

from datetime import datetime

album = None # You can also enter an album ID here
#image_path = 'out.jpg'

def uploadsnapshot(image_path, post_title, post_id, comment_id, comment_url,album):
	client = authenticate()

	'''
		Upload a picture of a kitten. We don't ship one, so get creative!
	'''

	# Here's the metadata for the upload. All of these are optional, including
	# this config dict itself.
	imagename = f"RedditSnapshotBot Post { post_id } - comment { comment_id } - { format(datetime.now()) }"

	config = {
		'Album':album,
		'name': imagename,
		'title': f"{post_title} - redditsnapshotbot",
		'description': f'This image uploaded via u/redditsnapshotterbot'
	}

	print("Uploading image... ")
	image = client.upload_from_path(image_path, config=config, anon=False)
	print("Done")

	return image['link']


# If you want to run this as a standalone script
if __name__ == "__main__":

	print("Image was posted! Go check your images you sexy beast!")
