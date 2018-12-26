# Analytical Approach to Content Creation

With the rise of digital marketing and social media, content creation is key to grabbing the attention of your target market and adding value to your existing customer base.  Without the proper tools and processes in place to capture the attention of your audience, companies fall prey to their competitors.  This project aims to develop an analytical approach to the content creation process.  For more information, view the file labeled report.pdf.

### Prerequisites

To properly run the code, several packages must be installed first.  To install these packages cd to the local directory where the project is located and install the packages from the requirments.txt file.  
```
pip install -r requirments
```

### Run Application 
To scrape current blog data from relevant sites, and analyze the data to find trending topics across different blogs enter the following commands.  
```
python getBlogData.py
python content_creation -c blogTrendingTopics
```

To download current query data from Google, and analyze the data to find the top issues customers are searching for enter the following commands
```
python getGoogleData.py
python content_creation -c getGoogleData
```




