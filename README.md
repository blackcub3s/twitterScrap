## AIM

This program has the purpose of notifying its user every time a twitter user twits something, with a latency of no more than 2 or 3 minutes.

The utility of this script comes out as twitter with several million followers have slow pushup notifications to its followers. It becomes virtually impossible to monitor publications of popular users without a latency of several hours.

## UTILITY

Certain twitter users with certain million followers create tendencies. For example, this program was made with the purpose of targeting a certain twitter account: Elon Musk, with more than 70 million followers at the time of writing this lines. Due to markets sentiment, Elon Musk modifies stock prices and cryptocurrency prices just with a one line twit. The SEC watches him closely to make sure this does not happen with stocks, but Cryptocurrencies are unregulated in that regard. Therefore, knowing what he says around cryptocurrency before the rest of Twitter users know it is crucial for investment purposes. You can see there is a clear correlation between Musk twitting positively about Dogecoin and an inmediate fluctuation of the cryptocurrency price against the USD/EUR as he did in January 14 [see twit and prices](https://github.com/blackcub3s/twitterScrap/blob/main/infoInstalacio/PRECEDENTS/1aManipulacio.jpeg) and again at 25 January 2021; the latter twit brought about a 10% increase in the prices of the coin of a 10% in a 36 hour span (see here)[https://github.com/blackcub3s/twitterScrap/blob/main/infoInstalacio/PRECEDENTS/2a%20manipulacio%20mercat%2025gen2021.png]:

![musk bull on Dogecoin via tesla](https://github.com/blackcub3s/twitterScrap/blob/main/infoInstalacio/PRECEDENTS/2a%20manipulacio%20mercat%2025gen2021.png)


## PROGRAMMING APPROACH

Initially I thought it would be an easy task to make a twitter scrapper using only web scrapping technologies, such as selenium, beautifulsoup, urllib. But it was not. In the end I took a rather inefficient approach, but useful in most cases[^1]: I used an OCR tool to extract the text of the cropped screenshot (image) of the screen profile of Elon Musk (using [PIL](https://pillow.readthedocs.io/en/stable/) image library, instead of getting directly the text from the HTML code -which was certainly not easily structured-. That cropped screenshot would be what in the program I call as ROI (Region of Interest). Each cropped screenshot would generate a .txt file where information would be stored. When it gets executed again it will compare the with the previous .txt file with the newer one. This is done, for example, within the `function comparaRoi(ROI1,ROI2)`

The program would take a screenshot of the profile with a time period (in s) of * *segons pausa* * (it would just open a browser tag, take the screenshot and save the text of the first line of the twit [^2] In the code I uploaded * *segons pausa* * is 5s, but I happen to find a time interval of 2 or 3 minutes (120 or 180s) or even 15 minutes would be ok.

## NOTIFICATIONS SERVICE 

I used a notification service called [pushover](https://pushover.net/). With pushover you can make a desktop program communicate with your mobile via push-notifications with no time. It is a free service and involves a one-time purchasing fee.



[^1] The program works when a new twit, with text, is published by the user. It won't work if the user twits an image without text on top of it, without text, pins a twit on top of its profile or retweets or replies. In this case, we would have a false positive (the program would told us a new twit has been published where it hasn't). What is it important, though, the program has a very high sensitivity to changes of twits with texts.

[^2] Another feature that I would need to add in the future.