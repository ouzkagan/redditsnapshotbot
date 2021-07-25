import praw
import time
from datetime import datetime

import json
import imgkit
import pprint
from helpers import get_config

config = get_config()
config.read('auth.ini')
client_id = config.get('bot', 'client_id')
client_secret=config.get('bot', 'client_secret')
username=config.get('bot', 'username')
password=config.get('bot', 'password')
user_agent=config.get('bot', 'user_agent')

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    username=username,
    password=password,
    user_agent=user_agent,
)

param = 2
def get_price(award):
    return award.get('coin_price')
def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.0f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

def generateImage(HTML, pagewidth):
	options = {
	   'crop-w': pagewidth,
	}
	css = ['commentstyle.css']
	imgkit.from_string(HTML, 'out.jpg', options,css=css)

def getCommentHtml(call, index):
	#dir(object)
	comment = call
	usericon = comment.author.icon_img
	username = comment.author
	isop = ''
	if comment.is_submitter == True:
		isop = """<span class="isop">OP</span>"""

	datec = datetime.fromtimestamp(comment.created_utc)
	isedited = comment.edited
	edited = ""
	if isedited:
		edited = """<i class="isedited"> - edited %s</i>"""%(datetime.fromtimestamp(isedited))
	json_object = json.dumps(comment.all_awardings, indent = 4)  
	#print(json_object)
	
	awardcount = 0
	awardcount2 = 0
	awardings = comment.all_awardings 
	awardings.sort(key=get_price, reverse=True)
	moreAwardsHTML = ""
	awardsHTML = ""
	if len(awardings) > 0:
		iterator = 0
		for i in awardings:
			awardcount = awardcount + i['count']
			#print( i['coin_price'], i['resized_icons'][1]['url'], i['count'], end='\n\n')
			if iterator < 3:
				awardcount2 = awardcount2 + i['count']
				awardtemplate = """
					<span class="award" >
		              <img
		                alt="award-name"
		                src="%s"
		              />
		              <span class="awardcount">%s</span>
		            </span>
				"""%(i['resized_icons'][1]['url'], i['count'])
				awardsHTML = awardsHTML + awardtemplate
			iterator = iterator + 1
	
	if awardcount != awardcount2:
		moreAwardsHTML = """
			<i class="moreawards">& %s more</i>
		"""%(awardcount)
	#print('Total Award => ', awardcount)
	body = comment.body_html
	score = human_format(comment.score)

	
	commentTemplate = """
		<div class="comment">
		  <div class="block-comment" style="padding-left:%spx">
		    <div class="comment-user-info">
		      <div class="comment-user-img">
		        <img src="%s" alt="" />
		      </div>
		      <span class="username">%s</span>
		      %s
		      <span class="date"> - %s</span>
		      %s
		      <div class="awards">
		        %s
		        %s
		      </div>
		    </div>
		    <div class="comment-content">
		      %s
		      <div class="comment-bottom">
		        <div class="vote-arrows">
		          <button>
		              <!-- Generated by IcoMoon.io -->
		              <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
		                <title></title>
		                <g id="icomoon-ignore">
		                </g>
		                <path d="M665.6 979.2h-307.2c-31.788-0.058-57.542-25.812-57.6-57.594v-352.62h-192.051c-0.003 0-0.006 0-0.009 0-31.812 0-57.6-25.788-57.6-57.6 0-14.851 5.62-28.389 14.85-38.604l-0.045 0.050 403.302-447.59c10.83-11.18 25.981-18.12 42.752-18.12s31.922 6.94 42.737 18.104l0.015 0.016 403.405 447.693c9.213 10.171 14.852 23.73 14.852 38.605 0 31.777-25.732 57.544-57.496 57.6l-192.313 0.41v352.051c-0.058 31.788-25.812 57.542-57.594 57.6h-0.006zM364.8 915.2h294.4v-409.6l241.869-0.512-389.069-431.667-389.12 431.565h241.92zM516.71 68.147v0z"></path>
		            </span>
		          </button>
		          <div class="votecount">%s</div>
		          <button>
		              <!-- Generated by IcoMoon.io -->
		              <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
		                <title></title>
		                <g id="icomoon-ignore1">
		                </g>
		                <path d="M512 1017.754c-0.008 0-0.017 0-0.026 0-16.929 0-32.151-7.31-42.682-18.946l-0.044-0.049-403.405-447.693c-9.213-10.171-14.852-23.73-14.852-38.605 0-31.777 25.732-57.544 57.496-57.6l192.313-0.41v-352.051c0.058-31.788 25.812-57.542 57.594-57.6h307.206c31.788 0.058 57.542 25.812 57.6 57.594v352.62h192.051c0.003 0 0.006 0 0.009 0 31.812 0 57.6 25.788 57.6 57.6 0 14.851-5.62 28.389-14.85 38.604l0.045-0.050-403.302 447.59c-10.574 11.685-25.796 18.995-42.726 18.995-0.009 0-0.019 0-0.028 0h0.001zM507.29 955.802v0zM122.88 518.861l389.12 431.718 389.12-431.565h-241.92v-410.214h-294.4v409.6z"></path>
		              </svg>
		          </button>
		        </div>
		      </div>
		    </div>
		  </div>
		</div>
	"""%((index + 1)* 21, usericon,username,isop,datec,edited,awardsHTML,moreAwardsHTML, body,score)
	return commentTemplate


