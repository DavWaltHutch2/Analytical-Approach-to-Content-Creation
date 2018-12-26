import time
from pytrends.request import TrendReq
import pandas as pd


def getTrends(inDepth, inKeywords):

    ##FUNCTION VARIABLES
    depth = inDepth
    keywords = inKeywords
    topResults = None
    risingResults = None


    ##CONNECT TO GOOGLE
    pytrends = TrendReq(hl='en-US', tz=360)

    ##LOOP THROUGH KEYWORDS
    for i in range(0,len(keywords)):
        print("Round: " + str(i + 1) + " of " + str(len(keywords)) + " / Keyword = " + keywords[i])
        print("------------------------------------")

        ##BUILD PAYLOAD
        kw_list = [keywords[i]]
        last_week = "now 7-d"
        one_month = "today 1-m"
        location = "US"

        try:
            ##GET RELATED QUERIES
            pytrends.build_payload(kw_list, cat=0, timeframe=one_month, geo=location, gprop='')
            related_queries = pytrends.related_queries()

        except:
            ##SLEEP
            sleep_time = 60*3
            print("Max retries exceeded.  Sleeping for " + str(sleep_time) + " seconds")
            time.sleep(sleep_time)

            ##GET RELATED QUERIES
            pytrends.build_payload(kw_list, cat=0, timeframe=one_month, geo=location, gprop='')
            related_queries = pytrends.related_queries()


        if topResults is None:
            topResults = related_queries[keywords[i]]["top"]
        else:
            topResults = pd.concat([topResults, related_queries[keywords[i]]["top"]], ignore_index = True)

        if risingResults is None:
            risingResults = related_queries[keywords[i]]["rising"]
            ##risingResults["topic"] = keywords[i]
        else:
            temp_results = related_queries[keywords[i]]["rising"]
            temp_results = pd.DataFrame(temp_results)
            ##temp_results["topic"] = keywords[i]
            risingResults = pd.concat([risingResults, temp_results], ignore_index=True)


    if(depth != 0):
        children_risingResults = getTrends(depth - 1, topResults["query"])
        risingResults = pd.concat([risingResults, children_risingResults],ignore_index = True)

    ##REARRANGE RESULTS
    risingResults = risingResults.sort_values(by =["value"], ascending = False)
    risingResults = risingResults.reset_index(drop = True)

    return risingResults




def main():
    ##ALGO SETTINGS
    depth = 1
    keywords = ["iPhone","Android", "Samsung", "HTC", "LG"]

    ##SCRAPE DATA
    gTrends = getTrends(depth, keywords)
    gTrends = gTrends.drop_duplicates(["query"])

    ##SAVE TRENDS TO CSV
    gTrends.to_csv("./data/googleData.csv", index = False)



if __name__ == "__main__":
    main()




