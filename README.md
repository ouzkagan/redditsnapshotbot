# redditcommentsnapshotbot

This bot is made to take snapshot of comments

# work style

1. run comments
2. find mention or similar
3. get parameter which represents how many comments will be included<br/>
	3.1. if there is no parameter<br/>
		-> get that much of parent comments <br/>
		*stop if on top*<br/>
	3.2. if there is a parameter<br/>
		->get only 1 comment<br/>
		?->get all comments come before that<br/>
		?->get all comments coming after that<br/>
		?->get all comments flood
4. style comments (with upvotes and chain styling) - create image
5. upload image to imgur ~ for now

### To-do

- [x] Find a library to turn text to image
- [x] Imitate Reddit comment styles
- [x] Imitate Reddit (post) styles
- [ ] ~~Name bot to 'SnapshotBot' to make it more sense (taken)~~
- [x] Start with shotting 1 comment
- [ ] Shot Upper chain
- [ ] Design a signature to make it official
- [ ] Upload image to Imgur
- [ ] Design a reply for !Snapshot
- [ ] Ask redditors if it's a good idea
- [ ] Shot All chain in expanded ??
- [ ] Shot Also Post?
- [ ] Option names: 
	* parent (get only parent) **default**
	* withpost/all (from parent to port all) 
	* top (get all to first comment) **default**
	* tree (get all commented until that time)