# Football_predictor
Machine Learning Football Predictor

 In this project you can do your predictions about any football match.
 


1) Getting data. As you might probably know, gettind the data is usually one of the biggest part of the work. Well, this was not an exception. I used web scraping applications for getting the team rates from the website sofifa.com. This site is a nice data source and it extracts the data used for the videogame fifa.com. I got 8 seasons of teams from the main 5 leagues in Europe. Every seasons has between 30 and 100 rating-updates. I used basically Beautifulsoup from Python. Regarding the results and statistics of the matches, I downloaded them from https://www.football-data.co.uk/ and I merged it by date with the rates of the teams for the matchdays. The size of the matrix for the training and evaluation consisted of 14417 football games and 124 features (not all the features were used). Download FIFA_teams_scrap.ipynb for the general data file for the network and scrap_last_update.ipynb for the last update.

2) Machine learning part. As usual, not the longest part of the project. I used logistic regressions and linear regressions. No, don't think I did not try deep learning. I did and I used Grid Search cross validation for searching the best hyperparameters. Surprisingly the results for the linear regression were a little bit more accurate than for the neural network. If you want to check it, just check the file Models.ipynb.

3) Visualization and deployment of results. For the graphs I used d3.js, a powerful library of javascript when it comes to data visualization. I deployed it by using Flask. The "core" of the app is the file app.py. You can check index.html to see the html documents and the d3.js files in the folder static/js
