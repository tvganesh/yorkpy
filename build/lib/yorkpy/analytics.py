import os
import yaml
import json
import pandas as pd
import matplotlib.pyplot as plt
from pylab import rcParams
import seaborn as sns

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 27 Dec 2018
# Function: convertYaml2PandasDataframeT20
# This function converts yaml files to Pandas dataframe and saves as CSV
#

###########################################################################################
def convertYaml2PandasDataframeT20(infile,source,dest):
    '''
    Converts and save T20 yaml files to pandasdataframes
    
    Description
    
    This function coverts all T20 Yaml files from source directory to pandas ata frames. 
    The data frames are then stored as .csv files The saved file is of the format 
    team1-team2-date.csv For e.g. Kolkata Knight Riders-Sunrisers Hyderabad-2016-05-22.csv etc
    
    Usage
    
    convertYaml2PandasDataframeT20(yamlFile,sourceDir=".",targetDir=".")
    Arguments
    
    yamlFile	
    The yaml file to be converted to dataframe and saved
    sourceDir	
    The source directory of the yaml file
    targetDir	
    The target directory in which the data frame is stored as RData file
    Value
    
    None
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.in/

    
    See Also

    convertYaml2PandasDataframeT20
    Examples
    
    # In the example below ../yamldir c
    convertYaml2PandasDataframeT20("225171.yaml",".","../data")
    
    '''

    os.chdir(source)
    os.path.join(source,infile)
    
    # Read Yaml file and convert to json
    print('Converting file:',infile)
    with open(infile) as f:
           a=yaml.load(f)
          
    # 1st innings
    deliveries=a['innings'][0]['1st innings']['deliveries']
    
    #Create empty dataframe for team1
    team1=pd.DataFrame()
    # Loop through all the deliveries of 1st innings and append each row to dataframe
    for i in range(len(deliveries)):
        df = pd.DataFrame(deliveries[i])
        b= df.T
        team1=pd.concat([team1,b])
    
    # Rename batsman to striker/non-striker as there is another column  batsman who scored runs
    team1=team1.rename(columns={'batsman':'striker'}) 
    # All extras column names
    extras=[0,'wides','byes','legbyes','noballs','penalty']
    
    if 'extras' in team1: #Check if extras are there
        # Get the columns in extras for team1
        b=team1.extras.apply(pd.Series).columns
        # Find the missing extras columns
        diff= list(set(extras) - set(b))
        print('Team1:diff:',diff)
        
        # Rename extras dict column as there is another column extras which comes from runs_dict
        team1=team1.rename(columns={'extras':'extras_dict'}) 
        #Create new columns by splitting dictionary columns - extras and runs
        team1=pd.concat([team1,team1['extras_dict'].apply(pd.Series)], axis=1)
        
        # Add the missing columns
        for col in diff:
            print("team1:",col)
            team1[col]=0
            
        team1=team1.drop(columns=0)
    else:
        print('Team1:Extras not present')
        
    # Rename runs columns to runs_dict
    if 'runs' in team1: #Check if runs in team1
        team1=team1.rename(columns={'runs':'runs_dict'}) 
        team1=pd.concat([team1,team1['runs_dict'].apply(pd.Series)], axis=1)  
    else:
        print('Team1:Runs not present')
        
    if 'wicket' in team1: #Check if wicket present
        # Rename wicket as wicket_dict dict column as there is another wicket column
        team1=team1.rename(columns={'wicket':'wicket_dict'}) 
        team1=pd.concat([team1,team1['wicket_dict'].apply(pd.Series)], axis=1) 
    else:
        print('Team1: Wicket not present')
        
    team1['team']=a['innings'][0]['1st innings']['team']
    team1=team1.reset_index(inplace=False)
    #Rename index to delivery
    team1=team1.rename(columns={'index':'delivery'}) 
    
    

    # 2nd innings - Check if the 2nd inning was played
    if len(a['innings']) > 1: # Team2 played
        deliveries=a['innings'][1]['2nd innings']['deliveries']
        #Create empty dataframe for team1
        team2=pd.DataFrame()
        # Loop through all the deliveries of 1st innings
        for i in range(len(deliveries)):
            df = pd.DataFrame(deliveries[i])
            b= df.T
            team2=pd.concat([team2,b])
            
        # Rename batsman to striker/non-striker as there is another column  batsman who scored runs
        team2=team2.rename(columns={'batsman':'striker'}) 
            
        # Get the columns in extras for team1
        if 'extras' in team2: #Check if extras in team2
            b=team2.extras.apply(pd.Series).columns
            diff= list(set(extras) - set(b))
            print('Team2:diff:',diff)
            
            # Rename extras dict column as there is another column extras which comes from runs_dict
            team2=team2.rename(columns={'extras':'extras_dict'})
            
            #Create new columns by splitting dictionary columns - extras and runs
            team2=pd.concat([team2,team2['extras_dict'].apply(pd.Series)], axis=1)
            
            # Add the missing columns
            for col in diff:
                print("team2:",col)
                team2[col]=0
                
            team2=team2.drop(columns=0)
        else:
            print('Team2:Extras not present') 
            
        # Rename  runs columns to runs_dict  
        if 'runs' in team2:
            team2=team2.rename(columns={'runs':'runs_dict'})
            team2=pd.concat([team2,team2['runs_dict'].apply(pd.Series)], axis=1) 
        else:
            print('Team2:Runs not present') 
            
        if 'wicket' in team2:
            # Rename wicket as wicket_dict column as there is another column  wicket
            team2=team2.rename(columns={'wicket':'wicket_dict'}) 
            team2=pd.concat([team2,team2['wicket_dict'].apply(pd.Series)], axis=1) 
        else:
            print('Team2:wicket not present')
    
            
        team2['team']=a['innings'][1]['2nd innings']['team'] 
        team2=team2.reset_index(inplace=False)
        
        #Rename index to delivery
        team2=team2.rename(columns={'index':'delivery'}) 
    else: # Create empty columns for team2 so that the complete DF as all columns
        team2 = pd.DataFrame()
        cols=['delivery', 'striker', 'bowler', 'extras_dict', 'non_striker',\
           'runs_dict', 'wicket_dict', 'wides', 'noballs', 'legbyes', 'byes', 'penalty',\
            'kind','player_out','fielders',\
           'batsman', 'extras', 'total', 'team']
        team2 = team2.reindex(columns=cols)
    
    #Check for missing columns. It is possible that no wickets for lost in the entire innings
    cols=['delivery', 'striker', 'bowler', 'extras_dict', 'non_striker',\
           'runs_dict', 'wicket_dict', 'wides', 'noballs', 'legbyes', 'byes', 'penalty',\
           'kind','player_out','fielders',\
           'batsman', 'extras', 'total', 'team']
    
    # Team1 - missing columns
    msngCols=list(set(cols) - set(team1.columns))
    print('Team1-missing columns:', msngCols)
    for col in msngCols:
        print("Adding:team1:",col)
        team1[col]=0
    
    # Team2 - missing columns
    msngCols=list(set(cols) - set(team2.columns))
    print('Team2-missing columns:', msngCols)
    for col in msngCols:
        print("Adding:team2:",col)
        team2[col]=0
    
    
    # Now both team1 and team2 should have the same columns. Concatenate 
    team1=team1[['delivery', 'striker', 'bowler', 'extras_dict', 'non_striker',\
           'runs_dict', 'wicket_dict', 'wides', 'noballs', 'legbyes', 'byes', 'penalty',\
           'kind','player_out','fielders',\
           'batsman', 'extras', 'total', 'team']]
    team2=team2[['delivery', 'striker', 'bowler', 'extras_dict', 'non_striker',\
           'runs_dict', 'wicket_dict', 'wides', 'noballs', 'legbyes', 'byes', 'penalty',\
           'kind','player_out','fielders',\
           'batsman', 'extras', 'total', 'team']]
    df=pd.concat([team1,team2])
    
    #Fill NA's with 0s
    df=df.fillna(0)
    
    # Fill in INFO
    print("Length of info field=",len(a['info']))
    #City
    try:
        df['city']=a['info']['city']
    except:
        df['city'] =0
    #Date
    df['date']=a['info']['dates'][0]
    #Gender
    df['gender']=a['info']['gender']
    #Match type
    df['match_type']=a['info']['match_type']
    
    # Neutral venue
    try:
        df['neutral_venue'] = a['info']['neutral_venue'] 
    except KeyError as  error:
        df['neutral_venue'] = 0
        
    #Outcome - Winner
    try:
        df['winner']=a['info']['outcome']['winner']
        # Get the win type - runs, wickets etc
        df['winType']=list(a['info']['outcome']['by'].keys())[0]
        print("Wintype=",list(a['info']['outcome']['by'].keys())[0])
        
        #Get the value of wintype
        winType=list(a['info']['outcome']['by'].keys())[0]
        print("Win value=",list(a['info']['outcome']['by'].keys())[0] )
        
        # Get the win margin - runs,wickets etc
        df['winMargin']=a['info']['outcome']['by'][winType]
        print("win margin=", a['info']['outcome']['by'][winType])
    except:
        df['winner']=0
        df['winType']=0
        df['winMargin']=0
    
    # Outcome - Tie  
    try: 
        print("Here11")
        df['result']=a['info']['outcome']['result']
        df['resultHow']=list(a['info']['outcome'].keys())[0]
        df['resultTeam'] = a['info']['outcome']['eliminator']
        print(a['info']['outcome']['result'])
        print(list(a['info']['outcome'].keys())[0])
        print(a['info']['outcome']['eliminator'])
        print("Her2")
    except:
         df['result']=0
         df['resultHow']=0
         df['resultTeam']=0
        
    try:
        df['non_boundary'] = a['info']['non_boundary'] 
    except KeyError as  error:
        df['non_boundary'] = 0
    


    try:
        df['ManOfMatch']=a['info']['player_of_match'][0]
    except:
        df['ManOfMatch']=0        
    # Identify the winner
    
    df['overs']=a['info']['overs']
    df['team1']=a['info']['teams'][0]
    df['team2']=a['info']['teams'][1]
    df['tossWinner']=a['info']['toss']['winner']
    df['tossDecision']=a['info']['toss']['decision']
    df['venue']=a['info']['venue']
    
    # Rename column 'striker' to batsman
    # Rename column 'batsman' to runs as it signifies runs scored by batsman
    df=df.rename(columns={'batsman':'runs'})
    df=df.rename(columns={'striker':'batsman'}) 
    
    outfile=a['info']['teams'][0]+ '-' + a['info']['teams'][1] + '-' +a['info']['dates'][0].strftime('%Y-%m-%d') + '.csv'
    destFile=os.path.join(dest,outfile)
    print(destFile)
    df.to_csv(destFile,index=False)
    print("Dataframe shape=",df.shape)
    return df, outfile

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 27 Dec 2018
# Function: convertAllYaml2PandasDataframesT20
# This function converts all yaml files to Pandas dataframes and saves as CSV
#

