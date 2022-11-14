## AIM

This program has the purpose of notifying its user every time a twitter user twits something, with a latency of no more than 2 or 3 minutes.

The utility of this script comes out as twitter users with several million followers have slow pushup notifications to its followers, which makes it virtually impossible for a follower to monitor tweets of those popular users without a latency of several hours or even days.

## UTILITY

Twitter users with certain million followers create tendencies. For example, this program was made with the purpose of targeting a certain twitter account: Elon Musk, with more than 70 million followers at the time of writing this lines. Due to markets sentiment, Elon Musk modifies stock prices and cryptocurrency prices just with a one line twit. The SEC watches him closely to make sure this does not happen with stocks, but Cryptocurrencies are unregulated in that regard. Therefore, knowing what he says around cryptocurrency before the rest of Twitter users know it is crucial for investment purposes. You can see there is a clear correlation between Musk twitting positively about Dogecoin and an inmediate fluctuation of the cryptocurrency price against the USD/EUR as he did in January 14 [(see twit and price fluctuation)](https://github.com/blackcub3s/twitterScrap/blob/main/infoInstalacio/PRECEDENTS/1aManipulacio.jpeg) and again at 25 January 2021; the latter twit brought about a 10% increase in the prices of the coin of a 10% in a 36 hour span:

![musk bull on Dogecoin via tesla](https://github.com/blackcub3s/twitterScrap/blob/main/infoInstalacio/PRECEDENTS/2a%20manipulacio%20mercat.png)


## PROGRAMMING APPROACH

Initially I thought it would be an easy task to make a twitter scrapper using only web scrapping technologies, such as selenium, beautifulsoup or urllib. But it was not. In the end I decided to take an inefficient approach, but useful in most cases[^1]: I used an OCR tool to extract the text of a cropped screenshot, which would contain Musk's latest twit. I did that using [PIL](https://pillow.readthedocs.io/en/stable/) (python image library) instead of getting it directly from the HTML source code. The first line of twit of that screenshot -discarding the line with the @username- was what in the program I call as ROI (Region of Interest) and is what I compare at each execution of the program. That cropped screenshot would serve to generate a .txt file where the information of that ROI at a given time, would be stored. When, after several minutes or seconds, the program was executed again (see segons pausa argument [^3], which is the time the program remains "waiting" for the next webscrap) it will compare the actual ROI stored in the last .txt with the previous ROI stored in the previous .txt file. This is done, for example, within the `function comparaRoi(ROI1,ROI2)` that I state here:

https://github.com/blackcub3s/twitterScrap/blob/ea66dcd555a1d4a30d0d701abc3a5e2b288e094a/main__TwitterScrap.py#L193-L228



## NOTIFICATIONS SERVICE 

I used a notification service called [pushover](https://pushover.net/). With pushover you can make a desktop program communicate with your mobile via push-notifications with no time. It is a free service and involves a one-time purchasing fee.



[^1]: The program works when a new twit, with text, is published by the user. It won't work if the user twits an image without text on top of it, without text, pins a twit on top of its profile or retweets or replies. In this case, we would have a false positive (the program would told us a new twit has been published where it hasn't). What is it important, though, the program has a very high sensitivity to changes of twits with texts.

[^3]: see the inicial function call of the program https://github.com/blackcub3s/twitterScrap/blob/ea66dcd555a1d4a30d0d701abc3a5e2b288e094a/main__TwitterScrap.py#L505-L508