import xlrd
import twitter_db
import re

tweet_list = xlrd.open_workbook("tweet_list.xls")

def read_list(excelfile, sheetNo):
    """ Troll through all the entries, compiling a list."""
    sheet = excelfile.sheet_by_index(sheetNo)
    workingList = []
    for row in range(0,sheet.nrows):
        workingList.append(sheet.row_values(row)[0])
    return workingList

full_list = []
for i in range(3,4):
    full_list += read_list(tweet_list, i)


print "Total tweets: ", len(full_list)
db = twitter_db.TwitterDB()
for each in full_list:
    each = re.sub(u'\xa0', '',each)
    db.add_tweet(each)
db.close()
print "DB load complete."