###########################################################################################
def convertAllYaml2PandasDataframesT20(source,dest):
    '''
    Convert and save all Yaml files to pandas dataframes and save as CSV
    
    Description
    
    This function coverts all Yaml files from source directory to data frames. The data frames are 
    then stored as .csv. The saved files are of the format team1-team2-date.RData For 
    e.g. England-India-2008-04-06.RData etc
    
    Usage
    
    convertAllYaml2PandasDataframesT20(sourceDir=".",targetDir=".")
    Arguments
    
    sourceDir	
    The source directory of the yaml files
    targetDir	
    The target directory in which the data frames are stored as RData files
    Value
    
    None
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.in/

    
    See Also

    convertYaml2PandasDataframe
    Examples

    # In the example below ../yamldir is the source dir for the yaml files
    convertAllYaml2PandasDataframesT20("../yamldir","../data")
    
    
    '''
    files = os.listdir(source)
    for index, file in enumerate(files):
         print("\n\nFile no=",index)
         if file.endswith(".yaml"):
             df, filename = convertYaml2PandasDataframe(file, source, dest)
             #print(filename)
             

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 27 Dec 2018
# Function: getRuns
# This function gets the runs scored by batsmen
#

###########################################################################################             
def getRuns(df):
    df1=df[['batsman','runs','extras','total','non_boundary']]
    # Determine number of deliveries faced and runs scored
    runs=df1[['batsman','runs']].groupby(['batsman'],sort=False,as_index=False).agg(['count','sum'])
    # Drop level 0
    runs.columns = runs.columns.droplevel(0)
    runs=runs.reset_index(inplace=False)
    runs.columns=['batsman','balls','runs']
    return(runs)
    
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 27 Dec 2018
# Function: getFours
# This function gets the fours scored by batsmen
#

########################################################################################### 
    
def getFours(df):
    df1=df[['batsman','runs','extras','total','non_boundary']]
    # Get number of 4s. Check if it is boundary (non_boundary=0)
    m=df1.loc[(df1.runs >=4) & (df1.runs <6) & (df1.non_boundary==0)]
    # Count the number of 4s
    noFours= m[['batsman','runs']].groupby('batsman',sort=False,as_index=False).count()
    noFours.columns=['batsman','4s']
    return(noFours)
    
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 27 Dec 2018
# Function: getSixes
# This function gets the sixes scored by batsmen
#

########################################################################################### 
    
def getSixes(df):
    df1=df[['batsman','runs','extras','total','non_boundary']]
    df2= df1.loc[(df1.runs ==6)]
    sixes= df2[['batsman','runs']].groupby('batsman',sort=False,as_index=False).count()
    sixes.columns=['batsman','6s']
    return(sixes)
    
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 27 Dec 2018
# Function: getExtras
# This function gets the extras for the team
#

