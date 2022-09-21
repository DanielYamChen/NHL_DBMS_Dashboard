import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, insert, delete, update, func, select
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///nhl.db?check_same_thread=False', echo=None)

conn = engine.connect()

meta = MetaData(engine)

Session = sessionmaker(bind = engine)
session = Session()

# create sqlite Team table
Team = Table(
    'Team', meta,
    Column('team_abbrev', String(50), primary_key=True),
    Column('team_name', String(50)),
    Column('team_city', String(50)),
    Column('team_arena', String(50))
)
# create sqlite Player table
Player = Table(
    'Player', meta,
    Column('player_id', Integer, primary_key=True),
    Column('season', Integer, primary_key=True),
    Column('player_name', String(50)),
    Column('position', String(5)),
    Column('weight', Integer),
    Column('height', Integer),
    Column('team_abbrev', String(5))
)
# create sqlite BasicStats table
BasicStats = Table(
    'BasicStats', meta,
    Column('player_id', Integer, primary_key=True),
    Column('season', Integer, primary_key=True),
    Column('games_played', Integer),
    Column('penalty_minutes', Integer),
    Column('ice_time', Integer),
    Column('game_score', Float),
    Column('shifts', Integer),
)
# create sqlite AdvancedStats table
AdvancedStats = Table(
    'AdvancedStats', meta,
    Column('player_id', Integer, primary_key=True),
    Column('season', Integer, primary_key=True),
    Column('I_F_xGoals', Float),
    Column('I_F_flurryScoreVenueAdjustedxGoals', Float),
    Column('I_F_primaryAssists', Integer),
    Column('I_F_secondaryAssists', Integer),
    Column('I_F_shotsOnGoal', Integer),
    Column('I_F_missedShots', Integer),
    Column('I_F_blockedShotAttempts', Integer),
    Column('I_F_shotAttempts', Integer),
    Column('I_F_points', Integer),
    Column('I_F_goals', Integer),
    Column('I_F_rebounds', Integer),
    Column('I_F_savedShotsOnGoal', Integer),
    Column('I_F_faceOffsWon', Integer),
    Column('I_F_hits', Integer),
    Column('I_F_takeaways', Integer)
)

# run iff Team table has not been created
if not engine.dialect.has_table(conn, "Team"):
    # transfer csv data to sqlite Team table
    pd.read_csv('./data/Team.csv').to_sql('Team',con=engine,
                                                  if_exists='append',
                                                  index=False,
                                                  dtype={
                                                      'team_abbrev': String(50),
                                                      'team_name': String(50),
                                                      'team_city': String(50),
                                                      'team_arena': String(50)
                                                      })
    
# run iff Player table has not been created
if not engine.dialect.has_table(conn, "Player"):
    # transfer csv data to sqlite Player table
    pd.read_csv('./data/Player.csv').to_sql('Player',con=engine,
                                                  if_exists='append',
                                                  index=False,
                                                  dtype={
                                                      'player_id': Integer,
                                                      'season': Integer,
                                                      'player_name': String(50),
                                                      'position': String(5),
                                                      'weight': Integer,
                                                      'height': Integer,
                                                      'team_abbrev': String(5)
                                                      })
# run iff BasicStats table has not been created
if not engine.dialect.has_table(conn, "BasicStats"):
    # transfer csv data to sqlite BasicStats table
    pd.read_csv('./data/BasicStats.csv').to_sql('BasicStats',con=engine,
                                                  if_exists='append',
                                                  index=False,
                                                  dtype={
                                                      'player_id': Integer,
                                                      'season': Integer,
                                                      'games_played': Integer,
                                                      'penalty_minutes': Integer,
                                                      'ice_time': Integer,
                                                      'game_score': Float,
                                                      'shifts': Integer
                                                      })

# run iff AdvancedStats table has not been created
if not engine.dialect.has_table(conn, "AdvancedStats"):
    # transfer csv data to sqlite AdvancedStats table
    pd.read_csv('./data/AdvancedStats.csv').to_sql('AdvancedStats',con=engine,
                                                  if_exists='append',
                                                  index=False,
                                                  dtype={
                                                      'player_id': Integer,
                                                      'season': Integer,
                                                      'I_F_xGoals': Float,
                                                      'I_F_flurryScoreVenueAdjustedxGoals': Float,
                                                      'I_F_primaryAssists': Integer,
                                                      'I_F_secondaryAssists': Integer,
                                                      'I_F_shotsOnGoal': Integer,
                                                      'I_F_missedShots': Integer,
                                                      'I_F_blockedShotAttempts': Integer,
                                                      'I_F_shotAttempts': Integer,
                                                      'I_F_points': Integer,
                                                      'I_F_goals': Integer,
                                                      'I_F_rebounds': Integer,
                                                      'I_F_savedShotsOnGoal': Integer,
                                                      'I_F_faceOffsWon': Integer,
                                                      'I_F_hits': Integer,
                                                      'I_F_takeaways': Integer
                                                      })