def getSubmissionHtml(submission):
	# print(submission.title)
	# print(submission.selftext == "")
	# if submission.selftext != "":
	# 	print(submission.selftext_html)
	# else:
	# 	print(submission.preview['images'][0]['resolutions'][3]['url'])
	# print(submission.score)
	# print(submission.all_awardings)
	# print(submission.num_comments)
	sr = submission.subreddit
	sr_image = sr.icon_img
	sr_name = sr.display_name
	poster = submission.author

	datec = datetime.fromtimestamp(submission.created_utc)
	isedited = submission.edited
	edited = ""
	if isedited:
		edited = """<i class="isedited"> - edited %s</i>"""%(datetime.fromtimestamp(isedited))


	#awards
	awardcount = 0
	awardcount2 = 0
	awardings = submission.all_awardings 
	awardings.sort(key=get_price, reverse=True)
	moreAwardsHTML = ""
	awardsHTML = ""
	if len(awardings) > 0:
		iterator = 0
		for i in awardings:
			awardcount = awardcount + i['count']
			#print( i['coin_price'], i['resized_icons'][1]['url'], i['count'], end='\n\n')
			if iterator < 3:
				awardcount2 = awardcount2 + i['count']
				awardtemplate = """
					<span class="award" >
		              <img
		                alt="award-name"
		                src="%s"
		              />
		              <span class="awardcount">%s</span>
		            </span>
				"""%(i['resized_icons'][1]['url'], i['count'])
				awardsHTML = awardsHTML + awardtemplate
			iterator = iterator + 1
	
	if awardcount != awardcount2:
		moreAwardsHTML = """
			<i class="moreawards">& %s more</i>
		"""%(awardcount)

	post_title = submission.title
	post_content = ""
	if submission.selftext != "":
		post_content = submission.selftext_html
	else:
		post_content = """
			<img class="post-img" src="%s">
		"""%(submission.preview['images'][0]['resolutions'][3]['url'])

	score = human_format(submission.score)
	comments_count = submission.num_comments
	
	submissionTemplate = """
		<div class="comment post">
		  <div class="block-comment">
		    <div class="comment-user-info post-user-info">
		      <div class="comment-user-img">
		        <img src="%s" alt="" />
		      </div>
		      <span class="subreddit-name">r/%s</span>
		      <span class="date">Posted by u/%s</span>
		      <span class="date"> - %s</span>
		      %s
		      <div class="awards">
		          %s
					%s		        
		      </div>
		    </div>
		    <div class="comment-content">
		      <div class="post-title">
		          <h1>%s</h1>
		      </div>
		      <div class="post-content-container">
		        %s
		      </div>
		      <div class="comment-bottom" style="padding:8px 4px 8px 0">
		        <div class="vote-arrows">
		          <button>
		            <!-- Generated by IcoMoon.io -->
		            <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
		              <title></title>
		              <g id="icomoon-ignore"></g>
		              <path d="M665.6 979.2h-307.2c-31.788-0.058-57.542-25.812-57.6-57.594v-352.62h-192.051c-0.003 0-0.006 0-0.009 0-31.812 0-57.6-25.788-57.6-57.6 0-14.851 5.62-28.389 14.85-38.604l-0.045 0.050 403.302-447.59c10.83-11.18 25.981-18.12 42.752-18.12s31.922 6.94 42.737 18.104l0.015 0.016 403.405 447.693c9.213 10.171 14.852 23.73 14.852 38.605 0 31.777-25.732 57.544-57.496 57.6l-192.313 0.41v352.051c-0.058 31.788-25.812 57.542-57.594 57.6h-0.006zM364.8 915.2h294.4v-409.6l241.869-0.512-389.069-431.667-389.12 431.565h241.92zM516.71 68.147v0z"></path>
		              </svg>
		          </button>
		          <div class="votecount">%s</div>
		          <button>
		            <!-- Generated by IcoMoon.io -->
		            <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
		              <title></title>
		              <g id="icomoon-ignore1"></g>
		              <path d="M512 1017.754c-0.008 0-0.017 0-0.026 0-16.929 0-32.151-7.31-42.682-18.946l-0.044-0.049-403.405-447.693c-9.213-10.171-14.852-23.73-14.852-38.605 0-31.777 25.732-57.544 57.496-57.6l192.313-0.41v-352.051c0.058-31.788 25.812-57.542 57.594-57.6h307.206c31.788 0.058 57.542 25.812 57.6 57.594v352.62h192.051c0.003 0 0.006 0 0.009 0 31.812 0 57.6 25.788 57.6 57.6 0 14.851-5.62 28.389-14.85 38.604l0.045-0.050-403.302 447.59c-10.574 11.685-25.796 18.995-42.726 18.995-0.009 0-0.019 0-0.028 0h0.001zM507.29 955.802v0zM122.88 518.861l389.12 431.718 389.12-431.565h-241.92v-410.214h-294.4v409.6z"></path>
		            </svg>
		          </button>
		        </div>
		        <div class="vote-arrows" style="margin-left:20px;">
		          <button>
		            <!-- Generated by IcoMoon.io -->
		            <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
		              <title></title>
		              <g id="icomoon-ignore"></g>
		              <path d="M389.12 1024c-20.479-0.029-37.069-16.637-37.069-37.12v0-161.28h-121.651c-102.457-0.116-185.484-83.143-185.6-185.589v-409.611c0.116-102.457 83.143-185.484 185.589-185.6h563.211c102.457 0.116 185.484 83.143 185.6 185.589v409.611c-0.116 102.457-83.143 185.484-185.589 185.6h-167.026l-212.787 189.133c-6.548 5.755-15.191 9.267-24.654 9.267-0.009 0-0.017 0-0.026 0h0.001zM230.4 108.8c-67.134 0.058-121.542 54.466-121.6 121.594v409.606c0.058 67.134 54.466 121.542 121.594 121.6h185.606v165.53l186.214-165.53h191.386c67.134-0.058 121.542-54.466 121.6-121.594v-409.606c-0.058-67.134-54.466-121.542-121.594-121.6h-0.006z"></path>
		            </svg>
		          </button>
		          <div class="votecount">%s</div>
		        </div>
		      </div>
		      <hr />
		    </div>
		  </div>
		</div>
	"""%(sr_image, sr_name, poster, datec, edited, awardsHTML, moreAwardsHTML, post_title, post_content, score, comments_count)

	return submissionTemplate