########################################################################################### 

def getExtras(df):
    df3= df[['total','wides', 'noballs', 'legbyes', 'byes', 'penalty', 'extras']]
    a=df3.sum().astype(int)
    #Convert series to dataframe
    extras=a.to_frame().T
    return(extras)
    
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 27 Dec 2018
# Function: teamBattingScorecardMatch
# This function returns the team batting scorecard
#

########################################################################################### 

def teamBattingScorecardMatch (match,theTeam):
    '''
    Team batting scorecard of a team in a match
    
    Description
    
    This function computes returns the batting scorecard (runs, fours, sixes, balls played) for the team
    
    Usage
    
    teamBattingScorecardMatch(match,theTeam)
    Arguments
    
    match	
    The match for which the score card is required e.g.
    theTeam	
    Team for which scorecard required
    Value
    
    scorecard A data frame with the batting scorecard
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.in/

    
    See Also
    
    teamBatsmenPartnershipMatch
    teamBowlingScorecardMatch
    teamBatsmenVsBowlersMatch
    Examples


    x1,y1=teamBattingScorecardMatch(kkr_sh,"Sunrisers Hyderabad")
    print(x1)
    print(y1)
    
    '''
    team=match.loc[match.team== theTeam]
    a1= getRuns(team)
    b1= getFours(team)
    c1= getSixes(team)
    
    # Merge columns
    d1=pd.merge(a1, b1, how='outer', on='batsman')
    e=pd.merge(d1,c1,how='outer', on='batsman')
    e=e.fillna(0)
    
    e['4s']=e['4s'].astype(int)
    e['6s']=e['6s'].astype(int)
    e['SR']=(e['runs']/e['balls']) *100
    scorecard = e[['batsman','runs','balls','4s','6s','SR']]
    extras=getExtras(match)
    return(scorecard,extras)
    
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 27 Dec 2018
# Function: getRunsConceded
# This function gets the runs conceded by bowler
#

########################################################################################### 
def getRunsConceded(df):
    # Note the column batsman has the runs scored by batsman
    df1=df[['bowler','runs','wides', 'noballs']]
    df2=df1.groupby('bowler').sum()
    # Only wides and no balls included in runs conceded
    df2['runs']=(df2['runs']+df2['wides']+df2['noballs']).astype(int)
    df3 = df2['runs']
    return(df3)

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 27 Dec 2018
# Function: getOvers
# This function gets the overs for bowlers
#

########################################################################################### 
def getOvers(df):
    df1=df[['bowler','delivery']]
    df2=(df1.groupby('bowler').count()/6).astype(int)
    df2.columns=['overs']
    return(df2)
    
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 27 Dec 2018
# Function: getMaidens
# This function gets the maiden overs for bowlers
#

########################################################################################### 

def getMaidens(df):
    df1=df[['bowler','delivery','runs','wides', 'noballs']]  
    # Get the over
    df1['over']=df1.delivery.astype(int)
    
    # Runs conceded includes wides and noballs
    df1['runsConceded']=df1['runs'] + df1['wides'] + df1['noballs']
    df2=df1[['bowler','over','runsConceded']]
    
    # Compute runs in each over by bowler
    df3=df2.groupby(['bowler','over']).sum()
    df4=df3.reset_index(inplace=False)
    
    # If maiden set as 1 else as 0
    df4.loc[df4.runsConceded !=0,'maiden']=0
    df4.loc[df4.runsConceded ==0,'maiden']=1
    
    # Sum te maidens
    df5=df4[['bowler','maiden']].groupby('bowler').sum()
    return(df5)
    
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 27 Dec 2018
# Function: getWickets
# This function gets the wickets for bowlers
#

########################################################################################### 
def getWickets(df):
    df1=df[['bowler','kind', 'player_out', 'fielders']]
    df2= df1[df1.player_out !='0']
    df3 = df2[['bowler','player_out']].groupby('bowler').count()
    return(df3)


    
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 27 Dec 2018
# Function: teamBowlingScorecardMatch
# This function gets the bowling scorecard
#

########################################################################################### 
def teamBowlingScorecardMatch (match,theTeam):
    '''
    Compute and return the bowling scorecard of a team in a match
    
    Description
    
    This function computes and returns the bowling scorecard of a team in a match
    
    Usage
    
    teamBowlingScorecardMatch(match,theTeam)
    Arguments
    
    match	
    The match between the teams
    theTeam	
    Team for which bowling performance is required
    Value
    
    l A data frame with the bowling performance in alll matches against all oppositions
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.in/
    
    See Also
    
    teamBowlingWicketMatch
    teamBowlersVsBatsmenMatch
    teamBattingScorecardMatch
    Examples
    

    m=teamBowlingScorecardMatch(kkr_sh,"Sunrisers Hyderabad")
    print(m)
    '''
    team=match.loc[match.team== theTeam]
    # Compute overs bowled
    a1= getOvers(team).reset_index(inplace=False)
    # Compute runs conceded
    b1= getRunsConceded(team).reset_index(inplace=False)   
    # Compute maidens
    c1= getMaidens(team).reset_index(inplace=False)   
    # Compute wickets
    d1= getWickets(team).reset_index(inplace=False)
    e1=pd.merge(a1, b1, how='outer', on='bowler')
    f1= pd.merge(e1,c1,how='outer', on='bowler')
    g1= pd.merge(f1,d1,how='outer', on='bowler')
    g1 = g1.fillna(0)
    # Compute economy rate
    g1['econrate'] = g1['runs']/g1['overs']
    g1.columns=['bowler','overs','runs','maidens','wicket','econrate']
    g1.maidens = g1.maidens.astype(int)
    g1.wicket = g1.wicket.astype(int)
    return(g1)
    
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 27 Dec 2018
# Function: teamBatsmenPartnershipMatch
# This function gets the batting partnerships
#

########################################################################################### 

def teamBatsmenPartnershipMatch(match,theTeam,opposition,plot=True):
    '''
    Team batting partnerships of batsmen in a match

    Description
    
    This function plots the partnerships of batsmen in a match against an opposition or it can return the data frame
    
    Usage
    
    teamBatsmenPartnershipMatch(match,theTeam,opposition, plot=TRUE)
    Arguments
    
    match	
    The match between the teams
    theTeam	
    The team for which the the batting partnerships are sought
    opposition	
    The opposition team
    plot	
    If plot=TRUE then a plot is created otherwise a data frame is returned
    Value
    
    df The data frame of the batsmen partnetships
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.in/

    
    See Also
    
    teamBattingScorecardMatch
    teamBowlingWicketKindMatch
    teamBatsmenVsBowlersMatch
    matchWormChart
    Examples
    teamBatsmenPartnershipMatch(kkr_sh,"Kolkata Knight Riders","Sunrisers Hyderabad",plot=True)
    m=teamBatsmenPartnershipMatch(kkr_sh,"Kolkata Knight Riders","Sunrisers Hyderabad",plot=False)
    print(m)

    '''
    df1=match.loc[match.team== theTeam]
    df2= df1[['batsman','runs','non_striker']]    
    if plot == True:
        df3=df2.groupby(['batsman','non_striker']).sum().unstack().fillna(0)
        rcParams['figure.figsize'] = 10, 6
        df3.plot(kind='bar',stacked=True)
        plt.xlabel('Batsman')
        plt.ylabel('Runs')
        plt.title(theTeam + ' -batting partnership- vs ' + opposition)
        plt.text(4, 30,'Data source-Courtesy:http://cricsheet.org',
         horizontalalignment='center',
         verticalalignment='center',
         )
        plt.show()
        plt.gcf().clear()
    else:
        df3=df2.groupby(['batsman','non_striker']).sum().reset_index(inplace=False)
        return(df3)
        
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 27 Dec 2018
# Function: teamBatsmenPartnershipMatch
# This function gives the performances of batsmen vs bowlers
#