meta.create_all()

##################################################
##### BEGINNING OF FUNCTIONS FOR INTERFACE 1 #####
##################################################

'''
This function is for inserting a player tuple into DBMS.

return: error string of failed insert and 1 on successful insert
'''
def insert_player(pid=None, s=None, pname=None, pos=None, w=None, h=None, tm_abrv=None):
    # check 1: pid and s MUST NOT be empty
    if (pid is None) or (s is None) or (pname is None) or (pos is None) or (w is None) or (h is None) or (tm_abrv is None):
        return "Invalid insert: ALL blanks MUST NOT be empty."
        # return 0
    
    # check 2: player_id/season combo already exists in database
    if session.query(Player).filter((Player.c.player_id == pid) & (Player.c.season == s)).first() is not None:
        return "Invalid insert: player_id/season combo already exists in database"
        # return 0

    # if check 1 & 2 passed -> insert player data into dbms
    insert_statement_1 = insert(Player).values(player_id=pid,
                                               season=s,
                                               player_name=pname,
                                               position=pos,
                                               weight=w,
                                               height=h,
                                               team_abbrev=tm_abrv)
    insert_statement_2 = insert(BasicStats).values(player_id = pid,
                                                   season = s,
                                                   games_played = 0,
                                                   penalty_minutes = 0,
                                                   ice_time = 0,
                                                   game_score = 0,
                                                   shifts = 0)
    insert_statement_3 = insert(AdvancedStats).values(player_id = pid,
                                                      season = s,
                                                      I_F_xGoals = 0,
                                                      I_F_flurryScoreVenueAdjustedxGoals = 0,
                                                      I_F_primaryAssists = 0,
                                                      I_F_secondaryAssists = 0,
                                                      I_F_shotsOnGoal = 0,
                                                      I_F_missedShots = 0,
                                                      I_F_blockedShotAttempts = 0,
                                                      I_F_shotAttempts = 0,
                                                      I_F_points = 0,
                                                      I_F_goals = 0,
                                                      I_F_rebounds = 0,
                                                      I_F_savedShotsOnGoal = 0,
                                                      I_F_faceOffsWon = 0,
                                                      I_F_hits = 0,
                                                      I_F_takeaways = 0)
    
    conn.execute(insert_statement_1)
    conn.execute(insert_statement_2)
    conn.execute(insert_statement_3)
    
    return 1
    
    
'''
This function deletes a player from DBMS given a player_id & season

return: error string if deletion failed and 1 on success
'''
def delete_player(pid=None, s=None):
    # check 1: pid and s MUST NOT be empty
    if (pid is None) or (s is None):
        return "Invalid delete: player_id and season MUST NOT be empty."
        # return 0
    
    # check 2: player_id/season combo must exist in database
    if session.query(Player).filter((Player.c.player_id == pid) & (Player.c.season == s)).first() is None:
        return "Invalid delete: player_id/season combo doesn't exists in database"
        # return 0
    
    # if check 1 & 2 pass -> delete player from dbms
    delete_statement_1 = delete(Player).where((Player.c.player_id==pid) & (Player.c.season==s))
    delete_statement_2 = delete(BasicStats).where((BasicStats.c.player_id==pid) & (BasicStats.c.season==s))
    delete_statement_3 = delete(AdvancedStats).where((AdvancedStats.c.player_id==pid) & (AdvancedStats.c.season==s))
    conn.execute(delete_statement_1)
    conn.execute(delete_statement_2)
    conn.execute(delete_statement_3)
    return 1
  
    
