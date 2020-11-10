import numpy as np
from flask import Flask, request, render_template
import pickle
import pandas as pd
import os

application = Flask(__name__)

model_logreg = pickle.load(open('Models/logreg.pkl', 'rb'))
model_logreg_half = pickle.load(open('Models/logreg_half.pkl', 'rb'))
model_linreg_24 = pickle.load(open('Models/linear_regression_24.pkl', 'rb'))


PICTURE_FOLDER = os.path.join('static', 'img')
application.config['UPLOAD_FOLDER'] = PICTURE_FOLDER
full_filename = os.path.join(application.config['UPLOAD_FOLDER'], 'logo.png')

prob_home_win_previous = 0
prob_draw_game_previous = 0
prob_away_win_previous   = 0
prob_home_win_half_previous  = 0 
prob_draw_game_half_previous   = 0
prob_away_win_half_previous  = 0

@application.route('/')
def home():
    return render_template('index.html', user_image = full_filename)


@application.route('/predict',methods=['POST'])
    

def predict():

    global prob_home_win_previous
    global prob_draw_game_previous
    global prob_away_win_previous
    global prob_home_win_half_previous
    global prob_draw_game_half_previous
    global prob_away_win_half_previous

    
    prob_home_win_old = prob_home_win_previous
    prob_draw_game_old = prob_draw_game_previous
    prob_away_win_old = prob_away_win_previous
    prob_home_win_half_old = prob_home_win_half_previous
    prob_draw_game_half_old = prob_draw_game_half_previous
    prob_away_win_half_old =  prob_away_win_half_previous

    int_features = [str(x) for x in request.form.values()]
    final_features = np.array(int_features)    
        
    df = pd.read_csv('list_last_update.csv') 
    home_team = df[df['Name']==final_features[0]]
    away_team = df[df['Name']==final_features[1]]

        
    X1 = np.array(home_team[['OVA', 'ATT', 'MID', 'DEF', 'Transfer Budget(M€)', 'Speed', 'Dribbling', 'Passing', 'Positioning', 'Crossing','Passing.1', 'Shooting', 'Positioning.1', 'Aggression', 'Pressure', 'Team Width', 'Defender Line', 'DP', 'IP']])
        
    X2 = np.array(away_team[['OVA', 'ATT', 'MID', 'DEF', 'Transfer Budget(M€)', 'Speed', 'Dribbling', 'Passing', 'Positioning', 'Crossing','Passing.1', 'Shooting', 'Positioning.1', 'Aggression', 'Pressure', 'Team Width', 'Defender Line', 'DP', 'IP']])
        
    X = np.concatenate((X1, X2), axis=None).astype(int)

        
    X = X.reshape(1, -1)
        
    prediction = model_logreg.predict(X)     #MATCH WINNER
    prediction2 = model_logreg.predict_proba(X)     #PROBABILITIES OF WINNING THE MATCH
    prediction3 = model_logreg_half.predict_proba(X)     #PROBABILITIES OF WINNING ON THE HALF TIME
    #    prob_home_win = (round(100*prediction2[0,2],1)).astype(str) + '%'     #PROBABILITY HOME TEAM WINS
    #    prob_draw_game = (round(100*prediction2[0,1],1)).astype(str) + '%'    #PROBABILITY DRAW GAME
    #    prob_away_win = (round(100*prediction2[0,0],1)).astype(str) + '%'     #PROBABILITY AWAY TEAM WINS
        
    prob_home_win = round(100*prediction2[0,2],1)    #PROBABILITY HOME TEAM WINS
    prob_draw_game = round(100*prediction2[0,1],1)    #PROBABILITY DRAW GAME
    prob_away_win = round(100*prediction2[0,0],1)     #PROBABILITY AWAY TEAM WINS

    prob_home_win_half = round(100*prediction3[0,2],1)    #PROBABILITY HOME TEAM WINS
    prob_draw_game_half = round(100*prediction3[0,1],1)    #PROBABILITY DRAW GAME
    prob_away_win_half = round(100*prediction3[0,0],1)     #PROBABILITY AWAY TEAM WINS
        
    prediction_24 = model_linreg_24.predict(X) 

    total_goals_half = round(prediction_24[0,3],2)
    home_goals_half = round(prediction_24[0,4],2)
    away_goals_half = round(prediction_24[0,5],2)


    total_goals_final = round(prediction_24[0,0],2)
    home_goals_final = round(prediction_24[0,1],2)
    away_goals_final = round(prediction_24[0,2],2)

    full_time_shots = round(prediction_24[0,8],1)
    home_team_shots = round(prediction_24[0,6],1)
    away_team_shots = round(prediction_24[0,7],1)

    full_time_shots_target = round(prediction_24[0,11],1)
    home_team_shots_target = round(prediction_24[0,9],1)
    away_team_shots_target = round(prediction_24[0,10],1)

    full_time_corners = round(prediction_24[0,14],1)
    home_team_corners = round(prediction_24[0,12],1)
    away_team_corners = round(prediction_24[0,13],1)

    Total_fouls_comitted = round(prediction_24[0,17],1)
    home_team_fouls_comitted = round(prediction_24[0,15],1)
    away_team_fouls_comitted = round(prediction_24[0,16],1)

    Total_yellow_cards = round(prediction_24[0,20],1)
    home_team_yellow_cards = round(prediction_24[0,18],1)
    away_team_yellow_cards = round(prediction_24[0,19],1)

    Total_red_cards = round(prediction_24[0,23],1)
    home_team_red_cards = round(prediction_24[0,21],1)
    away_team_red_cards = round(prediction_24[0,22],1)

    prob_home_win_previous = prob_home_win
    prob_draw_game_previous = prob_draw_game
    prob_away_win_previous = prob_away_win
    prob_home_win_half_previous = prob_home_win_half
    prob_draw_game_half_previous = prob_draw_game_half
    prob_away_win_half_previous = prob_away_win_half



        # here we tell him what variables we want to send to the html:

    return render_template('index.html', value1 = prob_home_win, value2 = prob_draw_game, value3 = prob_away_win, 
    value4 = prob_home_win_half, value5 = prob_draw_game_half, value6 = prob_away_win_half, 
    value7 = total_goals_half, value8 = home_goals_half, value9 = away_goals_half, 
    value10 = total_goals_final, value11 = home_goals_final, value12 = away_goals_final, 
    value13 = full_time_shots, value14 = home_team_shots, value15 = away_team_shots, 
    value16 = full_time_shots_target, value17 = home_team_shots_target, value18 = away_team_shots_target, 
    value19 = full_time_corners, value20 = home_team_corners, value21 = away_team_corners, 
    value22 =  Total_fouls_comitted , value23 = home_team_fouls_comitted, value24 = away_team_fouls_comitted, 
    value28 =  Total_yellow_cards, value29 = home_team_yellow_cards, value30 = away_team_yellow_cards,
    value31 =  Total_red_cards, value32 = home_team_red_cards, value33 = away_team_red_cards,
    value1_old = prob_home_win_old, value2_old = prob_draw_game_old, value3_old = prob_away_win_old,
    value4_old = prob_home_win_half_old, value5_old = prob_draw_game_half_old, value6_old = prob_away_win_half_old, user_image = full_filename)  
    

    

if __name__ == "__main__":
    application.run(debug=True)
    
#if __name__ == "__main__":
#    app.run(host='0.0.0.0',port=8080)