########################################################################################### 
        
def teamBatsmenVsBowlersMatch(match,theTeam,opposition, plot=True):
    '''
    Team batsmen against bowlers in a match

    Description
    
    This function plots the performance of batsmen versus bowlers in a match or it can return the data frame
    
    Usage
    
    teamBatsmenVsBowlersMatch(match,theTeam,opposition, plot=TRUE)
    Arguments
    
    match	
    The match between the teams
    theTeam	
    The team for which the the batting partnerships are sought
    opposition	
    The opposition team
    plot	
    If plot=TRUE then a plot is created otherwise a data frame is returned
    Value
    
    b The data frame of the batsmen vs bowlers performance
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.in/
    
    See Also
    
    teamBowlingWicketKindMatch
    teamBowlingWicketMatch
    Examples
    

    teamBatsmenVsBowlersMatch(kkr_sh,"Kolkata Knight Riders","Sunrisers Hyderabad",plot=True)
    
    '''
    
    df1=match.loc[match.team== theTeam]
    df2= df1[['batsman','runs','bowler']]

    if plot == True:
        df3=df2.groupby(['batsman','bowler']).sum().unstack().fillna(0)
        df3.plot(kind='bar',stacked=True)
        rcParams['figure.figsize'] = 10, 6
        plt.xlabel('Batsman')
        plt.ylabel('Runs')
        plt.title(theTeam + ' -Batsman vs Bowler- in match against ' + opposition)
        plt.text(4, 30,'Data source-Courtesy:http://cricsheet.org',
         horizontalalignment='center',
         verticalalignment='center',
         )
        plt.show()
        plt.gcf().clear()
    else:
        df3=df2.groupby(['batsman','bowler']).sum().reset_index(inplace=False)
        return(df3)
        
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 27 Dec 2018
# Function: teamBowlingWicketKindMatch
# This function gives the wicket kind for bowlers
#

###########################################################################################
        
def teamBowlingWicketKindMatch(match,theTeam,opposition, plot=True):
    '''
    Compute and plot the wicket kinds by bowlers in match
    
    Description
    
    This function computes returns kind of wickets (caught, bowled etc) of bowlers in a match between 2 teams
    
    Usage
    
    teamBowlingWicketKindMatch(match,theTeam,opposition,plot=TRUE)
    Arguments
    
    match	
    The match between the teams
    theTeam	
    Team for which bowling performance is required
    opposition	
    The opposition team
    plot	
    If plot= TRUE the dataframe will be plotted else a data frame will be returned
    Value
    
    None or data fame A data frame with the bowling performance in alll matches against all oppositions
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.in/
    
    See Also
    
    teamBowlingWicketMatch
    teamBowlingWicketRunsMatch
    teamBowlersVsBatsmenMatch
    Examples
    teamBowlingWicketKindMatch(kkr_sh,"Kolkata Knight Riders","Sunrisers Hyderabad",plot=True)
    m=teamBowlingWicketKindMatch(kkr_sh,"Kolkata Knight Riders","Sunrisers Hyderabad",plot=False)
    print(m)
  
    '''
    df1=match.loc[match.team== theTeam]
    df2= df1[['bowler','kind','player_out']]
    # Find all rows where there was a wicket
    df3=df2[df2.player_out != '0']
    
    if plot == True:
        # Find the different types of wickets for each bowler
        df4=df3.groupby(['bowler','kind']).count().unstack().fillna(0)
        df4.plot(kind='bar',stacked=True)
        rcParams['figure.figsize'] = 10, 6
        plt.xlabel('Batsman')
        plt.ylabel('Runs')
        plt.title(theTeam + ' -Wicketkind vs Runs- given  against ' + opposition)
        plt.text(4, 30,'Data source-Courtesy:http://cricsheet.org',
         horizontalalignment='center',
         verticalalignment='center',
         )
        plt.show()
        plt.gcf().clear()
    else:
        # Find the different types of wickets for each bowler
        df4=df3.groupby(['bowler','kind']).count().reset_index(inplace=False)
        return(df4)
        
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 27 Dec 2018
# Function: teamBowlingWicketMatch
# This function gives the wickets for bowlers
#

###########################################################################################
        
def teamBowlingWicketMatch(match,theTeam,opposition, plot=True):
    '''
    Compute and plot wickets by bowlers in match
    
    Description
    
    This function computes returns the wickets taken bowlers in a match between 2 teams
    
    Usage
    
    teamBowlingWicketMatch(match,theTeam,opposition, plot=TRUE)
    Arguments
    
    match	
    The match between the teams
    theTeam	
    Team for which bowling performance is required
    opposition	
    The opposition team
    plot	
    If plot= TRUE the dataframe will be plotted else a data frame will be returned
    Value
    
    None or data fame A data frame with the bowling performance in alll matches against all oppositions
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.in/
    
    See Also
    
    teamBowlingWicketMatch
    teamBowlingWicketRunsMatch
    teamBowlersVsBatsmenMatch
    Examples
    

    teamBowlingWicketMatch(kkr_sh,"Kolkata Knight Riders","Sunrisers Hyderabad",plot=True)
    
    '''
    
    df1=match.loc[match.team== theTeam]
    df2= df1[['bowler','kind','player_out']]
    # Find all rows where there was a wicket
    df3=df2[df2.player_out != '0']
    
    if plot == True:
        # Find the different types of wickets for each bowler
        df4=df3.groupby(['bowler','player_out']).count().unstack().fillna(0)
        df4.plot(kind='bar',stacked=True)
        rcParams['figure.figsize'] = 10, 6
        plt.xlabel('Batsman')
        plt.ylabel('Runs')
        plt.title(theTeam + ' -No of Wickets vs Runs conceded- against ' + opposition)
        plt.text(1, 1,'Data source-Courtesy:http://cricsheet.org',
         horizontalalignment='center',
         verticalalignment='center',
         )
        plt.show()
        plt.gcf().clear()
    else:
        # Find the different types of wickets for each bowler
        df4=df3.groupby(['bowler','player_out']).count().reset_index(inplace=False)
        return(df4)
        
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 27 Dec 2018
# Function: teamBowlersVsBatsmenMatch
# This function gives the bowlers vs batsmen and runs conceded
#