'''
This function updates one or multiple of the following player attributes:
        - player_name
        - position
        - weight
        - height
        - team_abbrev

return: error string if update failed and 1 on success
'''
def update_player(pid=None, s=None, pname=None, pos=None, w=None, h=None, tm_abrv=None):
    # check 1: pid and s MUST NOT be empty
    if (pid is None) or (s is None):
        return "Invalid update: player_id and season MUST NOT be empty."
        # return 0
    
    # check 2: player_id/season combo must exist in database
    if session.query(Player).filter((Player.c.player_id == pid) & (Player.c.season == s)).first() is None:
        return "Invalid update: player_id/season combo doesn't exists in database"
        # return 0
    
    # check 3: must have passed a value in one of the updatable features
    if (pname is None) and (pos is None) and (w is None) and (h is None) and (tm_abrv is None):
        return "Invalid update: must have passed a value in one of the updatable features."
        # return 0
    
    # if check 1 & 2 & 3 pass -> update player data
    if (pname is not None):
        update_statement = update(Player).where((Player.c.player_id==pid) & (Player.c.season==s)).values(player_name=pname)
        conn.execute(update_statement)
    if (pos is not None):
        update_statement = update(Player).where((Player.c.player_id==pid) & (Player.c.season==s)).values(position=pos)
        conn.execute(update_statement)
    if (w is not None):
        update_statement = update(Player).where((Player.c.player_id==pid) & (Player.c.season==s)).values(weight=w)
        conn.execute(update_statement)
    if (h is not None):
        update_statement = update(Player).where((Player.c.player_id==pid) & (Player.c.season==s)).values(height=h)
        conn.execute(update_statement)
    if (tm_abrv is not None):
        update_statement = update(Player).where((Player.c.player_id==pid) & (Player.c.season==s)).values(team_abbrev=tm_abrv)
        conn.execute(update_statement)
    
    return 1
    

'''
This function searches for player data for the 'Display' button. Dictionary is of form:
    {'player_name':'---', 'position':'---', 'weight':'---', 'height':'---', 'team_abbrev':'---'}

return: dictionary of player data or 0 if failed
'''
def get_player_data(pid=None, pname=None, s=None):
    if (pname is None or (pid is not None and pname is not None)):
        # check 1: pid and s MUST NOT be empty
        if (pid is None) or (s is None):
            return "Invalid get: player_id and season MUST NOT be empty."
            # return 0
        
        # check 2: player_id/season combo must exist in database
        if session.query(Player).filter((Player.c.player_id == pid) & (Player.c.season == s)).first() is None:
            return "Invalid get: player_id/season combo doesn't exists in database"
            # return 0
        
        # check 1 & 2 passed -> get player data
        get_statment = Player.select().where((Player.c.player_id==pid) & (Player.c.season==s))
    
    else:
        # check 1: pid and s MUST NOT be empty
        if (s is None):
            return "Invalid get: season MUST NOT be empty."
            # return 0
        
        # check 2: player_id/season combo must exist in database
        if session.query(Player).filter((Player.c.player_name == pname) & (Player.c.season == s)).first() is None:
            return "Invalid get: player_id/season combo doesn't exists in database"
            # return 0
        
        # check 1 & 2 passed -> get player data
        get_statment = Player.select().where((Player.c.player_name==pname) & (Player.c.season==s))
    
    result = conn.execute(get_statment)
    player_dict = {}
    for row in result:
        player_dict = {
            "player_id" : row[0],
            "season" : row[1],
            "player_name" : row[2],
            "position" : row[3],
            "weight" : row[4],
            "height" : row[5],
            "team_abbrev" : row[6]
            }
    
    return player_dict

##################################################
#####    END OF FUNCTIONS FOR INTERFACE 1    #####
##################################################

##################################################
##### BEGINNING OF FUNCTIONS FOR INTERFACE 2 #####
##################################################

'''
This function returns team dictionary of form:
    {'team_abbrev':'---', 'team_name':'---', 'team_city':'---', 'team_arena':'---'}

return: 0 on failure, dictionary of basic team info on success
'''
def get_basic_team_info(tm_name=None):
    # check: team name exists in 'Team' table
    if session.query(Team).filter(Team.c.team_name == tm_name).first() is None:
        print("ERR: team name not found in database")
        return 0
    
    get_statment = Team.select().where(Team.c.team_name==tm_name)
    result = conn.execute(get_statment)
    team_dict = {}
    for row in result:
        team_dict = {
            "team_abbrev" : row[0],
            "team_name" : row[1],
            "team_city" : row[2],
            "team_arena" : row[3],
            }
    
    return team_dict
    
