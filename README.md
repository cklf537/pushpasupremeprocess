# pushpasupremeprocess

Follow below steps to execute the application.
# Google Spread sheet:
1. Navigate to the google sheet document.
2. Copy Id of the spread sheet which you want to read.
    i. https://docs.google.com/spreadsheets/d/15m1jGnsbbqFFD3afHf6AgivcfcEbcoqqkr4UOa4ERT8/edit#gid=0 (example: 15m1jGnsbbqFFD3afHf6AgivcfcEbcoqqkr4UOa4ERT8 )  
3. Make the curent sheet (Ex: Sheet 1) as the default. (Currently the application always reads from the first sheet in the document - fix in progress to read fro all the sheets as configurable.)
4. Open config.ini file.
    i. Specify read column.(Ex: gcp.spreedsheet.read.column=A:A )
    ii. Specify right column (Ex: gcp.spreedsheet.write.column=D )