###########################################################################################
        
def teamBowlersVsBatsmenMatch (match,theTeam,opposition, plot=True):
    '''
    Team bowlers vs batsmen in a match

    Description
    
    This function computes performance of bowlers of a team against an opposition in a match
    
    Usage
    
    teamBowlersVsBatsmenMatch(match,theTeam,opposition, plot=TRUE)
    Arguments
    
    match	
    The data frame of the match. This can be obtained with the call for e.g a <- getMatchDetails("England","Pakistan","2006-09-05",dir="../temp")
    theTeam	
    The team against which the performance is required
    opposition	
    The opposition team
    plot	
    This parameter specifies if a plot is required, If plot=FALSE then a data frame is returned
    Value
    
    None or dataframe If plot=TRUE there is no return. If plot=TRUE then the dataframe is returned
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.in/

    
    See Also
    teamBattingScorecardMatch
    teamBowlingWicketKindMatch
    matchWormChart
    Examples
    teamBowlersVsBatsmenMatch(kkr_sh,"Kolkata Knight Riders","Sunrisers Hyderabad",plot=True)

    '''
    df1=match.loc[match.team== theTeam]
    df2= df1[['batsman','runs','bowler']]
    
    if plot == True:
        df3=df2.groupby(['batsman','bowler']).sum().unstack().fillna(0)
        df3.plot(kind='bar',stacked=True)
        rcParams['figure.figsize'] = 10, 6
        plt.xlabel('Batsman')
        plt.ylabel('Runs')
        plt.title(theTeam + ' -Bowler vs Batsman- against ' + opposition)
        plt.text(4, 20,'Data source-Courtesy:http://cricsheet.org',
         horizontalalignment='center',
         verticalalignment='center',
         )
        plt.show()
        plt.gcf().clear()
    else:
        df3=df2.groupby(['batsman','bowler']).sum().reset_index(inplace=False)
        return(df3)
        
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 27 Dec 2018
# Function: matchWormChart
# This function draws the match worm chart
#
###########################################################################################
        
def matchWormChart(match,team1,team2):
    '''
    Plot the match worm graph

    Description
    
    This function plots the match worm graph between 2 teams in a match
    
    Usage
    
    matchWormGraph(match,t1,t2)
    Arguments
    
    match	
    The dataframe of the match
    team1	
    The 1st team of the match
    team2	
    the 2nd team in the match
    Value
    
    none
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.in/

    
    See Also
    teamBatsmenVsBowlersMatch
    teamBowlingWicketKindMatch
    Examples
    
    ## Not run: 
    #Get the match details
    a <- getMatchDetails("England","Pakistan","2006-09-05",dir="../temp")
    
    # Plot tne match worm plot
    matchWormChart(kkr_sh,"Kolkata Knight Riders","Sunrisers Hyderabad")
    '''
    df1=match.loc[match.team==team1]
    df2=match.loc[match.team==team2]
    
    df3=df1[['delivery','total']]
    df3['cumsum']=df3.total.cumsum()
    df4 = df2[['delivery','total']]
    df4['cumsum'] = df4.total.cumsum()
    
    df31 = df3[['delivery','cumsum']]
    df41 = df4[['delivery','cumsum']]
    #plt.plot(df3.delivery.values,df3.cumsum.values)
    df51= pd.merge(df31,df41,how='outer', on='delivery').dropna()
    df52=df51.set_index('delivery')
    df52.columns = [team1,team2]
    df52.plot()
    rcParams['figure.figsize'] = 10, 6
    plt.xlabel('Delivery')
    plt.ylabel('Runs')
    plt.title('Match worm chart ' + team1 + ' vs ' + team2)
    plt.text(10, 10,'Data source-Courtesy:http://cricsheet.org',
         horizontalalignment='center',
         verticalalignment='center',
         )
    plt.show()
    plt.gcf().clear()

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 26 Jan 2019
# Function: getAllMatchesBetweenTeams
# This function gets all the matches between 2 IPL teams
#
###########################################################################################
    
def getAllMatchesBetweenTeams(team1,team2,dir=".",save=False):
    '''
    Get data on all matches between 2 opposing teams
    
    Description
    This function gets all the data on matches between opposing IPL teams This can be saved 
    by the user which can be used in function in which analyses are done for all matches 
    between these teams.
    
    Usage
    getAllMatchesBetweenTeams(team1,team2,dir=".",save=FALSE)
    Arguments
    
    team1	
    One of the team in consideration e.g (KKR, CSK etc)
    team2	
    The other team for which matches are needed e.g( MI, GL)
    dir	
    The directory which has the RData files of matches between teams
    save	
    Default=False. This parameter indicates whether the combined data frame 
    needs to be saved or not. It is recommended to save this large dataframe as 
    the creation of this data frame takes a several seconds depending on the number of matches
    Value   
    matches - The combined data frame
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.wordpress.com/
    
    See Also
    
    plotWinsbyTossDecision
    teamBowlersVsBatsmenOppnAllMatches

    '''

    # Create the 2 combinations
    t1 = team1 +'-' + team2 + '*.csv'
    t2 = team2 + '-' + team1 + '*.csv'
    path1= os.path.join(dir1,t1)
    path2 = os.path.join(dir1,t2)
    
    files = glob.glob(path1) + glob.glob(path2)
    print(len(files))
    # Save as CSV only if there are matches between the 2 teams
    if len(files) !=0:
        df = pd.DataFrame()
        for file in files:
            df1 = pd.read_csv(file)
            df=pd.concat([df,df1])    
        if save==True:
            dest= team1 +'-' + team2 + '-allMatches.csv'    
            df.to_csv(dest)
        else:
           return(df) 
    
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 26 Jan 2019
# Function: saveAllMatchesBetween2IPLTeams
# This function saves all the matches between allIPL teams
#
###########################################################################################

def saveAllMatchesBetween2IPLTeams(dir1):  
    '''
    Saves all matches between 2 IPL teams as dataframe
    Description
   
    This function saves all matches between 2 IPL teams as a single dataframe in the 
    current directory
    
    Usage
    
    saveAllMatchesBetween2IPLTeams(dir)
    Arguments
    
    dir	
    Directory to store saved matches
    Value
    
    None
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.in/
    
    See Also
    
    teamBowlingScorecardOppnAllMatches
    teamBatsmenVsBowlersOppnAllMatches
    '''
    teams = ["Chennai Super Kings","Deccan Chargers","Delhi Daredevils",
                  "Kings XI Punjab", 'Kochi Tuskers Kerala',"Kolkata Knight Riders",
                  "Mumbai Indians", "Pune Warriors","Rajasthan Royals",
                  "Royal Challengers Bangalore","Sunrisers Hyderabad","Gujarat Lions",
                  "Rising Pune Supergiants"]
    
    for team1 in teams:
        for team2 in teams:
            if team1 != team2:
                print("Team1=",team1,"team2=", team2)
                getAllMatchesBetweenTeams(team1,team2,dir=dir1,save=True)
                time.sleep(2) #Sleep before  next save   
                
    return    

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 26 Jan 2019
# Function: teamBatsmenPartnershiOppnAllMatches
# This function gets the partnetships for a team in all matches
#
###########################################################################################       
                