'''
Buckets team historical player weights into 8 buckets. Does not count '0' weights as they are equivalent to missing data
Example returned dictionary:
    {'<= 159': 2, '[160, 174]': 4, '[175, 189]': 77, '[190, 204]': 155, '[205, 219]': 87, '[220, 234]': 36, '[235, 249]': 4, '>=250': 1}

returns: 0 on failure, dictionary of buckets on success
'''
def get_team_weight_buckets(tm_name=None):
    # check: team name exists in 'Team' table
    if session.query(Team).filter(Team.c.team_name == tm_name).first() is None:
        print("ERR: team name not found in database")
        return 0
    
    team_dict = get_basic_team_info(tm_name)
    tm_abbrev = team_dict.get("team_abbrev")
    
    bucket_list =[]
    # count number players weight <=159
    get_statement = select([func.count()]).select_from(Player).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.weight<=159) & (Player.c.weight>0))
    result = conn.execute(get_statement)
    for row in result:
        bucket_list.append(row[0])
         
    # count number players weight [160, 174]
    get_statement = select([func.count()]).select_from(Player).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.weight>=160) & (Player.c.weight<=174))
    result = conn.execute(get_statement)
    for row in result:
        bucket_list.append(row[0])
        
    # count number players weight [175, 189]
    get_statement = select([func.count()]).select_from(Player).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.weight>=175) & (Player.c.weight<=189))
    result = conn.execute(get_statement)
    for row in result:
        bucket_list.append(row[0])
    
    # count number players weight [190, 204]
    get_statement = select([func.count()]).select_from(Player).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.weight>=190) & (Player.c.weight<=204))
    result = conn.execute(get_statement)
    for row in result:
        bucket_list.append(row[0])
        
    # count number players weight [205, 219]
    get_statement = select([func.count()]).select_from(Player).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.weight>=205) & (Player.c.weight<=219))
    result = conn.execute(get_statement)
    for row in result:
        bucket_list.append(row[0])

    # count number players weight [220, 234]
    get_statement = select([func.count()]).select_from(Player).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.weight>=220) & (Player.c.weight<=234))
    result = conn.execute(get_statement)
    for row in result:
        bucket_list.append(row[0])

    # count number players weight [235, 249]
    get_statement = select([func.count()]).select_from(Player).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.weight>=235) & (Player.c.weight<=249))
    result = conn.execute(get_statement)
    for row in result:
        bucket_list.append(row[0])
        
    # count number players weight >=250
    get_statement = select([func.count()]).select_from(Player).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.weight>=250))
    result = conn.execute(get_statement)
    for row in result:
        bucket_list.append(row[0])
        
    weight_dict = {
        "<= 159" : bucket_list[0],
        "[160, 174]" : bucket_list[1],
        "[175, 189]" : bucket_list[2],
        "[190, 204]" : bucket_list[3],
        "[205, 219]" : bucket_list[4],
        "[220, 234]" : bucket_list[5],
        "[235, 249]" : bucket_list[6],
        ">=250" : bucket_list[7]
        }
    
    return weight_dict

