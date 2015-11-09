import textblob
import requests


class Sentiments:
    def __init__(self):
        link = "https://raw.githubusercontent.com/shadowwalker/optgo/master/data/comments.txt"
        self.f = requests.get(link)
    
    def get_stats(self):
        pos = 0
        neg = 0
        for line in self.f:
            for t in line.split('.'):
                score = textblob.TextBlob(t).sentiment.polarity
                if score > 0.7:
                    pos += 1
                elif score < -0.5:
                    neg += 1
        return float(pos)/(pos+neg)



