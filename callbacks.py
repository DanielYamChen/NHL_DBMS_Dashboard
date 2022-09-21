# import dash IO and graph objects
from dash.dependencies import Input, Output
# Plotly graph objects to render graph plots
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
# Import dash html, bootstrap components, and tables for datatables
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_table
import dash
import pandas as pd

# Import app from the same folder
from app_setup import app

## import back-end functions
import backend_functions
from backend_functions import get_basic_team_info, get_team_weight_buckets
from backend_functions import get_team_height_buckets, get_game_score_performance
from backend_functions import get_penalty_minutes, get_ice_time, get_player_data
from backend_functions import insert_player, update_player, delete_player
from backend_functions import get_basic_stats, get_advanced_stats
# Import custom data.py
import data

# Import data from data.py file
# teams_df = data.teams
# Hardcoded list that contain era names
# era_list = data.era_list

# Player Profiles data
# player_df = data.players
# team_players_df = data.team_players

# Statistical data
# batter_df = data.batters
# field_df = data.fielding
# pitching_df = data.pitching

# batter_df.astype({"rbi":'int64', "sb":'int64', "cs":'int64', "so":'int64', "ibb":'int64', "hbp":'int64', "sh":'int64', "sf":'int64', "g_idp":'int64'})

player_record = {
    "player_id": 0,
    "season": 0,
    "player_name" : "",
    "position" : "",
    "weight" : 0,
    "height" : 0,
    "team_abbrev" : "",
}

b_or_a_form = {
    "team_name": "",
    "season": 0,
    "b_or_a": "",    
}

# This will update the team dropdown and the range of the slider
@app.callback(
    [Output('team-dropdown', 'options'),
    Output('team-dropdown', 'value'),
    Output('era-slider', 'value'),],
    [Input('era-dropdown', 'value')])
def select_era(selected_era):
    # Check if selected era is equal to the value in the era list
    # Makes sure that teams and range are set to desired era
    if (selected_era == era_list[1]['value']):
        teams = data.dynamicteams(1)
        range = data.dynamicrange(1)
    elif (selected_era == era_list[2]['value']):
        teams = data.dynamicteams(2)
        range = data.dynamicrange(2)
    elif (selected_era == era_list[3]['value']):
        teams = data.dynamicteams(3)
        range = data.dynamicrange(3)
    elif (selected_era == era_list[4]['value']):
        teams = data.dynamicteams(4)
        range = data.dynamicrange(4)
    elif (selected_era == era_list[5]['value']):
        teams = data.dynamicteams(5)
        range = data.dynamicrange(5)
    elif (selected_era == era_list[6]['value']):
        teams = data.dynamicteams(6)
        range = data.dynamicrange(6)
    elif (selected_era == era_list[7]['value']):
        teams = data.dynamicteams(7)
        range = data.dynamicrange(7)
    else:
        teams = data.dynamicteams(0)
        range = data.dynamicrange(0)
    # Return team list, the initial value of the team list, and the range in the era
    return teams, teams[0]['value'], range


# Team championship datatable
@app.callback(
    [Output('team-data', 'children')],
    [Input('team-dropdown', 'value'),Input('era-slider', 'value')])