'''
Buckets team historical player heights into 9 buckets excluding heights of '0'
Example returned dictionary:
    {'<= 70': 45, '71': 44, '72': 63, '73': 65, '74': 48, '75': 52, '76': 22, '77': 17, '>=78': 10}

returns: 0 on failure, dictionary of buckets on success
'''
def get_team_height_buckets(tm_name=None):
    # check: team name exists in 'Team' table
    if session.query(Team).filter(Team.c.team_name == tm_name).first() is None:
        print("ERR: team name not found in database")
        return 0
    
    team_dict = get_basic_team_info(tm_name)
    tm_abbrev = team_dict.get("team_abbrev")
    
    bucket_list =[]
    # count number players height <=70
    get_statement = select([func.count()]).select_from(Player).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.height<=70) & (Player.c.height>0))
    result = conn.execute(get_statement)
    for row in result:
        bucket_list.append(row[0])
         
    # count number players wight height of 71
    get_statement = select([func.count()]).select_from(Player).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.height==71))
    result = conn.execute(get_statement)
    for row in result:
        bucket_list.append(row[0])
        
    # count number players wight height of 72
    get_statement = select([func.count()]).select_from(Player).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.height==72))
    result = conn.execute(get_statement)
    for row in result:
        bucket_list.append(row[0])

    # count number players wight height of 73
    get_statement = select([func.count()]).select_from(Player).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.height==73))
    result = conn.execute(get_statement)
    for row in result:
        bucket_list.append(row[0])
    
    # count number players wight height of 74
    get_statement = select([func.count()]).select_from(Player).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.height==74))
    result = conn.execute(get_statement)
    for row in result:
        bucket_list.append(row[0])
    
    # count number players wight height of 75
    get_statement = select([func.count()]).select_from(Player).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.height==75))
    result = conn.execute(get_statement)
    for row in result:
        bucket_list.append(row[0])
    
    # count number players wight height of 76
    get_statement = select([func.count()]).select_from(Player).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.height==76))
    result = conn.execute(get_statement)
    for row in result:
        bucket_list.append(row[0])
    
    # count number players wight height of 77
    get_statement = select([func.count()]).select_from(Player).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.height==77))
    result = conn.execute(get_statement)
    for row in result:
        bucket_list.append(row[0])
        
    # count number players wight height of >=78
    get_statement = select([func.count()]).select_from(Player).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.height>=78))
    result = conn.execute(get_statement)
    for row in result:
        bucket_list.append(row[0])
        
 
        
    height_dict = {
        "<= 70" : bucket_list[0],
        "71" : bucket_list[1],
        "72" : bucket_list[2],
        "73" : bucket_list[3],
        "74" : bucket_list[4],
        "75" : bucket_list[5],
        "76" : bucket_list[6],
        "77" : bucket_list[7],
        ">=78" : bucket_list[8]
        }
    
    return height_dict


'''
Returns a list of all team names.
'''
def getAllTeamNames():
    get_statement = Team.select()
    result = conn.execute(get_statement)
    team_list = []
    for row in result:
        team_list.append(row[1])
    return team_list

'''
Gets the net Game Score Performance of a teams players each year. Returns dict like:
    {'2009': 527.07, '2010': 457.34, '2011': 590.5100000000001, '2012': 274.81, '2013': 339.83000000000004, 
     '2014': 374.52000000000004, '2015': 555.32, '2016': 758.88, '2017': 781.0100000000001, '2018': 885.46, 
     '2019': 730.4399999999998, '2020': 573.3000000000001, '2021': 1024.3400000000001}
    
return: 0 on failure, dictionary success
'''
def get_game_score_performance(tm_name=None):
    # check: team name exists in 'Team' table
    if session.query(Team).filter(Team.c.team_name == tm_name).first() is None:
        print("ERR: team name not found in database")
        return 0
    
    team_dict = get_basic_team_info(tm_name)
    tm_abbrev = team_dict.get("team_abbrev")
    
    j = Player.join(BasicStats, (Player.c.player_id==BasicStats.c.player_id) & (Player.c.season==BasicStats.c.season))
    
    gsp_list = []
    
    # get total player gsp for team in 2009
    gsp = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2009))
    result = conn.execute(stmt)
    for row in result:
        gsp += row[12]
    gsp_list.append(gsp)
    # get total player gsp for team in 2010
    gsp = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2010))
    result = conn.execute(stmt)
    for row in result:
        gsp += row[12]
    gsp_list.append(gsp)
    # get total player gsp for team in 2011
    gsp = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2011))
    result = conn.execute(stmt)
    for row in result:
        gsp += row[12]
    gsp_list.append(gsp)
    # get total player gsp for team in 2012
    gsp = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2012))
    result = conn.execute(stmt)
    for row in result:
        gsp += row[12]
    gsp_list.append(gsp)
    # get total player gsp for team in 2013
    gsp = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2013))
    result = conn.execute(stmt)
    for row in result:
        gsp += row[12]
    gsp_list.append(gsp)
    # get total player gsp for team in 2014
    gsp = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2014))
    result = conn.execute(stmt)
    for row in result:
        gsp += row[12]
    gsp_list.append(gsp)
    # get total player gsp for team in 2015
    gsp = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2015))
    result = conn.execute(stmt)
    for row in result:
        gsp += row[12]
    gsp_list.append(gsp)
    # get total player gsp for team in 2016
    gsp = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2016))
    result = conn.execute(stmt)
    for row in result:
        gsp += row[12]
    gsp_list.append(gsp)
    # get total player gsp for team in 2017
    gsp = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2017))
    result = conn.execute(stmt)
    for row in result:
        gsp += row[12]
    gsp_list.append(gsp)
    # get total player gsp for team in 2018
    gsp = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2018))
    result = conn.execute(stmt)
    for row in result:
        gsp += row[12]
    gsp_list.append(gsp)
    # get total player gsp for team in 2019
    gsp = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2019))
    result = conn.execute(stmt)
    for row in result:
        gsp += row[12]
    gsp_list.append(gsp)
    # get total player gsp for team in 2020
    gsp = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2020))
    result = conn.execute(stmt)
    for row in result:
        gsp += row[12]
    gsp_list.append(gsp)
    # get total player gsp for team in 2021
    gsp = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2021))
    result = conn.execute(stmt)
    for row in result:
        gsp += row[12]
    gsp_list.append(gsp)
    
    gsp_dict = {
        "2009" : gsp_list[0],
        "2010" : gsp_list[1],
        "2011" : gsp_list[2],
        "2012" : gsp_list[3],
        "2013" : gsp_list[4],
        "2014" : gsp_list[5],
        "2015" : gsp_list[6],
        "2016" : gsp_list[7],
        "2017" : gsp_list[8],
        "2018" : gsp_list[9],
        "2019" : gsp_list[10],
        "2020" : gsp_list[11],
        "2021" : gsp_list[12],
        }
    
    return gsp_dict
    