def teamBatsmenPartnershiOppnAllMatches(matches,theTeam,report="summary",top=5):
    '''
    Team batting partnership against a opposition all IPL matches
    
    Description
    
    This function computes the performance of batsmen against all bowlers of an oppositions in 
    all matches. This function returns a dataframe
    
    Usage
    
    teamBatsmenPartnershiOppnAllMatches(matches,theTeam,report="summary")
    Arguments
    
    matches	
    All the matches of the team against the oppositions
    theTeam	
    The team for which the the batting partnerships are sought
    report	
    If the report="summary" then the list of top batsmen with the highest partnerships 
    is displayed. If report="detailed" then the detailed break up of partnership is returned 
    as a dataframe
    top
    The number of players to be displayed from the top
    Value
    
    partnerships The data frame of the partnerships
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.wordpress.com/

    
    See Also
    
    teamBatsmenVsBowlersOppnAllMatchesPlot
    teamBatsmenPartnershipOppnAllMatchesChart
 
    '''
    df1 = matches[matches.team == theTeam]
    df2 = df1[['batsman','non_striker','runs']]
    
    # Compute partnerships
    df3=df2.groupby(['batsman','non_striker']).sum().reset_index(inplace=False)
    df3.columns = ['batsman','non_striker','partnershipRuns']
    
    # Compute total partnerships
    df4 = df3.groupby('batsman').sum().reset_index(inplace=False).sort_values('partnershipRuns',ascending=False)
    df4.columns = ['batsman','totalPartnershipRuns']
    
    # Select top 5
    df5 = df4.head(top)    
    df6= pd.merge(df5,df3,on='batsman')
    
    if report == 'summary':
       return(df5)
    elif report == 'detailed':
       return(df6)
    else:
         print("Invalid option")     
         
    return

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 26 Jan 2019
# Function: teamBatsmenPartnershipOppnAllMatchesChart
# This function plots the partnetships for a team in all matches
#
###########################################################################################       
    
def teamBatsmenPartnershipOppnAllMatchesChart(matches,main,opposition,plot=True,top=5,partnershipRuns=20):
    '''
    Plot of team partnership in all IPL matches against an opposition
    
    Description
    
    This function plots the batting partnership of a team againt all oppositions in all
    matches This function also returns a dataframe with the batting partnerships
    
    Usage
    
    teamBatsmenPartnershipOppnAllMatchesChart(matches,main,opposition, plot=TRUE,top=5,partnershipRuns=20))
    Arguments
    
    matches	
    All the matches of the team against all oppositions
    main	
    The main team for which the the batting partnerships are sought
    opposition	
    The opposition team for which the the batting partnerships are sought
    plot	
    Whether the partnerships have top be rendered as a plot. If plot=FALSE the data frame is returned
    top
    The number of players from the top to be included in chart
    partnershipRuns
    The minimum number of partnership runs to include for the chart
    Value
    
    None or partnerships
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.wordpress.com/

    
    See Also
    
    teamBatsmenPartnershiplOppnAllMatches
    saveAllMatchesBetween2IPLTeams
    teamBatsmenVsBowlersAllOppnAllMatchesPlot
    teamBatsmenVsBowlersOppnAllMatches    
    '''
    df1 = matches[matches.team == main]
    df2 = df1[['batsman','non_striker','runs']]
    
    # Compute partnerships
    df3=df2.groupby(['batsman','non_striker']).sum().reset_index(inplace=False)
    df3.columns = ['batsman','non_striker','partnershipRuns']
    
    # Compute total partnerships
    df4 = df3.groupby('batsman').sum().reset_index(inplace=False).sort_values('partnershipRuns',ascending=False)
    df4.columns = ['batsman','totalPartnershipRuns']
    
    
    # Select top 5
    df5 = df4.head(top)    
    df6= pd.merge(df5,df3,on='batsman')
    df7 = df6[['batsman','non_striker','partnershipRuns']]
 
    # Remove rows where partnershipRuns < partnershipRuns as there are too many
    df8 = df7[df7['partnershipRuns'] > partnershipRuns]
    
    df9=df8.groupby(['batsman','non_striker'])['partnershipRuns'].sum().unstack().fillna(0)
    # Note: Can also use the below code -*************
    #df8=df7.pivot(columns='non_striker',index='batsman').fillna(0)
 

    if plot == True:
       df9.plot(kind='bar',stacked=True,legend=False,fontsize=8)
       plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5),fontsize=8)
       plt.title('Partnership runs bby batsmen of  ' + main + ' against ' + opposition)
       plt.xlabel('Batsman')
       plt.ylabel('Partnership runs')   
       plt.show()
       plt.gcf().clear()
    else:
        return(df7)
        
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 26 Jan 2019
# Function: teamBatsmenVsBowlersOppnAllMatches
# This function plots the performance of batsmen against bowlers
#
###########################################################################################    
        
def teamBatsmenVsBowlersOppnAllMatches(matches,main,opposition,plot=True,top=5,runsScored=20):
    '''
    Description

    This function computes the performance of batsmen against the bowlers of an oppositions in all matches
    
    Usage
    
    teamBatsmenVsBowlersOppnAllMatches(matches,main,opposition,plot=TRUE,top=5,runsScored=20)
    Arguments
    
    matches	
    All the matches of the team against one specific opposition
    main	
    The team for which the the batting partnerships are sought
    opposition	
    The opposition team
    plot	
    If plot=True then a plot will be displayed else a data frame will be returned
    top	
    The number of players to be plotted or returned as a dataframe. The default is 5
    runsScored
    The cutfoff limit for runs scored for runs scored against bowler
    Value
    
    None or dataframe
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.wordpress.com/

    
    See Also
    
    teamBatsmenVsBowlersOppnAllMatchesPlot
    teamBatsmenPartnershipOppnAllMatchesChart
    teamBatsmenVsBowlersOppnAllMatches   
    '''
    df1 = matches[matches.team == main]
    df2 = df1[['batsman','bowler','runs']]
    
    # Runs scored by bowler
    df3=df2.groupby(['batsman','bowler']).sum().reset_index(inplace=False)
    df3.columns = ['batsman','bowler','runsScored']
    
    # Need to pick the 'top' number of bowlers
    df4 = df3.groupby('batsman').sum().reset_index(inplace=False).sort_values('runsScored',ascending=False)
    df4.columns = ['batsman','totalRunsScored']
    df5 = df4.head(top)
    df6= pd.merge(df5,df3,on='batsman')
    df7 = df6[['batsman','bowler','runsScored']]
    
    # Remove rows where runsScored < runsScored as there are too many
    df8 = df7[df7['runsScored'] >runsScored]
    df9=df8.groupby(['batsman','bowler'])['runsScored'].sum().unstack().fillna(0)
    # Note: Can also use the below code -*************
    #df8=df7.pivot(columns='bowler',index='batsman').fillna(0)
    
    if plot == True:
        ax=df9.plot(kind='bar',stacked=False,legend=False,fontsize=8)
        plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5),fontsize=8)
        plt.title('Runs by batsmen of  ' + main + ' against bowler of ' + opposition)
        plt.xlabel('Batsman')
        plt.ylabel('Runs scored') 
        plt.show()
        plt.gcf().clear()
    else:
        return(df7)
        
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 26 Jan 2019
# Function: teamBattingScorecardOppnAllMatches
# This function computes the batting scorecard for all matches
#
########################################################################################### 