def update_win_table(selected_team, year_range):
    # Create filter dataframe of requested team
    filter_team = teams_df[teams_df.team_id == selected_team]
    # I will revisit this again soon, it just doesnt seem efficient
    if year_range:
        filter_year = filter_team[( filter_team.year >= year_range[0] )&( filter_team.year <= year_range[1] )]
    else:
        filter_year = filter_team[( filter_team.year >= 1903 )&( filter_team.year <= 1919 )]

    # Filter unneccessary data
    Data = filter_year.drop(columns=['team_id', 'franchise_id', 'div_id', 'ghome', 'g', 'w', 'l', 'r', 'ab', 'h', 'double', 'triple',
        'hr', 'bb', 'so', 'sb', 'cs', 'era', 'cg', 'sho', 'sv', 'ha', 'hra', 'bba', 'soa', 'e', 'dp', 'hbp', 'sf', 'ra', 'er', 'ipouts',
        'fp', 'name', 'park', 'attendance', 'bpf', 'ppf', 'team_id_br', 'team_id_lahman45', 'team_id_retro'])

    # Set data to variable if team won world series
    WIN = Data[Data.ws_win == 'Y']
    # Check if dataframe is empty (no world series won)
    if WIN.empty:
        # Set data to variable if team won a wild card
        WIN = Data[Data.wc_win == 'Y']
        # if the team did not win a wild card (dataframe is empty)
        if WIN.empty:
            # finally set data to variable if team won a division title
            WIN = Data[Data.div_win == 'Y']

    # Create empty data list for notification if needed
    data_note = []

    # If the team did not win any championships append alert and return data list
    if WIN.empty:
        data_note.append(html.Div(dbc.Alert('The selected team did not win any championships.', color='warning'),))
        return data_note
    # else set and return datatable with team championship data
    else:
        data_note.append(html.Div(dash_table.DataTable(
            data= WIN.to_dict('records'),
            columns= [{'name': x, 'id': x} for x in WIN],
            style_as_list_view=True,
            editable=False,
            style_table={
                'overflowY': 'scroll',
                'width': '100%',
                'minWidth': '100%',
            },
            style_header={
                    'backgroundColor': '#f8f5f0',
                    'fontWeight': 'bold'
                },
            style_cell={
                    'textAlign': 'center',
                    'padding': '8px',
                },
        )))
        return data_note


###################################
#### Begin Team Info Interface ####
###################################
# %%
# This will update the team Basic Information division
@app.callback(
    [Output("team_abbrev", "children"),
     Output("team_name", "children"),
     Output("team_city", "children"),
     Output("team_arena", "children")],
    [Input("team-dropdown", "value")])
def updateTeamBasicInfo(team_name):
    team_basic_info = get_basic_team_info(team_name)
    abbrev_child = "Team Abbrev.: " + team_basic_info["team_abbrev"]
    name_child = "Team name: " + team_basic_info["team_name"]
    city_child = "Team city: " + team_basic_info["team_city"]
    arena_child = "Team arena: " + team_basic_info["team_arena"]
    
    return abbrev_child, name_child, city_child, arena_child

# Callback to update weight hist. bar chart, takes data request from team_menu
@app.callback(
    Output('weight-hist', 'figure'),
    Input('team-dropdown', 'value'))
def updateWeightHist(team_name):
    weight_dict = get_team_weight_buckets(team_name)
    # Create Bar Chart figure
    fig = px.bar(pd.DataFrame(weight_dict, index=["key"]).T, opacity=0.8)
        # go.Bar(name='Weights', x=pd.DataFrame(weight_dict, index=["key"]).T,
        #        y="key", marker_color='#004687',opacity=0.8),
    
    # set x axes title and tick to only include year given no half year such as 1927.5
    fig.update_xaxes(title='Weight (lb)',tickformat='d')
    # set y axes to fixed selection range, user can only select data in the x axes
    fig.update_yaxes(title='Number of players', fixedrange=False)
    
    # Update figure, set hover to the X-Axis and establish title
    # fig.update_layout(
    #     barmode='group', title="Weight histogram of team players",
    #     font={'color':'darkslategray'},paper_bgcolor='white',plot_bgcolor='#f8f5f0',
    #     legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))
    
    # return figure
    return fig

# Callback to update height hist. bar chart, takes data request from team_menu
@app.callback(
    Output('height-hist', 'figure'),
    Input('team-dropdown', 'value'))
def updateHeightHist(team_name):
    height_dict = get_team_height_buckets(team_name)
    
    # Create Bar Chart figure
    fig = px.bar(pd.DataFrame(height_dict, index=["key"]).T, opacity=0.8)
    fig.update_xaxes(title='Height (in)',tickformat='d')
    fig.update_yaxes(title='Number of players', fixedrange=False)
       
    # return figure
    return fig

# Callback to update game score line chart, takes data request from team_menu
@app.callback(
    Output('game_score-line', 'figure'),
    Input('team-dropdown', 'value'))