'''
Gets the net Penalty Minutes of a teams players each year. Returns dict like:
    {'2009': 760, '2010': 834, '2011': 738, '2012': 582, '2013': 855, '2014': 694, 
     '2015': 561, '2016': 744, '2017': 583, '2018': 464, '2019': 465, '2020': 373, '2021': 618}
    
return: 0 on failure, dictionary on success
'''
def get_penalty_minutes(tm_name=None):
    # check: team name exists in 'Team' table
    if session.query(Team).filter(Team.c.team_name == tm_name).first() is None:
        print("ERR: team name not found in database")
        return 0
    
    team_dict = get_basic_team_info(tm_name)
    tm_abbrev = team_dict.get("team_abbrev")
    
    j = Player.join(BasicStats, (Player.c.player_id==BasicStats.c.player_id) & (Player.c.season==BasicStats.c.season))
    
    pm_list = []
    
    # get total player pm for team in 2009
    pm = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2009))
    result = conn.execute(stmt)
    for row in result:
        pm += row[10]
    pm_list.append(pm)
    # get total player pm for team in 2010
    pm = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2010))
    result = conn.execute(stmt)
    for row in result:
        pm += row[10]
    pm_list.append(pm)
    # get total player pm for team in 2011
    pm = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2011))
    result = conn.execute(stmt)
    for row in result:
        pm += row[10]
    pm_list.append(pm)
    # get total player pm for team in 2012
    pm = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2012))
    result = conn.execute(stmt)
    for row in result:
        pm += row[10]
    pm_list.append(pm)
    # get total player pm for team in 2013
    pm = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2013))
    result = conn.execute(stmt)
    for row in result:
        pm += row[10]
    pm_list.append(pm)
    # get total player pm for team in 2014
    pm = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2014))
    result = conn.execute(stmt)
    for row in result:
        pm += row[10]
    pm_list.append(pm)
    # get total player pm for team in 2015
    pm = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2015))
    result = conn.execute(stmt)
    for row in result:
        pm += row[10]
    pm_list.append(pm)
    # get total player pm for team in 2016
    pm = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2016))
    result = conn.execute(stmt)
    for row in result:
        pm += row[10]
    pm_list.append(pm)
    # get total player pm for team in 2017
    pm = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2017))
    result = conn.execute(stmt)
    for row in result:
        pm += row[10]
    pm_list.append(pm)
    # get total player pm for team in 2018
    pm = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2018))
    result = conn.execute(stmt)
    for row in result:
        pm += row[10]
    pm_list.append(pm)
    # get total player pm for team in 2019
    pm = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2019))
    result = conn.execute(stmt)
    for row in result:
        pm += row[10]
    pm_list.append(pm)
    # get total player pm for team in 2020
    pm = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2020))
    result = conn.execute(stmt)
    for row in result:
        pm += row[10]
    pm_list.append(pm)
    # get total player pm for team in 2021
    pm = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2021))
    result = conn.execute(stmt)
    for row in result:
        pm += row[10]
    pm_list.append(pm)

    
    pm_dict = {
        "2009" : pm_list[0],
        "2010" : pm_list[1],
        "2011" : pm_list[2],
        "2012" : pm_list[3],
        "2013" : pm_list[4],
        "2014" : pm_list[5],
        "2015" : pm_list[6],
        "2016" : pm_list[7],
        "2017" : pm_list[8],
        "2018" : pm_list[9],
        "2019" : pm_list[10],
        "2020" : pm_list[11],
        "2021" : pm_list[12],
        }
    
    return pm_dict

