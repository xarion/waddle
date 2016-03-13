import re

from data.Data import Data

p = re.compile('.*(([Mm]anhattan)|([Nn]ew[ ]?[Yy]ork)|(NYC)|((NY))).*')

d = Data(training_factor=0, include_user_history=False)
docs = d.get_training_data()
docs = d.get_test_data()
matchCount = 0
count = 0
nyc = 0
nyc_corr = 0
nyc_incorr = 0
not_nyc = 0
not_nyc_corr = 0
not_nyc_incorr = 0
for doc in docs:
    m = p.match(doc["text"])
    match = m is not None
    is_nyc = doc["place"]["full_name"] == "Manhattan, NY"

    nyc += is_nyc
    nyc_corr += is_nyc and match
    nyc_incorr += is_nyc and not match
    not_nyc += not is_nyc
    not_nyc_corr += not is_nyc and not match
    not_nyc_incorr += not is_nyc and match

print nyc
print nyc_corr
print nyc_incorr

print not_nyc
print not_nyc_corr
print not_nyc_incorr


print "micro-average precision: %.2f" % ((nyc_corr + not_nyc_corr) / (nyc + not_nyc))
print "micro-average recall: %.2f" % ((nyc_corr + not_nyc_corr) / (nyc + not_nyc))