def updateGameScoreLine(team_name):
    score_dict = get_game_score_performance(team_name)
    
    # Create line chart figure
    fig = px.line(pd.DataFrame(score_dict, index=["key"]).T)
    fig.update_xaxes(title='Year',tickformat='d')
    fig.update_yaxes(title='Score', fixedrange=False)
       
    # return figure
    return fig

# Callback to update penalty minute line chart, takes data request from team_menu
@app.callback(
    Output('penalty_minutes-line', 'figure'),
    Input('team-dropdown', 'value'))
def updatePenaltyMinutesLine(team_name):
    penalty_dict = get_penalty_minutes(team_name)
    print(penalty_dict)
    
    # Create line chart figure
    fig = px.line(pd.DataFrame(penalty_dict, index=["key"]).T)
    fig.update_xaxes(title='Year',tickformat='d')
    fig.update_yaxes(title='Penalty minutes (min)', fixedrange=False)
    
    # return figure
    return fig

# Callback to update ice time line chart, takes data request from team_menu
@app.callback(
    Output('ice_time-line', 'figure'),
    Input('team-dropdown', 'value'))
def updateIceTimeLine(team_name):
    ice_time_dict = get_ice_time(team_name)
    
    # Create line chart figure
    fig = px.line(pd.DataFrame(ice_time_dict, index=["key"]).T)
    fig.update_xaxes(title='Year',tickformat='d')
    fig.update_yaxes(title='Ice time (sec)', fixedrange=False)
       
    # return figure
    return fig

# %%
#################################
#### End Team Info Interface ####
#################################

#######################################
#### Begin Update Player Interface ####
#######################################
# %%
## real time record what are in the update-player form
@app.callback(
    Output("form_state", "children"),
    [Input("player_id-input", "value"),
     Input("season-input", "value"),
     Input("player_name-input", "value"),
     Input("position-input", "value"),
     Input("weight-input", "value"),
     Input("height-input", "value"),
     Input("team_abbrev-input", "value")])
def updatePlayerTuple(player_id, season, player_name, position, weight, height, 
                      team_abbrev):
    player_record["player_id"] = player_id
    player_record["season"] = season
    player_record["player_name"] = player_name
    player_record["position"] = position
    player_record["weight"] = weight
    player_record["height"] = height
    player_record["team_abbrev"] = team_abbrev
    
    return ""

## callback to display/insert/update/delete player's data when buttons clicked
@app.callback(
    [Output("update_status", "children"),
     Output("player_id-display", "children"),
     Output("season-display", "children"),
     Output("player_name-display", "children"),
     Output("position-display", "children"),
     Output("weight-display", "children"),
     Output("height-display", "children"),
     Output("team_abbrev-display", "children")],
    [Input("display-button", "n_clicks"),
     Input("insert-button", "n_clicks"),
     Input("update-button", "n_clicks"),
     Input("delete-button", "n_clicks"),])