'''
Gets the net Ice Time of a teams players each year. Returns dict like:
    {'2009': 1188667, '2010': 1269929, '2011': 1438771, '2012': 883429, '2013': 1462542, 
     '2014': 1324164, '2015': 1283797, '2016': 1565450, '2017': 1519547, '2018': 1472265, 
     '2019': 1270171, '2020': 1044426, '2021': 1546887}
    
return: 0 on failure, dictionary on success
'''
def get_ice_time(tm_name=None):
    # check: team name exists in 'Team' table
    if session.query(Team).filter(Team.c.team_name == tm_name).first() is None:
        print("ERR: team name not found in database")
        return 0
    
    team_dict = get_basic_team_info(tm_name)
    tm_abbrev = team_dict.get("team_abbrev")
    
    j = Player.join(BasicStats, (Player.c.player_id==BasicStats.c.player_id) & (Player.c.season==BasicStats.c.season))
    
    iceTime_list = []
    
    # get total player iceTime for team in 2009
    iceTime = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2009))
    result = conn.execute(stmt)
    for row in result:
        iceTime += row[11]
    iceTime_list.append(iceTime)
    # get total player iceTime for team in 2010
    iceTime = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2010))
    result = conn.execute(stmt)
    for row in result:
        iceTime += row[11]
    iceTime_list.append(iceTime)
    # get total player iceTime for team in 2011
    iceTime = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2011))
    result = conn.execute(stmt)
    for row in result:
        iceTime += row[11]
    iceTime_list.append(iceTime)
    # get total player iceTime for team in 2012
    iceTime = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2012))
    result = conn.execute(stmt)
    for row in result:
        iceTime += row[11]
    iceTime_list.append(iceTime)
    # get total player iceTime for team in 2013
    iceTime = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2013))
    result = conn.execute(stmt)
    for row in result:
        iceTime += row[11]
    iceTime_list.append(iceTime)
    # get total player iceTime for team in 2014
    iceTime = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2014))
    result = conn.execute(stmt)
    for row in result:
        iceTime += row[11]
    iceTime_list.append(iceTime)
    # get total player iceTime for team in 2015
    iceTime = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2015))
    result = conn.execute(stmt)
    for row in result:
        iceTime += row[11]
    iceTime_list.append(iceTime)
    # get total player iceTime for team in 2016
    iceTime = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2016))
    result = conn.execute(stmt)
    for row in result:
        iceTime += row[11]
    iceTime_list.append(iceTime)
    # get total player iceTime for team in 2017
    iceTime = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2017))
    result = conn.execute(stmt)
    for row in result:
        iceTime += row[11]
    iceTime_list.append(iceTime)
    # get total player iceTime for team in 2018
    iceTime = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2018))
    result = conn.execute(stmt)
    for row in result:
        iceTime += row[11]
    iceTime_list.append(iceTime)
    # get total player iceTime for team in 2019
    iceTime = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2019))
    result = conn.execute(stmt)
    for row in result:
        iceTime += row[11]
    iceTime_list.append(iceTime)
    # get total player iceTime for team in 2020
    iceTime = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2020))
    result = conn.execute(stmt)
    for row in result:
        iceTime += row[11]
    iceTime_list.append(iceTime)
    # get total player iceTime for team in 2021
    iceTime = 0
    stmt = select(Player,BasicStats).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==2021))
    result = conn.execute(stmt)
    for row in result:
        iceTime += row[11]
    iceTime_list.append(iceTime)
    

    
    iceTime_dict = {
        "2009" : iceTime_list[0],
        "2010" : iceTime_list[1],
        "2011" : iceTime_list[2],
        "2012" : iceTime_list[3],
        "2013" : iceTime_list[4],
        "2014" : iceTime_list[5],
        "2015" : iceTime_list[6],
        "2016" : iceTime_list[7],
        "2017" : iceTime_list[8],
        "2018" : iceTime_list[9],
        "2019" : iceTime_list[10],
        "2020" : iceTime_list[11],
        "2021" : iceTime_list[12],
        }
    
    return iceTime_dict
    