#to generate reply for different kind of requests in the future
def generateReply(link1, link2):
	template = """
	Hi, here is your snapshot: \n
	[Parent comment](%s)\n
	[Upper comments with post](%s)\n

	<sub>Still in Beta  - *[github link to contribute](https://github.com/ouzkagan/redditsnapshotbot)*</sub>
	"""%(link1, link2)
	return template
def commentsnapbot():
	keywords = ['!snapshot','!snapshotbot','!commentsnapshot','!commentsnapshotbot']
	params = ['all', 'top']
	print("started")
	count = 0

	# comment = reddit.comment("h6cnx2s")
	# HTML = getCommentHtml(comment,0)
	# totalcomment = 1
	# commentindex = 0
	# commentwidth = 600
	# pagewidth = commentwidth + (totalcomment*21*2) + 40


	'''
		To include submission => "selftext" ?= "preview['images']['resolutions'][3].url" + "['title']" + "['score']" + "['all_awardings']" + "num_comments"
	'''
	#submission = reddit.submission(id="oqup6m")
	submission = reddit.submission("oqx075")
	# print(submission.title)  # to make it non-lazy
	# sr = submission.subreddit
	# sr.icon_img
	# pprint.pprint(vars(sr))
	# print(submission.author)
	#print(getSubmissionHtml(submission))
	generateImage(getSubmissionHtml(submission), 600)
	#options = {
	#    'crop-w': pagewidth,
	#}
	#css = ['commentstyle.css']
	#imgkit.from_string(HTML, 'out.jpg', options,css=css)
	return
	while True:
		time.sleep(1)
		# Checks each comment in the generated stream of new comments
		# Skips bot calls that were made before the bot was running
		#for comment in reddit.subreddit('all').stream.comments(limit=None):
		for comment in reddit.subreddit('phrexy').comments(limit=None):
			count = count + 1
			howmany = ""
			for keyword in keywords:
				if (keyword in comment.body.lower()):
					for param in params:
						if param in comment.body.lower():
							howmany = param
							break
					#print(str(comment.body_html) + ' by ' + str(comment.author))
					#if(comment.parent().id.startswith('t3')):
					#print(comment.parent_id)
					allparents = []
					parent = comment.parent()
					single = getCommentHtml(comment.parent(), 0)
					while(parent.name.startswith('t1')):
						#take snapshot of parent
						allparents.append(parent)
						#print(parent.body)  # to make it non-lazy
						#pprint.pprint(vars(parent))
						#print(comment.parent().link_id.startswith('t3'))
						#HTML = getCommentHtml(comment,0)
						parent = parent.parent()
						#return
					submission = getSubmissionHtml(parent)


					parentcount = len(allparents) #for page size
					count = 0
					chaintotop = ""
					for p in allparents:
						chaintotop += getCommentHtml(p, count)
						count = count + 1
					print(chaintotop)
					return


commentsnapbot()