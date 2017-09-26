## Megapod

*STEPS*

1. Collect Google Search Results
2. Collect Backlinks
3. Collect Emails
4. Outreach

### Collect Google Search Results

The type of search results we are looking for are those that are relevant to our business, and that we can sensibly refer to in a generic email template.

First, choose and search a term on Google.  On the results page, push the *Results per page* to 100 in *Search Settings* and also minimize text as much as possible (CMD + (-)).

Download [LinkClump](https://chrome.google.com/webstore/detail/linkclump/lfpjkncokllnfokkgpkobnkbkmelfefj) from the Chrome Webstore to copy links fast.  Copy all the search results (SHIFT + OPT + drag).  Create a csv named after using the search term snakecased, `<search_term>.csv`.  The csv should have one column with the heading `url`.  Fill the column with the Google / LinkClump results (CMD + V).

### Collect Google Search Results

After saving the search results csv, we want to find the domains of websites that have linked to any of these search results.

Run the `spider.py` script, passing in the name of the csv as a parameter (ex. `python spider.py <search_term>.csv`).  Let the spider run in the background.  Spiders are tricky and error-prone so raise any issues you see that interfere with or stop the program.  When the crawl is done, use the ahrefs interface to download every file (files will automatically download to `backlinks/<search_term>`).  Remove all these files from the browser after.

### Collect Emails

Run the `compile.py` script to compile the results from ahrefs, and dupe-check against previously collected data.  Pass in the search term as the only argument (ex `python compile.py <search_term>`).  The result is a file written to `domains/without_emails/<search_term>.csv`.

Use [Email Grabber](https://www.emailgrabber.net) to find emails for the domains in the csv.  Create a copy of the file `domains/without_emails/<search_term>.csv` with only the domain column.  Click Queue Manager > Browse to upload the file, then Start to begin the email crawl.  Recommended settings are Levels Allowed = 0, Limit last level = 7 pages per domain, Simultaneous searches = 3.

When the crawl is complete, download the file, and save it in `domains/with_emails/<search_term>.csv`.

### Outreach

## TODO
- finish documentation
- finish `needs_manual_dwnld.txt`
- test and optimize