##################################################
#####    END OF FUNCTIONS FOR INTERFACE 2    #####
##################################################


##################################################
##### BEGINNING OF FUNCTIONS FOR INTERFACE 3 #####
##################################################

'''
Gets basic stats of a team in a given year.

returns: a dataframe
'''
def get_basic_stats(s=None, tm_name=None):
    # check 1: s and tm_name MUST NOT be empty
    if (s is None) or (tm_name is None):
        print("Invalid request: season and tm_name MUST NOT be empty.")
        return 0
    
    # join player and basicstats tables
    team_dict = get_basic_team_info(tm_name)
    tm_abbrev = team_dict.get("team_abbrev")
    j = Player.join(BasicStats, (Player.c.player_id==BasicStats.c.player_id) & (Player.c.season==BasicStats.c.season))
    
    # check 2: tm_name/season combo must exist in database
    if session.query(Player).filter((Player.c.season == s) & (Player.c.team_abbrev == tm_abbrev)).first() is None:
        print("Invalid update: team_name/season combo doesn't exists in database")
        return 0
    
    stmt = select(Player.c.player_name,
                  Player.c.team_abbrev,
                  BasicStats.c.games_played,
                  BasicStats.c.penalty_minutes,
                  BasicStats.c.ice_time,
                  BasicStats.c.game_score,
                  BasicStats.c.shifts).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==s))
    result = conn.execute(stmt)
    row_list = []
    for row in result:
        row_list.append(row)
        
    df = pd.DataFrame(row_list, columns=['Player', 'Team', 'Games Played', 'Penalty Minutes', 'Ice Time', 'Game Score', 'Shifts'])
    return df


'''
Gets advanced stats of a team in a given year.

returns: a dataframe
'''
def get_advanced_stats(s=None, tm_name=None):
    # check 1: s and tm_name MUST NOT be empty
    if (s is None) or (tm_name is None):
        print("Invalid request: season and tm_name MUST NOT be empty.")
        return 0
    
    # join player and basicstats tables
    team_dict = get_basic_team_info(tm_name)
    tm_abbrev = team_dict.get("team_abbrev")
    j = Player.join(AdvancedStats, (Player.c.player_id==AdvancedStats.c.player_id) & (Player.c.season==AdvancedStats.c.season))
    
    # check 2: tm_name/season combo must exist in database
    if session.query(Player).filter((Player.c.season == s) & (Player.c.team_abbrev == tm_abbrev)).first() is None:
        print("Invalid update: team_name/season combo doesn't exists in database")
        return 0
    
    stmt = select(Player.c.player_name,
                  Player.c.team_abbrev,
                  AdvancedStats.c.I_F_xGoals,
                  AdvancedStats.c.I_F_flurryScoreVenueAdjustedxGoals,
                  AdvancedStats.c.I_F_primaryAssists,
                  AdvancedStats.c.I_F_secondaryAssists,
                  AdvancedStats.c.I_F_shotsOnGoal,
                  AdvancedStats.c.I_F_missedShots,
                  AdvancedStats.c.I_F_blockedShotAttempts,
                  AdvancedStats.c.I_F_shotAttempts,
                  AdvancedStats.c.I_F_points,
                  AdvancedStats.c.I_F_goals,
                  AdvancedStats.c.I_F_rebounds,
                  AdvancedStats.c.I_F_savedShotsOnGoal,
                  AdvancedStats.c.I_F_faceOffsWon,
                  AdvancedStats.c.I_F_hits,
                  AdvancedStats.c.I_F_takeaways).select_from(j).where((Player.c.team_abbrev==tm_abbrev) & (Player.c.season==s))
    result = conn.execute(stmt)
    row_list = []
    for row in result:
        row_list.append(row)
        
    df = pd.DataFrame(row_list, columns=['Player', 'Team', 'Expected Goals'	,'Flurry Score Venue Adjusted Expected Goals','Primary Assists',	
                                         'Secondary Assists','Shots On Goal','Missed Shots','Blocked Shot Attempts','Shot Attempts','Points',
                                         'Goals','Rebounds','Saved Shots On Goal','Face Offs Won','Hits','Takeaways'])
    return df


##################################################
#####    END OF FUNCTIONS FOR INTERFACE 3    #####
##################################################