def actionPlayerData(display_clicks, insert_clicks, update_clicks, delete_clicks):
    if ((display_clicks is None) and (insert_clicks is None)
        and (update_clicks is None) and (delete_clicks is None)):
        return 8 * [html.P(children="")]
    
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print(input_id)
    if (input_id == "display-button"):
        player_dict = get_player_data(pid=player_record["player_id"],
                                      pname=player_record["player_name"],
                                      s=player_record["season"])
        
        if (isinstance(player_dict, str)): # invalid inquiry
            ret = list()
            ret.append(html.P(children="Display" + player_dict))
            for i in range(7):
                ret.append(html.P(children=""))
            
            return ret
        
        else:
            return ["Display",
                    "Player ID: " + str(player_dict["player_id"]),
                    "Season: " + str(player_dict["season"]),
                    "Player name: " + player_dict["player_name"],
                    "Position: " + player_dict["position"],
                    "Weight: " + str(player_dict["weight"]) + " lb",
                    "Height: " + str(player_dict["height"]) + " in",
                    "Team Abbrev.: " + player_dict["team_abbrev"]]
    
    elif (input_id == "insert-button"):
        ret_val = insert_player(pid=player_record["player_id"],
                                s=player_record["season"],
                                pname=player_record["player_name"],
                                pos=player_record["position"],
                                w=player_record["weight"],
                                h=player_record["height"],
                                tm_abrv=player_record["team_abbrev"])
    
        if (isinstance(ret_val, str)): # invalid insertion
            ret = list()
            ret.append(html.P(children=ret_val))
            for i in range(7):
                ret.append(html.P(children=""))
            
            return ret
        
        else:
            return ["Successfully inserted",
                    "Player ID: " + str(player_record["player_id"]),
                    "Season: " + str(player_record["season"]),
                    "Player name: " + player_record["player_name"],
                    "Position: " + player_record["position"],
                    "Weight: " + str(player_record["weight"]) + " lb",
                    "Height: " + str(player_record["height"]) + " in",
                    "Team Abbrev.: " + player_record["team_abbrev"]]
    
    elif (input_id == "update-button"):
        ret_val = update_player(pid=player_record["player_id"],
                                s=player_record["season"],
                                pname=player_record["player_name"],
                                pos=player_record["position"],
                                w=player_record["weight"],
                                h=player_record["height"],
                                tm_abrv=player_record["team_abbrev"])
        
        if (isinstance(ret_val, str)): # invalid updating
            ret = list()
            ret.append(html.P(children=ret_val))
            for i in range(7):
                ret.append(html.P(children=""))
            
            return ret
        
        else:
            player_dict = get_player_data(pid=player_record["player_id"],
                                          s=player_record["season"])
            return ["Successfully updated",
                    "Player ID: " + str(player_dict["player_id"]),
                    "Season: " + str(player_dict["season"]),
                    "Player name: " + player_dict["player_name"],
                    "Position: " + player_dict["position"],
                    "Weight: " + str(player_dict["weight"]) + " lb",
                    "Height: " + str(player_dict["height"]) + " in",
                    "Team Abbrev.: " + player_dict["team_abbrev"]]
    
    elif (input_id == "delete-button"):
        ret_val = delete_player(pid=player_record["player_id"],
                                s=player_record["season"])
        
        if (isinstance(ret_val, str)): # invalid deletion
            ret = list()
            ret.append(html.P(children=ret_val))
            for i in range(7):
                ret.append(html.P(children=""))
            
            return ret
        
        else:
            return ["Successfully updated",
                    "Player ID: " + str(player_record["player_id"]),
                    "Season: " + str(player_record["season"]),
                    "Player name: ",
                    "Position: ",
                    "Weight: ",
                    "Height: ",
                    "Team Abbrev.: "]    
        
# %%
#####################################
#### End Update Player Interface ####
#####################################

#####################################################
#### Begin Basic/Advanced Player Stats Interface ####
#####################################################
# %%
## real time record what are in the Player Basic/Advanced form
@app.callback(
    Output("b_or_a_form_state", "children"),
    [Input("stats_season-input", "value"), Input("b_or_a-dropdown", "value"),
     Input("team-dropdown", "value")])
def updateBorATuple(season, b_or_a, team_name):
    b_or_a_form["season"] = season
    b_or_a_form["b_or_a"] = b_or_a
    b_or_a_form["team_name"] = team_name
    
    return ""


@app.callback(
    [Output('player_info-table', 'data'),Output('player_info-table','columns')],
    [Input('look_up-button', 'n_clicks')])
def updatePlayerInfoTable(look_up_clicks):
    if (look_up_clicks is None):
        df = pd.DataFrame()
    
    else:
        if (b_or_a_form["b_or_a"] == "Basic"):
            df = get_basic_stats(s=b_or_a_form["season"],
                                 tm_name=b_or_a_form["team_name"])
        
        elif (b_or_a_form["b_or_a"] == "Advanced"):
            df = get_advanced_stats(s=b_or_a_form["season"],
                                    tm_name=b_or_a_form["team_name"])
        else:
            df = pd.DataFrame()
            
    # Return player profile to datatable
    return df.to_dict('records'), [{'name': x, 'id': x} for x in df]



# %%
###################################################
#### End Basic/Advanced Player Stats Interface ####
###################################################