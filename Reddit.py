import praw
import json
import os


class reddit():

    def getRedditAPI(self):
        self.url = 'https://www.reddit.com/'
        data_file_path = os.path.join(os.path.dirname(__file__), "credentials.json")
        with open(data_file_path) as f:
            params = json.load(f)
        
        self.reddit = praw.Reddit(client_id=params['client_id'], 
                             client_secret=params['api_key'],
                             password=params['password'], 
                             user_agent='accessFirst',
                             username=params['username'])
    
    
    def writeSubredditData(self, Subreddit, questionLimit, timeLimit):
        subreddit = self.reddit.subreddit(Subreddit)
        #quoraQuestions = open(r'questionsQuora.txt', "ab")
        #new method just write to an aray and give it back
        quoraQuestions = []
        for submission in subreddit.top("day", limit = questionLimit):
            forbiddenWord = False
            if submission.created_utc < timeLimit:
                continue #this is linux time and Eastern time zone us
            if submission.title.endswith("?") and len(submission.title) < 249 and len(submission.title) > 13:
                listOfForbiddenWords = ['sub', 'AITA','redit','reddid','reddit','subreddit', 'r/','I ','AITA', 'TIL', "Reddit", "WCGW", "Reddits", "Redditors","Redditors", " my ", " mine ", " we ", " I ", "I've", " me ", " I'am " , " Iam ", "I'm"]
                for word in listOfForbiddenWords:
                    if word in submission.title:
                        forbiddenWord = True
                        break
                if forbiddenWord == False:
                    strSubmissionTitle = submission.title
                    quoraQuestions.append(strSubmissionTitle)
                    #quoraQuestions.write(strSubmissionTitle.encode('utf8'))#schreibt damit in Byte mode, (ab) so dass Sonderzeichen drin bleiben
                    #quoraQuestions.write(b"\n")#new line in bytes
        return quoraQuestions

#wtf is this "New", unused
    def writeSubredditDataNew(self, Subreddit, questionLimit):
        subreddit = self.reddit.subreddit(Subreddit)
        print(subreddit.display_name)  
        quoraQuestions = open(r'questionsQuora.txt', "ab")
        for submission in subreddit.new(limit = questionLimit):
            forbiddenWord = False
            strSstrSubmissionTitle = submission.title
            if submission.title.endswith("?") and len(submission.title) < 249 and len(submission.title) > 15:
                listOfForbiddenWords = ['reddit','subreddit', 'r/','I ','AITA', 'TIL', "Reddit", "WCGW", "Reddits", "Redditors","Redditors", " my ", " mine ", " we ", " I ", "I've", " me ", " I'am " , " Iam ", "I'm"]
                for word in listOfForbiddenWords:
                    if word in submission.title:
                        print('forbidden Word')
                        forbiddenWord = True
                        break
                if forbiddenWord == False:
                    strSubmissionTitle = submission.title
                    quoraQuestions.write(strSubmissionTitle.encode('utf8'))#schreibt damit in Byte mode, (ab) so dass Sonderzeichen drin bleiben
                    quoraQuestions.write(b"\n")#new line in bytes