def teamBattingScorecardOppnAllMatches(matches,main,opposition):
    '''
    Team batting scorecard of a team in all matches against an opposition
    
    Description
    
    This function computes returns the batting scorecard (runs, fours, sixes, balls played) 
    for the team in all matches against an opposition
    
    Usage
    
    teamBattingScorecardOppnAllMatches(matches,main,opposition)
    Arguments
    
    matches	
    the data frame of all matches between a team and an opposition obtained with the call getAllMatchesBetweenteam()
    main	
    The main team for which scorecard required
    opposition	
    The opposition team
    Value
    
    scorecard The scorecard of all the matches
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.wordpress.com/
    
    See Also
    
    teamBatsmenPartnershipAllOppnAllMatches
    teamBowlingWicketKindOppositionAllMatches    
    '''
    team=matches.loc[matches.team== main]
    a1= getRuns(team)
    b1= getFours(team)
    c1= getSixes(team)
    
    # Merge columns
    d1=pd.merge(a1, b1, how='outer', on='batsman')
    e=pd.merge(d1,c1,how='outer', on='batsman')
    e=e.fillna(0)
    
    e['4s']=e['4s'].astype(int)
    e['6s']=e['6s'].astype(int)
    e['SR']=(e['runs']/e['balls']) *100
    scorecard = e[['batsman','runs','balls','4s','6s','SR']].sort_values('runs',ascending=False)
    return(scorecard)   

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 26 Jan 2019
# Function: teamBattingScorecardOppnAllMatches
# This function computes the batting scorecard for all matches
#
########################################################################################### 
def teamBowlingScorecardOppnAllMatches(matches,main,opposition):
    '''
    Team bowling scorecard opposition all matches
    
    Description
    
    This function computes returns the bowling dataframe of best bowlers
    deliveries, maidens, overs, wickets against an IPL oppositions in all matches
    
    Usage
    
    teamBowlingScorecardOppnAllMatches(matches,main,opposition)
    Arguments
    
    matches	
    The matches of the team against all oppositions and all matches
    main	
    Team for which bowling performance is required
    opposition
    The opposing  IPL team
    Value
    
    l A data frame with the bowling performance in alll matches against all oppositions
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.wordpress.com/
    
    See Also
    teamBowlingWicketKindOppositionAllMatches
    teamBatsmenVsBowlersOppnAllMatches
    plotWinsbyTossDecision
    '''
    team=matches.loc[matches.team== main] 
    # Compute overs bowled
    a1= getOvers(team).reset_index(inplace=False)
    # Compute runs conceded
    b1= getRunsConceded(team).reset_index(inplace=False)   
    # Compute maidens
    c1= getMaidens(team).reset_index(inplace=False)   
    # Compute wickets
    d1= getWickets(team).reset_index(inplace=False)
    e1=pd.merge(a1, b1, how='outer', on='bowler')
    f1= pd.merge(e1,c1,how='outer', on='bowler')
    g1= pd.merge(f1,d1,how='outer', on='bowler')
    g1 = g1.fillna(0)
    # Compute economy rate
    g1['econrate'] = g1['runs']/g1['overs']
    g1.columns=['bowler','overs','runs','maidens','wicket','econrate']
    g1.maidens = g1.maidens.astype(int)
    g1.wicket = g1.wicket.astype(int)
    g2 = g1.sort_values('wicket',ascending=False)
    return(g2)
    
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 26 Jan 2019
# Function: teamBowlingWicketKindOppositionAllMatches
# This function plots the performance of bowlers and the kind of wickets
#
########################################################################################### 
    
