import pandas as pd
import tweepy
import sys
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from twitterformv2 import Ui_MainWindow


global completed
completed = 0
global linescount
linescount = 0
global consumer_key_string
global consumer_secret_string
global access_key_string
global access_secret_string

def get_all_tweets(screen_name):
    consumer_key = consumer_key_string
    consumer_secret = consumer_secret_string
    access_key = access_key_string
    access_secret = access_secret_string
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    alltweets = []
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1
    while len(new_tweets) > 0:
        print("Getting Tweets for", screen_name)
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        print("...%s tweets downloaded so far" % (len(alltweets)))
        data = [[obj.user.screen_name, obj.user.name, obj.user.id_str, obj.user.description.encode("utf8"),
                 obj.created_at.year, obj.created_at.month, obj.created_at.day,
                 "%s.%s" % (obj.created_at.hour, obj.created_at.minute),
                 "%s.%s.%s" % (obj.created_at.month, obj.created_at.day, obj.created_at.year), obj.id_str,
                 obj.favorite_count, obj.retweet_count, obj.text] for obj in alltweets]
        data2 = [[obj.text] for obj in alltweets]
        dataframe = pd.DataFrame(data,
                                 columns=['screen_name', 'name', 'twitter_id', 'description', 'year', 'month', 'day',
                                          'time', 'date', 'tweet_id', 'favorite_count', 'retweet_count', 'tweet'])
        dataframe2 = pd.DataFrame(data2, columns=['tweet'])
        dataframe.to_csv("%s_tweets.csv" % (screen_name), index=True)
        dataframe2.to_csv("%s_tweetsonly.csv" % (screen_name), index=False)
    print("Finished Mining Tweets for", screen_name)


class StartQT5(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.button_open.clicked.connect(self.file_dialog)
        self.ui.button_submit.clicked.connect(self.button_submit_clicked)
        self.ui.progressBar.setValue(0)

    def button_submit_clicked(self):
        # pass in the usernames of the accounts you want to download
        self.ui.progressBar.setValue(0)

        def startMiner(threadname):
            tusers = self.ui.textEdit.toPlainText()
            global consumer_key_string
            consumer_key_string = self.ui.QLEConsumerKey.text()
            global consumer_secret_string
            consumer_secret_string = self.ui.QLEConsumerSecret.text()
            global access_key_string
            access_key_string = self.ui.QLEAccessKey.text()
            global access_secret_string
            access_secret_string = self.ui.QLEAccessSecret.text()

            completedCount = 0;
            for line in tusers.splitlines():
                global linescount
                linescount += 1
            for line in tusers.splitlines():
                try:
                    get_all_tweets(line.rstrip())
                except (IndexError, tweepy.TweepError):
                    pass

                    completedCount += 1
                    global completed
                    completed = ((completedCount / linescount) * 100)
                    self.ui.progressBar.setValue(completed)
                    print("Finished Mining Tweets")

        class myThread(threading.Thread):
            def __init__(self, threadID):
                threading.Thread.__init__(self)
                self.threadID = threadID

            def run(self):
                startMiner(self.name)

        thread1 = myThread(1)
        thread1.start()

    def file_dialog(self):
        fd = QtWidgets.QFileDialog(self)
        self.filename = fd.getOpenFileName()
        from os.path import isfile
        if isfile(self.filename):
            import codecs
            s = codecs.open(self.filename, 'r', 'utf-8').read()
            self.ui.textEdit.setPlainText(s)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = StartQT5()
    myapp.show()
    sys.exit(app.exec_())