def teamBowlingWicketKindOppositionAllMatches(matches,main,opposition,plot=True,top=5,wickets=2):
    '''
    Team bowlers wicket kind against an opposition in all matches
    
    Description
    
    This function computes performance of bowlers of a team and the wicket kind against 
    an opposition in all matches against the opposition
    
    Usage
    
    teamBowlersWicketKindOppnAllMatches(matches,main,opposition,plot=TRUE,top=5,wickets=2)
    Arguments
    
    matches	
    The data frame of all matches between a team the opposition. T
    main	
    The team for which the performance is required
    opposition	
    The opposing team
    plot	
    If plot=True then a plot is displayed else a dataframe is returned
    top
    The top number of players to be considered
    wickets
    The minimum number of wickets as cutoff
    Value
    
    None or dataframe The return depends on the value of the plot
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.wordpress.com/

    
    See Also
    
    plotWinsByRunOrWickets 
    teamBowlersVsBatsmenOppnAllMatches
    '''
    df1=matches.loc[matches.team== main]
    df2= df1[['bowler','kind','player_out']]

    # Find all rows where there was a wicket
    df2=df2[df2.player_out != '0']
    
    # Number of wickets taken by bowler
    df3=df2.groupby(['bowler','kind']).count().reset_index(inplace=False)
    df3.columns = ['bowler','kind','wickets']
    
    # Need to pick the 'top' number of bowlers by wickets
    df4 = df3.groupby('bowler').sum().reset_index(inplace=False).sort_values('wickets',ascending=False)
    df4.columns = ['bowler','totalWickets']
    df5 = df4.head(top)
    df6= pd.merge(df5,df3,on='bowler')
    df7 = df6[['bowler','kind','wickets']]
    
    
    # Remove rows where runsScored < runsScored as there are too many
    df8 = df7[df7['wickets'] >wickets]
    df9=df8.groupby(['bowler','kind'])['wickets'].sum().unstack().fillna(0)   
    # Note: Can also use the below code -*************
    #df9=df8.pivot(columns='bowler',index='batsman').fillna(0)

    if plot == True:
        ax=df9.plot(kind='bar',stacked=False,legend=False,fontsize=8)
        plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5),fontsize=8)
        plt.title('Wicker kind by bowlers of ' + main + ' against ' + opposition)
        plt.xlabel('Bowler')
        plt.ylabel('Total wickets') 
        plt.show()
        plt.gcf().clear()
    else:
        return(df7)
        
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 26 Jan 2019
# Function: teamBowlersVsBatsmenOppnAllMatches
# This function plots the performance of the bowlers against batsmen
#
########################################################################################### 
def teamBowlersVsBatsmenOppnAllMatches(matches,main,opposition,plot=True,top=5,runsConceded=10):
    '''
    Team bowlers vs batsmen against an opposition in all matches

    Description
    
    This function computes performance of bowlers of a team against an opposition in all 
    matches against the opposition
    
    Usage
    
    teamBowlersVsBatsmenOppnAllMatches(matches,main,opposition,plot=True,top=5,runsConceded=10))
    Arguments
    
    matches	
    The data frame of all matches between a team the opposition. 
    
    main	
    The main team against which the performance is required
    opposition	
    The opposition team against which the performance is require
    plot	
    If true plot else return dataframe
    top	
    The number of rows to be returned. 5 by default
    runsConceded
    The minimum numer runs to use as cutoff
    Value
    
    dataframe The dataframe with all performances
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.wordpress.com/

    
    See Also
    
    teamBatsmenPartnershipOppnAllMatches
    teamBowlersVsBatsmenOppnAllMatchesRept

    '''
    df1=matches.loc[matches.team== main]
    df2= df1[['bowler','batsman','runs']]
    
    # Number of wickets taken by bowler
    df3=df2.groupby(['bowler','batsman']).sum().reset_index(inplace=False)
    df3.columns = ['bowler','batsman','runsConceded']
    
    # Need to pick the 'top' number of bowlers by wickets
    df4 = df3.groupby('bowler').sum().reset_index(inplace=False).sort_values('runsConceded',ascending=False)
    df4.columns = ['bowler','totalRunsConceded']
    df5 = df4.head(top)
    df6= pd.merge(df5,df3,on='bowler')
    df7 = df6[['bowler','batsman','runsConceded']]
    
    
    # Remove rows where runsScored < runsScored as there are too many
    df8 = df7[df7['runsConceded'] >runsConceded]
    df9=df8.groupby(['bowler','batsman'])['runsConceded'].sum().unstack().fillna(0)   
    # Note: Can also use the below code -*************
    #df9=df8.pivot(columns='bowler',index='batsman').fillna(0)
    
    if plot == True:
        ax=df9.plot(kind='bar',stacked=False,legend=False,fontsize=8)
        plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5),fontsize=8)
        plt.title('Performance of  bowlers of ' + main + ' against ' + opposition)
        plt.xlabel('Bowler')
        plt.ylabel('Total runs') 
        plt.show()
        plt.gcf().clear()
    else:
        return(df7)
        
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 26 Jan 2019
# Function: plotWinLossBetweenTeams
# This function plots the number of wins and losses in teams
#
########################################################################################### 
def plotWinLossBetweenTeams(matches,team1,team2):
    '''
    Plot wins for each team
    
    Description
    
    This function computes and plots number of wins for each team in all their encounters. 
    The plot includes the number of wins byteam1 each team and the matches with no result
    
    Usage
    
    plotWinLossBetweenTeams(matches)
    Arguments
    
    matches
    The dataframe with all matches between 2 IPL teams
    team1
    The 1st team
    team2
    The 2nd team
    Value
    
    None
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.wordpress.com/
    https://github.com/tvganesh/yorkrData
    
    See Also
    
    teamBattingScorecardOppnAllMatches
    teamBatsmenPartnershipOppnAllMatchesChart
    getAllMatchesBetweenTeams
    '''
    a=matches[['date','winner']].groupby(['date','winner']).count().reset_index(inplace=False)
    b=a.groupby('winner').count().reset_index(inplace=False)
    b.columns = ['winner','number']
    sns.barplot(x='winner',y='number',data=b)
    plt.xlabel('Winner')
    plt.ylabel('Number')
    plt.title("Wins vs losses " +  team1 + "-"+ team2)
    plt.show()
    plt.gcf().clear()
    return
    
    
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 26 Jan 2019
# Function: plotWinsByRunOrWickets
# This function plots how the win for the team was whether by runs or wickets
#
########################################################################################### 
def plotWinsByRunOrWickets(matches,team1):
    '''

    Plot whether the wins for the team was by runs or wickets
    
    Description
    
    This function computes and plots number the number of wins by runs vs number of wins
    by wickets
    
    Usage
    
    plotWinsByRunOrWickets(matches,team1)
    Arguments
    
    matches
    The dataframe with all matches between 2 IPL teams
    
    team1
    The team for which the plot has to be done
    Value
    
    None
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.wordpress.com/

    
    See Also
    
    teamBowlingScorecardOppnAllMatches
    teamBatsmenPartnershipOppnAllMatchesChart
    getAllMatchesBetweenTeams    
    '''
    # Get the number of matches won
    df= matches.loc[matches.winner == team1]
    a=df[['date','winType']].groupby(['date','winType']).count().reset_index(inplace=False)
    b=a.groupby('winType').count().reset_index(inplace=False)
    b.columns = ['winType','number']
    sns.barplot(x='winType',y='number',data=b)
    plt.xlabel('Win Type - Runs or wickets')
    plt.ylabel('Number')
    plt.title("Win type for team -" +  team1 )
    plt.show()
    plt.gcf().clear()
    return
 
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 26 Jan 2019
# Function: plotWinsbyTossDecision
# This function plots the number of wins/losses for team based on its toss decision
#
########################################################################################### 
def plotWinsbyTossDecision(matches,team1,tossDecision='bat'):
    '''
   Plot whether the wins for the team was by runs or wickets
    
    Description
    
    This function computes and plots number the number of wins by runs vs number of wins
    by wickets
    
    Usage
    
    plotWinsbyTossDecision(matches,team1,tossDecision='bat')
    Arguments
    
    matches
    The dataframe with all matches between 2 IPL teams
    
    team1
    The team for which the plot has to be done
    Value
    
    None
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.wordpress.com/

    
    See Also
    
    teamBowlingScorecardOppnAllMatches
    teamBatsmenPartnershipOppnAllMatchesChart
    teamBowlingWicketKindOppositionAllMatches       
    '''
    df=matches.loc[(matches.tossDecision==tossDecision) & (matches.tossWinner==team1)]
    a=df[['date','winner']].groupby(['date','winner']).count().reset_index(inplace=False)
    b=a.groupby('winner').count().reset_index(inplace=False)
    b.columns = ['winner','number']
    sns.barplot(x='winner',y='number',data=b)
    plt.xlabel('Winner ' + 'when toss decision was to :' + tossDecision)
    plt.ylabel('Number')
    plt.title('Wins vs losses for ' + team1 + ' when toss decision was to ' + tossDecision )
    plt.show()
    plt.gcf().clear()
    return