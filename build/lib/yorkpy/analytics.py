import os
import yaml
import json
import pandas as pd
import matplotlib.pyplot as plt
from pylab import rcParams
import seaborn as sns
import numpy as np
from sklearn.linear_model import LinearRegression
import glob
import time

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
        
        df['result']=a['info']['outcome']['result']
        df['resultHow']=list(a['info']['outcome'].keys())[0]
        df['resultTeam'] = a['info']['outcome']['eliminator']
        print(a['info']['outcome']['result'])
        print(list(a['info']['outcome'].keys())[0])
        print(a['info']['outcome']['eliminator'])
        
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
    if (type(a['info']['dates'][0]) == str):
       outfile=a['info']['teams'][0]+ '-' + a['info']['teams'][1] + '-' +a['info']['dates'][0] + '.csv'
    else:  
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
             df, filename = convertYaml2PandasDataframeT20(file, source, dest)
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
    scorecard=pd.DataFrame()
    if(match.size != 0):
      team=match.loc[match['team'] == theTeam]
    else:
      return(scorecard,-1)
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
    
    # Check if the team took wickets. Then this column will be a string
    if isinstance(df1.player_out.iloc[0],str):
        df2= df1[df1.player_out !='0']
        df3 = df2[['bowler','player_out']].groupby('bowler').count()
    else: # Did not take wickets. Set wickets as 0
        df3 = df1[['bowler','player_out']].groupby('bowler').count()
        df3['player_out']=0 # Set wicktes as 0

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

def teamBatsmenPartnershipMatch(match,theTeam,opposition,plot=True,savePic=False, dir1=".",picFile="pic1.png"):
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
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
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
        
def teamBatsmenVsBowlersMatch(match,theTeam,opposition, plot=True, savePic=False, dir1=".",picFile="pic1.png"):
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
    If plot=TRUE then a plot is created otherwise a data frame is return
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
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
        
def teamBowlingWicketKindMatch(match,theTeam,opposition, plot=True,savePic=False, dir1=".",picFile="pic1.png"):
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
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile))
        else:
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
        
def teamBowlingWicketMatch(match,theTeam,opposition, plot=True,savePic=False, dir1=".",picFile="pic1.png"):
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
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
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
        
def teamBowlersVsBatsmenMatch (match,theTeam,opposition, plot=True, savePic=False, dir1=".",picFile="pic1.png"):
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
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
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
        
def matchWormChart(match,team1,team2,plot=True, savePic=False, dir1=".",picFile="pic1.png"):
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
    plot	
    If plot=TRUE then a plot is created otherwise a data frame is returned
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
    if plot == True:
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
    plt.gcf().clear()

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 26 Jan 2019
# Function: getAllMatchesBetweenTeams
# This function gets all the matches between 2 IPL teams
#
###########################################################################################
    
def getAllMatchesBetweenTeams(team1,team2,dir=".",save=False,odir="."):
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
    path1= os.path.join(dir,t1)
    path2 = os.path.join(dir,t2)
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
            output=os.path.join(odir,dest)
            df.to_csv(output)
        else:
           return(df) 
    
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 26 Jan 2019
# Function: saveAllMatchesBetween2IPLTeams
# This function saves all the matches between allIPL teams
#
###########################################################################################

def saveAllMatchesBetween2IPLTeams(dir1,odir="."):  
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
                getAllMatchesBetweenTeams(team1,team2,dir=dir1,save=True,odir=odir)
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
    
def teamBatsmenPartnershipOppnAllMatchesChart(matches,main,opposition,plot=True,top=5,partnershipRuns=20,avePic=False, dir1=".",picFile="pic1.png"):
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
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
       plt.title('Partnership runs between ' + main + '-' + opposition)
       plt.xlabel('Batsman')
       plt.ylabel('Partnership runs')  
       if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
       else:
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
        
def teamBatsmenVsBowlersOppnAllMatches(matches,main,opposition,plot=True,top=5,runsScored=20,savePic=False, dir1=".",picFile="pic1.png"):
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
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
        plt.title('Runs against bowlers ' + main + '-' + opposition)
        plt.xlabel('Batsman')
        plt.ylabel('Runs scored') 
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
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
    
def teamBowlingWicketKindOppositionAllMatches(matches,main,opposition,plot=True,top=5,wickets=2,savePic=False, dir1=".",picFile="pic1.png"):
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
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
        plt.title('Wicker kind by bowlers of ' + main + '-' + opposition)
        plt.xlabel('Bowler')
        plt.ylabel('Total wickets') 
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
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
def teamBowlersVsBatsmenOppnAllMatches(matches,main,opposition,plot=True,top=5,runsConceded=10, savePic=False, dir1=".",picFile="pic1.png"):
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
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
        plt.title('Wicker kind by bowlers of ' + main + '-' + opposition)
        plt.xlabel('Bowler')
        plt.ylabel('Total runs') 
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
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
def plotWinLossBetweenTeams(matches,team1,team2,plot=True, savePic=False, dir1=".",picFile="pic1.png"):
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
    plot	
    If plot=TRUE then a plot is created otherwise a data frame is returned
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
    if(plot==True):
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
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
def plotWinsByRunOrWickets(matches,team1,plot=True, savePic=False, dir1=".",picFile="pic1.png"):
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
    
    plot	
    If plot=TRUE then a plot is created otherwise a data frame is returned
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
    if(plot==True):
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
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
def plotWinsbyTossDecision(matches,team1,tossDecision='bat', plot=True, savePic=False, dir1=".",picFile="pic1.png"):
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

    plot	
    If plot=TRUE then a plot is created otherwise a data frame is returned
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
    
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
    if(plot==True):
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
    plt.gcf().clear()
    return

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 1 Feb 2019
# Function: getAllMatchesAllOpposition
# This function gets all the matches between a IPL team and all opposition
#
########################################################################################### 
def getAllMatchesAllOpposition(team1,dir=".",save=False,odir="."):
    '''
    Get data on all matches against all opposition
    
    Description
    
    This function gets all the matches for a particular IPL team for
    against all other oppositions.  It constructs a huge dataframe of 
    all these matches. This can be saved by the user which can be used in 
    function in which analyses are done for all matches and for all oppositions. 

    
    Usage
    
    getAllMatchesAllOpposition(team,dir=".",save=FALSE)
    Arguments
    
    team	
    The team for which all matches and all opposition has to be obtained e.g. India, Pakistan
    dir	
    The directory in which the saved .RData files exist
    save	
    Default=False. This parameter indicates whether the combined data frame needs to be saved or not. It is recommended to save this large dataframe as the creation of this data frame takes a several seconds depending on the number of matches
    Value
    
    match The combined data frame
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.wordpress.com/

    
    See Also
    
    saveAllMatchesAllOppositionIPLT20
    teamBatsmenPartnershiAllOppnAllMatches  
    '''

    # Create the 2 combinations
    t1 = '*' +  team1 +'*.csv'
    path= os.path.join(dir,t1)

    
    files = glob.glob(path) 
    print(len(files))
    # Save as CSV only if there are matches between the 2 teams
    if len(files) !=0:
        df = pd.DataFrame()
        for file in files:
            df1 = pd.read_csv(file)
            df=pd.concat([df,df1])    
        if save==True:
            dest= team1 + '-allMatchesAllOpposition.csv'    
            output=os.path.join(odir,dest)
            df.to_csv(output)
        else:
           return(df)
           
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 1 Feb 2019
# Function: saveAllMatchesAllOppositionIPLT20
# This function saves all the matches between all IPL team and all opposition
#
########################################################################################### 
def saveAllMatchesAllOppositionIPLT20(dir1,odir="."):  
    '''
    Saves matches against all IPL teams as dataframe and CSV for an IPL team
    
    Description
    
    This function saves all IPL matches agaist all opposition as a single 
    dataframe in the current directory
    
    Usage
    
    saveAllMatchesAllOppositionIPLT20(dir)
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
    https://gigadom.wordpress.com/

    
    See Also
    
    convertYaml2PandasDataframeT20
    teamBattingScorecardMatch 
    '''
    teams = ["Chennai Super Kings","Deccan Chargers","Delhi Daredevils",
                  "Kings XI Punjab", 'Kochi Tuskers Kerala',"Kolkata Knight Riders",
                  "Mumbai Indians", "Pune Warriors","Rajasthan Royals",
                  "Royal Challengers Bangalore","Sunrisers Hyderabad","Gujarat Lions",
                  "Rising Pune Supergiants"]
    
    for team in teams:
                print("Team=",team)
                getAllMatchesAllOpposition(team,dir=dir1,save=True,odir=odir)
                time.sleep(2) #Sleep before  next save
                
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 1 Feb 2019
# Function: teamBatsmenPartnershiAllOppnAllMatches
# This function computes the partnerships of an IPK team against all other IPL teams
#
########################################################################################### 
def teamBatsmenPartnershiAllOppnAllMatches(matches,theTeam,report="summary",top=5):
    '''
    Team batting partnership against a opposition all IPL matches
    
    Description
    
    This function computes the performance of batsmen against all bowlers of an oppositions in 
    all matches. This function returns a dataframe
    
    Usage
    
    teamBatsmenPartnershiAllOppnAllMatches(matches,theTeam,report="summary")
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
         
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 1 Feb 2019
# Function: teamBatsmenPartnershipAllOppnAllMatchesChart
# This function computes and plots the partnerships of an IPK team against all other IPL teams
#
########################################################################################### 
def teamBatsmenPartnershipAllOppnAllMatchesChart(matches,main,plot=True,top=5,partnershipRuns=20, savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Plots team batting partnership all matches all oppositions
    
    Description
    
    This function plots the batting partnership of a team againt all oppositions in all matches This function also returns a dataframe with the batting partnerships
    
    Usage
    
    teamBatsmenPartnershipAllOppnAllMatchesChart(matches,theTeam,main,plot=True,top=5,partnershipRuns=20)
    Arguments
    
    matches	
    All the matches of the team against all oppositions
    theTeam	
    The team for which the the batting partnerships are sought
    main	
    The main team for which the the batting partnerships are sought
    plot	
    Whether the partnerships have top be rendered as a plot. If plot=FALSE the data frame is returned
    
    top
    The number of players from the top to be included in chart
    partnershipRuns
    The minimum number of partnership runs to include for the chart
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
    Value
    
    None or partnerships
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.wordpress.com/
   
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
    
    df9=df8.groupby(['batsman','non_striker'])['partnershipRuns'].sum().unstack(fill_value=0)
    # Note: Can also use the below code -*************
    #df8=df7.pivot(columns='non_striker',index='batsman').fillna(0)
 

    if plot == True:
       df9.plot(kind='bar',stacked=True,legend=False,fontsize=8)
       plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5),fontsize=8)
       plt.title('Batting partnerships  of' + main + 'against all teams')
       plt.xlabel('Batsman')
       plt.ylabel('Partnership runs') 
       if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
       else:
            plt.show()

       plt.gcf().clear()
    else:
        return(df7)

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 1 Feb 2019
# Function: teamBatsmenVsBowlersAllOppnAllMatches
# This function computes and plots the performance of batsmen
# of an IPL team against all other teams
#
########################################################################################### 
def teamBatsmenVsBowlersAllOppnAllMatches(matches,main,plot=True,top=5,runsScored=20, savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Report of team batsmen vs bowlers in all matches all oppositions

    Description
    
    This function computes the performance of batsmen against all bowlers of all oppositions in all matches
    
    Usage
    
    teamBatsmenVsBowlersAllOppnAllMatches(matches,main,plot=True,top=5,runsScored=20)
    Arguments
    
    matches	
    All the matches of the team against all oppositions
    main
    The team for which the the batting partnerships are sought
    plot	
    Whether a plot is required or not
    top
    The number of top batsmen to be included
    runsScored
    The total runs scoed by batsmen
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
    Value
    
    The data frame of the batsman and the runs against bowlers
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.wordpress.com/

    '''

    df1 = matches[matches.team == main]
    df2 = df1[['batsman','bowler','runs']]
    
    # Runs scored by bowler
    df3=df2.groupby(['batsman','bowler']).sum().reset_index(inplace=False)
    df3.columns = ['batsman','bowler','runsScored']
    print(df3.shape)
    # Need to pick the 'top' number of bowlers
    df4 = df3.groupby('batsman').sum().reset_index(inplace=False).sort_values('runsScored',ascending=False)
    print(df4.shape)
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
        #ax.legend(fontsize=25)
        plt.title('Runs by ' + main + ' against all T20 bowlers')
        plt.xlabel('Batsman')
        plt.ylabel('Runs scored') 
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
        plt.gcf().clear()
    else:
        return(df7)
        
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 1 Feb 2019
# Function: teamBattingScorecardAllOppnAllMatches
# This function computes and batting scorecard of an IPL team against all other 
# IPL teams
#
########################################################################################### 
        
def teamBattingScorecardAllOppnAllMatches(matches,main):
    '''
    Team batting scorecard against all oppositions in all matches
    
    Description
    
    This function omputes and returns the batting scorecard of a team in all matches against all oppositions. The data frame has the ball played, 4's,6's and runs scored by batsman
    
    Usage
    
    teamBattingScorecardAllOppnAllMatches(matches,theTeam)
    Arguments
    
    matches	
    All matches of the team in all matches with all oppositions
    main	
    The team for which the the batting partnerships are sought
    Value
    
    details The data frame of the scorecard of the team in all matches against all oppositions
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.wordpress.com/    
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
# Date : 1 Feb 2019
# Function: teamBowlingScorecardAllOppnAllMatches
# This function computes and bowling scorecard of an IPL team against all other 
# IPL teams
#
###########################################################################################
def teamBowlingScorecardAllOppnAllMatches(matches,main):
    '''
    Team bowling scorecard all opposition all matches

    Description
    
    This function computes returns the bowling dataframe of bowlers deliveries,
    maidens, overs, wickets against all oppositions in all matches
    
    Usage
    
    teamBowlingScorecardAllOppnAllMatches(matches,theTeam)
    Arguments
    
    matches	
    The matches of the team against all oppositions and all matches
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
    https://gigadom.wordpress.com/
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
# Date : 1 Feb 2019
# Function: teamBowlingWicketKindAllOppnAllMatches
# This function computes and plots the wicket kind of an IPL team against all other 
# IPL teams
#
###########################################################################################
def teamBowlingWicketKindAllOppnAllMatches(matches,main,plot=True,top=5,wickets=2,savePic=False, dir1=".",picFile="pic1.png"):
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
        plt.title('Wicker kind by bowlers of ' + main + ' against all T20 teams')
        plt.xlabel('Bowler')
        plt.ylabel('Total wickets') 
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
        plt.gcf().clear()
    else:
        return(df7)

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 1 Feb 2019
# Function: teamBowlersVsBatsmenAllOppnAllMatches
# This function computes and plots the performance of bowlers of an IPL team against all other 
# IPL teams
#
###########################################################################################
def teamBowlersVsBatsmenAllOppnAllMatches(matches,main,plot=True,top=5,runsConceded=10,savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Compute team bowlers vs batsmen all opposition all matches
    
    Description
    
    This function computes performance of bowlers of a team against all opposition in all matches
    
    Usage
    
    teamBowlersVsBatsmenAllOppnAllMatches(matches,,main,plot=True,top=5,runsConceded=10)
    Arguments
    
    matches	
    the data frame of all matches between a team and aall opposition and all obtained with the call getAllMatchesAllOpposition()
    main	
    The team against which the performance is requires
    plot	
    Whether a plot should be displayed or a dataframe to be returned
    top
    The top number of bowlers in result
    runsConded
    The number of runs conceded by bowlers
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
    Value
    
    dataframe The dataframe with all performances
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.wordpress.com/    
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
        plt.title('Performance of' + main  + 'Bowlers vs Batsmen ' )
        plt.xlabel('Bowler')
        plt.ylabel('Total runs')
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
        plt.gcf().clear()
    else:
        return(df7)
        
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 1 Feb 2019
# Function: plotWinLossByTeamAllOpposition
# This function computes and plots twins and lossed of  IPL team against all other 
# IPL teams
#
###########################################################################################
def plotWinLossByTeamAllOpposition(matches, team1, plot='summary',savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Plot wins for each team
    
    Description
    
    This function computes and plots number of wins for each team in all their encounters. 
    The plot includes the number of wins byteam1 each team and the matches with no result
    
    Usage
    
    plotWinLossByTeamAllOpposition(matches, main, plot='summary')
    Arguments
    
    matches
    The dataframe with all matches between 2 IPL teams
    main
    The 1st team
    plot
    Summary or detailed
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
    Value
    
    None
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.wordpress.com/
    '''
    a=matches[['date','winner']].groupby(['date','winner']).count().reset_index(inplace=False)
    # Plot the overall performance as wins and losses
    if plot=="summary":
        m= a.loc[a.winner==team1]['winner'].count()
        n= a.loc[a.winner!=team1]['winner'].count()
        df=pd.DataFrame({'outcome':['win','loss'],'number':[m,n]})
        sns.barplot(x='outcome',y='number',data=df)
        plt.xlabel('Outcome')
        plt.ylabel('Number')
        plt.title("Wins vs losses(summary) of " +  team1 + ' against all Opposition' )
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
        plt.gcf().clear()
    elif plot=="detailed" : 
        #Plot breakup by team
        b=a.groupby('winner').count().reset_index(inplace=False)
        # If 'winner' is '0' then the match is a tie.Set as 'tie'
        b.loc[b.winner=='0','winner']='Tie'
        b.columns = ['winner','number']
        ax=sns.barplot(x='winner',y='number',data=b)
        plt.xlabel('Winner')
        plt.ylabel('Number')
        plt.title("Wins vs losses(detailed) of " +  team1 + ' against all Opposition' )
        ax.set_xticklabels(ax.get_xticklabels(),rotation=60,fontsize=6)
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
        plt.gcf().clear()
    else:
        print("Unknown option")
        
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 1 Feb 2019
# Function: plotWinsByRunOrWicketsAllOpposition
# This function computes and plots twins and lossed of  IPL team against all other 
# IPL teams
#
###########################################################################################
def plotWinsByRunOrWicketsAllOpposition(matches,team1,plot=True, savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Plot whether the wins for the team was by runs or wickets
    
    Description
    
    This function computes and plots number the number of wins by runs vs number of wins
    by wickets against all Opposition
    
    Usage
    
    plotWinsByRunOrWicketsAllOpposition(matches,team1)
    Arguments
    
    matches
    The dataframe with all matches between an IPL team and all IPL teams
    
    team1
    The team for which the plot has to be done
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
    Value
    
    None
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.wordpress.com/   
    '''
    # Get the number of matches won
    df= matches.loc[matches.winner == team1]
    a=df[['date','winType']].groupby(['date','winType']).count().reset_index(inplace=False)
    b=a.groupby('winType').count().reset_index(inplace=False)
    b.columns = ['winType','number']
    sns.barplot(x='winType',y='number',data=b)
    plt.xlabel('Win Type - Runs or wickets')
    plt.ylabel('Number')
    plt.title("Win type for team -" +  team1 + ' against all opposition' )
    if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
    else:
            plt.show()
    plt.gcf().clear()
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 1 Feb 2019
# Function: plotWinsbyTossDecisionAllOpposition
# This function computes and plots the win type of IPL team against all 
# IPL teams
#
###########################################################################################
def plotWinsbyTossDecisionAllOpposition(matches,team1,tossDecision='bat',plot="summary", savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Plot whether the wins for the team was by runs or wickets
    
    Description
    
    This function computes and plots number the number of wins by runs vs number of wins
    by wickets
    
    Usage
    
    plotWinsbyTossDecisionAllOpposition(matches,team1,tossDecision='bat',plot="summary")
    Arguments
    
    matches
    The dataframe with all matches between 2 IPL teams
    
    team1
    The team for which the plot has to be done
    
    plot
    'summary' or 'detailed'
    
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
    
    if plot=="summary":
        m= a.loc[a.winner==team1]['winner'].count()
        n= a.loc[a.winner!=team1]['winner'].count()
        df=pd.DataFrame({'outcome':['win','loss'],'number':[m,n]})
        sns.barplot(x='outcome',y='number',data=df)
        plt.xlabel('Outcome')
        plt.ylabel('Number')
        plt.title("Wins vs losses(summary) against all opposition when toss decision was to " + tossDecision + ' for ' +  team1 )
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()        
        plt.gcf().clear()
    elif plot=="detailed" : 
        #Plot breakup by team        
        b=a.groupby('winner').count().reset_index(inplace=False)
        # If 'winner' is '0' then the match is a tie.Set as 'tie'
        b.loc[b.winner=='0','winner']='Tie'
        b.columns = ['winner','number']
        ax=sns.barplot(x='winner',y='number',data=b)
        plt.xlabel(team1 + ' chose to ' + tossDecision)
        plt.ylabel('Number')
        plt.title('Wins vs losses(detailed) against all opposition for ' + team1 + ' when toss decision was to ' + tossDecision )
        ax.set_xticklabels(ax.get_xticklabels(),rotation=60, fontsize=6)
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()        
        plt.show()
        plt.gcf().clear()
        return

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 24 Feb 2019
# Function: Details
# This function computes the batting details of a team
# IPL teams
#
###########################################################################################        
        
def getTeamBattingDetails(team,dir=".",save=False,odir="."):
    '''
    Description
    
    This function gets the batting details of a team in all matchs against all oppositions. This gets all the details of the batsmen balls faced,4s,6s,strikerate, runs, venue etc. This function is then used for analyses of batsmen. This function calls teamBattingPerfDetails()
    
    Usage
    
    getTeamBattingDetails(team,dir=".",save=FALSE)
    Arguments
    
    team	
    The team for which batting details is required
    dir	
    The source directory of RData files obtained with convertAllYaml2RDataframes()
    save	
    Whether the data frame needs to be saved as RData or not. It is recommended to set save=TRUE as the data can be used for a lot of analyses of batsmen
    Value
    
    battingDetails The dataframe with the batting details
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.in/
    
    Examples  
    m=getTeamBattingDetails(team1,dir1,save=True)
    '''
    
    # Get all matches played by team
    t1 = '*' +  team +'*.csv'
    path= os.path.join(dir,t1)
    files = glob.glob(path) 

    
    # Create an empty dataframe
    details = pd.DataFrame()
    
    # Loop through all matches played by team
    for file in files:
          match=pd.read_csv(file)
        
          
          scorecard,extras=teamBattingScorecardMatch(match,team)
          if scorecard.empty:
               continue
          # Filter out only the rows played by team
          match1 = match.loc[match.team==team]
       
          # Check if there were wickets, you will 'bowled', 'caught' etc
          if len(match1 !=0):
            if isinstance(match1.kind.iloc[0],str):
              b=match1.loc[match1.kind != '0']
          
              # Get the details of the wicket
              wkts= b[['batsman','bowler','fielders','kind','player_out']]
              #date','team2','winner','result','venue']]
              df=pd.merge(scorecard,wkts,how='outer',on='batsman')
              
              # Fill NA as not outs
              df =df.fillna('notOut')
              
              # Set other info
              if len(b) != 0:
                  df['date']= b['date'].iloc[0]
                  df['team2']= b['team2'].iloc[0]
                  df['winner']= b['winner'].iloc[0]
                  df['result']= b['result'].iloc[0]
                  df['venue']= b['venue'].iloc[0]         
                  details= pd.concat([details,df])
                  details = details.sort_values(['batsman','date'])      
 
    if save==True:
              fileName = "./" + team + "-BattingDetails.csv"
              output=os.path.join(odir,fileName)
              details.to_csv(output)
             
    return(details)
    

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 24 Feb 2019
# Function: getBatsmanDetails
# This function gets the batsman details
# IPL teams
#
###########################################################################################         
    
def getBatsmanDetails(team, name,dir="."):
    '''
    Get batting details of batsman from match

    Description
    
    This function gets the batting details of a batsman given the match data as a RData file
    
    Usage
    
    getBatsmanDetails(team,name,dir=".")
    Arguments
    
    team	
    The team of the batsman e.g. India
    name	
    Name of batsman
    dir	
    The directory where the source file exists
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
    
    batsmanRunsPredict
    batsmanMovingAverage
    bowlerWicketsVenue
    bowlerMeanRunsConceded
    Examples
    
    ## Not run: 
    name="SK Raina"
    team='Chennai Super Kings'
    #df=getBatsmanDetails(team, name,dir=".")
    '''
    path = dir + '/' + team + "-BattingDetails.csv"
    battingDetails= pd.read_csv(path)
    batsmanDetails = battingDetails.loc[battingDetails['batsman'].str.contains(name)]
    return(batsmanDetails)
    
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 24 Feb 2019
# Function: getBatsmanDetails
# This function plots runs vs deliveries for the batsman
#
###########################################################################################  
def batsmanRunsVsDeliveries(df,name= "A Late Cut",plot=True, savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Runs versus deliveries faced
    
    Description
    
    This function plots the runs scored and the deliveries required. A regression smoothing function is used to fit the points
    
    Usage
    
    batsmanRunsVsDeliveries(df, name= "A Late Cut")
    Arguments
    
    df	
    Data frame
    name	
    Name of batsman
    plot	
    If plot=TRUE then a plot is created otherwise a data frame is returned
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
    
    batsmanFoursSixes
    batsmanRunsVsDeliveries
    batsmanRunsVsStrikeRate
    
    Examples   
    name="SK Raina"
    team='Chennai Super Kings'
    df=getBatsmanDetails(team, name,dir=".")
    batsmanRunsVsDeliveries(df, name)
    '''
    rcParams['figure.figsize'] = 8, 5
    plt.scatter(df.balls,df.runs)
    sns.lmplot(x='balls',y='runs', data=df)
    plt.xlabel("Balls faced",fontsize=8)
    plt.ylabel('Runs',fontsize=8)
    atitle=name + "- Runs vs balls faced"
    plt.title(atitle,fontsize=8)
    if(plot==True):
       if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
       else:
            plt.show()
    plt.gcf().clear()
    return

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 24 Feb 2019
# Function: batsmanFoursSixes
# This function gets the batsman fours and sixes for batsman
# 
#
###########################################################################################  
    
def batsmanFoursSixes(df,name= "A Leg Glance", plot=True, savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Description
    
    This function computes and plots the total runs, fours and sixes of the batsman
    
    Usage
    
    batsmanFoursSixes(df,name= "A Leg Glance")
    Arguments
    
    df	
    Data frame
    name	
    Name of batsman
    If plot=TRUE then a plot is created otherwise a data frame is returned
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
    
    batsmanDismissals batsmanRunsVsDeliveries batsmanRunsVsStrikeRate batsmanRunsVsStrikeRate batsmanRunsPredict
    
    Examples 
    name="SK Raina"
    team='Chennai Super Kings'
    df=getBatsmanDetails(team, name,dir=".")
    batsmanFoursSixes(df,"SK Raina")

    '''
 
    # Compute runs from fours and sixes 
    rcParams['figure.figsize'] = 8, 5
    df['RunsFromFours']=df['4s']*4
    df['RunsFromSixes']=df['6s']*6
    df1 = df[['balls','runs','RunsFromFours','RunsFromSixes']]
    
    # Total runs
    sns.scatterplot('balls','runs',data=df1)
    # Fit a linear regression line
    balls=df1.balls.reshape(-1,1)
    linreg = LinearRegression().fit(balls, df1.runs)
    x=np.linspace(0,120,10)    
    #Plot regression line balls vs runs
    plt.plot(x, linreg.coef_ * x + linreg.intercept_, color='blue',label="Total runs")
    
    # Runs from fours
    sns.scatterplot('balls','RunsFromFours',data=df1)
    #Plot regression line balls vs Runs from fours
    linreg = LinearRegression().fit(balls, df1.RunsFromFours)
    plt.plot(x, linreg.coef_ * x + linreg.intercept_, color='red',label="Runs from fours")
    
    # Runs from sixes
    sns.scatterplot('balls','RunsFromSixes',data=df1)
    #Plot regression line balls vs Runs from sixes
    linreg = LinearRegression().fit(balls, df1.RunsFromSixes)
    plt.plot(x, linreg.coef_ * x + linreg.intercept_, color='green',label="Runs from sixes")
    
    plt.xlabel("Balls faced",fontsize=8)
    plt.ylabel('Runs',fontsize=8)
    atitle=name + "- Total runs, fours and sixes"
    plt.title(atitle,fontsize=8)
    plt.legend(loc="upper left")
    if(plot==True):
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
    plt.gcf().clear()
    return
     
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 24 Feb 2019
# Function: batsmanDismissals
# This function plots the batsman dismissals
#
###########################################################################################       
def batsmanDismissals(df,name="A Leg Glance",plot=True, savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Description
    
    This function computes and plots the type of dismissals of the the batsman
    
    Usage
    
    batsmanDismissals(df,name="A Leg Glance")
    Arguments
    
    df	
    Data frame
    name	
    Name of batsman
    plot	
    If plot=TRUE then a plot is created otherwise a data frame is returned
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
    
    batsmanFoursSixes
    batsmanRunsVsDeliveries
    batsmanRunsVsStrikeRate
    Examples   
    name="SK Raina"
    team='Chennai Super Kings'
    df=getBatsmanDetails(team, name,dir=".")
    batsmanDismissals(df,"SK Raina")
    
    '''
    
    # Count dismissals
    rcParams['figure.figsize'] = 8, 5
    df1 = df[['batsman','kind']]
    df2 = df1.groupby('kind').count().reset_index(inplace=False)
    df2.columns = ['dismissals','count']
    plt.pie(df2['count'], labels=df2['dismissals'],autopct='%.1f%%')
    atitle= name + "-Dismissals"
    plt.title(atitle,fontsize=8)
    if(plot==True):
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
    plt.gcf().clear()
    return
    
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 24 Feb 2019
# Function: batsmanRunsVsStrikeRate
# This function plots the runs vs strike rate
# 
#
###########################################################################################  
def batsmanRunsVsStrikeRate (df,name= "A Late Cut", plot=True, savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Description
    
    This function plots the runs scored by the batsman and the runs scored by the batsman. A loess line is fitted over the points
    
    Usage
    
    batsmanRunsVsStrikeRate(df, name= "A Late Cut")
    Arguments
    
    df	
    Data frame
    name	
    Name of batsman
    plot	
    If plot=TRUE then a plot is created otherwise a data frame is returned
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
    
    batsmanDismissals
    batsmanRunsVsDeliveries
    batsmanRunsVsStrikeRate
    teamBatsmenPartnershipAllOppnAllMatches
    Examples
    name="SK Raina"
    team='Chennai Super Kings'
    df=getBatsmanDetails(team, name,dir=".")
    batsmanRunsVsStrikeRate(df,"SK Raina")
        
    '''
    rcParams['figure.figsize'] = 8, 5
    plt.scatter(df.runs,df.SR)
    sns.lmplot(x='runs',y='SR', data=df,order=2)
    plt.xlabel("Runs",fontsize=8)
    plt.ylabel('Strike Rate',fontsize=8)
    atitle=name + "- Runs vs Strike rate"
    plt.title(atitle,fontsize=8)
    if(plot==True):
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
    plt.gcf().clear()
    return

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 24 Feb 2019
# Function: movingaverage
# This computes the moving average 
# 
#
###########################################################################################  

def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')
    
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 24 Feb 2019
# Function: batsmanMovingAverage
# This function plots the moving average of runs
# 
#
###########################################################################################      
def batsmanMovingAverage(df, name, plot=True, savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Description
    
    This function plots the runs scored by the batsman over the career as a time series. A loess regression line is plotted on the moving average of the batsman the batsman
    
    Usage
    
    batsmanMovingAverage(df, name= "A Leg Glance")
    Arguments
    
    df	
    Data frame
    name	
    Name of batsman
    plot	
    If plot=TRUE then a plot is created otherwise a data frame is returned
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
    
    batsmanDismissals
    batsmanRunsVsDeliveries
    batsmanRunsVsStrikeRate
    teamBatsmenPartnershipAllOppnAllMatches
    Examples 
    name="SK Raina"
    team='Chennai Super Kings'
    df=getBatsmanDetails(team, name,dir=".")
    batsmanMovingAverage(df,"SK Raina")
    
    '''
    rcParams['figure.figsize'] = 8, 5
    y_av = movingaverage(df.runs, 10)
    date= pd.to_datetime(df['date'])
    plt.plot(date, y_av,"b")
    plt.xlabel('Date',fontsize=8)
    plt.ylabel('Runs',fontsize=8)
    plt.xticks(rotation=90)
    atitle = name +  "-Moving average of runs"
    plt.title(atitle,fontsize=8)
    if(plot==True):
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
    plt.gcf().clear()
    return
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 24 Feb 2019
# Function: batsmanCumulativeAverageRuns
# This functionplots the cumulative average runs
# 
#
###########################################################################################  
def batsmanCumulativeAverageRuns(df,name="A Leg Glance",plot=True, savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Batsman's cumulative average runs
    
    Description
    
    This function computes and plots the cumulative average runs of a batsman
    
    Usage
    
    batsmanCumulativeAverageRuns(df,name= "A Leg Glance")
    Arguments
    
    df	
    Data frame
    name	
    Name of batsman
    plot	
    If plot=TRUE then a plot is created otherwise a data frame is returned
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
    
    batsmanCumulativeStrikeRate bowlerCumulativeAvgEconRate bowlerCumulativeAvgWickets batsmanRunsVsStrikeRate batsmanRunsPredict
    
    Examples 
    name="SK Raina"
    team='Chennai Super Kings'
    df=getBatsmanDetails(team, name,dir=".")
    batsmanCumulativeAverageRuns(df,"SK Raina")
    
    '''
    rcParams['figure.figsize'] = 8, 5
    cumAvgRuns = df['runs'].cumsum()/pd.Series(np.arange(1, len( df['runs'])+1),  df['runs'].index)
    plt.plot(cumAvgRuns)
    plt.xlabel('No of matches',fontsize=8)
    plt.ylabel('Cumulative Average Runs',fontsize=8)
    plt.xticks(rotation=90)
    atitle = name +  "-Cumulative Average Runs vs matches"
    plt.title(atitle,fontsize=8)
    if(plot==True):
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
    plt.gcf().clear()
    return

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 24 Feb 2019
# Function: batsmanCumulativeStrikeRate
# This function plots the cumulative average Strike rate
# 
#
###########################################################################################  
def batsmanCumulativeStrikeRate(df,name="A Leg Glance",plot=True, savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Description
    
    This function computes and plots the cumulative average strike rate of a batsman
    
    Usage
    
    batsmanCumulativeStrikeRate(df,name= "A Leg Glance")
    Arguments
    
    df	
    Data frame
    name	
    Name of batsman
    plot	
    If plot=TRUE then a plot is created otherwise a data frame is returned
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
    
    batsmanCumulativeAverageRuns bowlerCumulativeAvgEconRate bowlerCumulativeAvgWickets batsmanRunsVsStrikeRate batsmanRunsPredict
    
    Examples
    name="SK Raina"
    team='Chennai Super Kings'
    df=getBatsmanDetails(team, name,dir=".")
    #batsmanCumulativeAverageRunsdf(df,name)
   
    
    '''
    rcParams['figure.figsize'] = 8, 5
    cumAvgRuns = df['SR'].cumsum()/pd.Series(np.arange(1, len( df['SR'])+1),  df['SR'].index)
    plt.plot(cumAvgRuns)
    plt.xlabel('No of matches',fontsize=8)
    plt.ylabel('Cumulative Average Strike Rate',fontsize=8)
    plt.xticks(rotation=70)
    atitle = name +  "-Cumulative Average Strike Rate vs matches"
    plt.title(atitle,fontsize=8) 
    if(plot==True):
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
    plt.gcf().clear()
    return

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 24 Feb 2019
# Function: batsmanRunsAgainstOpposition
# This function plots the batsman's runs against opposition
# 
#
###########################################################################################  
def batsmanRunsAgainstOpposition(df,name= "A Leg Glance",plot=True, savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Description

    This function computes and plots the mean runs scored by the batsman against different oppositions
    
    Usage
    
    batsmanRunsAgainstOpposition(df, name= "A Leg Glance")
    Arguments
    
    df	
    Data frame
    name	
    Name of batsman
    plot	
    If plot=TRUE then a plot is created otherwise a data frame is returned
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
    
    batsmanFoursSixes
    batsmanRunsVsDeliveries
    batsmanRunsVsStrikeRate
    teamBatsmenPartnershipAllOppnAllMatches
    Examples
    name="SK Raina"
    team='Chennai Super Kings'
    df=getBatsmanDetails(team, name,dir=".")
    batsmanRunsAgainstOpposition(df,name)

    '''
    rcParams['figure.figsize'] = 8, 5
    df1 = df[['batsman', 'runs','team2']]
    df2=df1.groupby('team2').agg(['sum','mean','count'])
    df2.columns= ['_'.join(col).strip() for col in df2.columns.values]
    # Reset index
    df3=df2.reset_index(inplace=False)
    ax=sns.barplot(x='team2', y="runs_mean", data=df3)
    plt.xticks(rotation="vertical",fontsize=8)
    plt.xlabel('Opposition',fontsize=8)
    plt.ylabel('Mean Runs',fontsize=8)
    atitle=name + "-Mean Runs against opposition"
    plt.title(atitle,fontsize=8)
    if(plot==True):
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
    plt.gcf().clear()
    return

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 24 Feb 2019
# Function: batsmanRunsVenue
# This function plos the batsman's runs at venues
# 
#
###########################################################################################  
def batsmanRunsVenue(df,name= "A Leg Glance",plot=True, savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Description
    
    This function computes and plots the mean runs scored by the batsman at different venues of the world
    
    Usage
    
    batsmanRunsVenue(df, name= "A Leg Glance")
    Arguments
    
    df	
    Data frame
    name	
    Name of batsman
    plot	
    If plot=TRUE then a plot is created otherwise a data frame is returned
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
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
    
    batsmanFoursSixes
    batsmanRunsVsDeliveries
    batsmanRunsVsStrikeRate
    teamBatsmenPartnershipAllOppnAllMatches
    batsmanRunsAgainstOpposition
    
    Examples    
    name="SK Raina"
    team='Chennai Super Kings'
    df=getBatsmanDetails(team, name,dir=".")
    #batsmanRunsVenue(df,name)
    '''
    rcParams['figure.figsize'] = 8, 5
    df1 = df[['batsman', 'runs','venue']]
    df2=df1.groupby('venue').agg(['sum','mean','count'])
    df2.columns= ['_'.join(col).strip() for col in df2.columns.values]
    # Reset index
    df3=df2.reset_index(inplace=False)
    ax=sns.barplot(x='venue', y="runs_mean", data=df3)
    plt.xticks(rotation="vertical",fontsize=8)
    plt.xlabel('Venue',fontsize=8)
    plt.ylabel('Mean Runs',fontsize=8)
    atitle=name + "-Mean Runs at venues"
    plt.title(atitle,fontsize=8)
    if(plot==True):
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
    plt.gcf().clear()
    return
    
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 24 Feb 2019
# Function: teamBowlingPerDetails
# This function gets the bowling performances
# 
#
###########################################################################################  
def teamBowlingPerDetails(team):

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
# Date : 24 Feb 2019
# Function: getTeamBowlingDetails
# This function gets the team bowling details
# 
#
###########################################################################################  
def getTeamBowlingDetails (team,dir=".",save=False,odir="."):
    '''
    Description
    
    This function gets the bowling details of a team in all matchs against all oppositions. This gets all the details of the bowlers for e.g deliveries, maidens, runs, wickets, venue, date, winner ec
    
    Usage
    
    getTeamBowlingDetails(team,dir=".",save=FALSE)
    Arguments
    
    team	
    The team for which detailed bowling info is required
    dir	
    The source directory of RData files obtained with convertAllYaml2RDataframes()
    save	
    Whether the data frame needs to be saved as RData or not. It is recommended to set save=TRUE as the data can be used for a lot of analyses of batsmen
    Value
    
    bowlingDetails The dataframe with the bowling details
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.wordpress.com/
    https://github.com/tvganesh/yorkrData
    
    See Also
    
    getBatsmanDetails
    getBowlerWicketDetails
    batsmanDismissals
    getTeamBattingDetails
    Examples    
    dir1= "C:\\software\\cricket-package\\yorkpyIPLData\\data"
    eam1='Delhi Daredevils'
    m=getTeamBowlingDetails(team1,dir1,save=True)
    '''
    
    # Get all matches played by team
    t1 = '*' +  team +'*.csv'
    path= os.path.join(dir,t1)
    files = glob.glob(path) 

    
    # Create an empty dataframe
    details = pd.DataFrame()
    
    # Loop through all matches played by team
    for file in files:
          match=pd.read_csv(file)
          if(match.size != 0):
              team1=match.loc[match.team != team]
          else:
              continue

          if len(team1) !=0:
              scorecard=teamBowlingPerDetails(team1)
              scorecard['date']= match['date'].iloc[0]
              scorecard['team2']= match['team2'].iloc[0]
              scorecard['winner']= match['winner'].iloc[0]
              scorecard['result']= match['result'].iloc[0]
              scorecard['venue']= match['venue'].iloc[0]       
              details= pd.concat([details,scorecard])
              details = details.sort_values(['bowler','date'])
          else:
              pass # The team did not bowl
    if save==True:
         fileName = "./" + team + "-BowlingDetails.csv"
         output=os.path.join(odir,fileName)
         details.to_csv(output,index=False)
              
    return(details)
    
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 24 Feb 2019
# Function: getBowlerWicketDetails
# This function gets the bowler wicket
# 
#
###########################################################################################  
    
def getBowlerWicketDetails (team, name,dir="."):
    '''
    Description
    
    This function gets the bowling of a bowler (overs,maidens,runs,wickets,venue, opposition)
    
    Usage
    
    getBowlerWicketDetails(team,name,dir=".")
    Arguments
    
    team	
    The team to which the bowler belongs
    name	
    The name of the bowler
    dir	
    The source directory of the data
    Value
    
    dataframe The dataframe of bowling performance
    
    Note
    
    Maintainer: Tinniam V Ganesh tvganesh.85@gmail.com
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://cricsheet.org/
    https://gigadom.wordpress.com/
    https://github.com/tvganesh/yorkrData
    
    See Also
    
    bowlerMovingAverage
    getTeamBowlingDetails
    bowlerMeanRunsConceded
    teamBowlersWicketRunsOppnAllMatches
    
    Examples    
    name="R Ashwin"
    team='Chennai Super Kings'
    df=getBowlerWicketDetails(team, name,dir=".")
    '''
    path = dir + '/' + team + "-BowlingDetails.csv"
    bowlingDetails= pd.read_csv(path,index_col=False)
    bowlerDetails = bowlingDetails.loc[bowlingDetails['bowler'].str.contains(name)]
    return(bowlerDetails)
    
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 24 Feb 2019
# Function: bowlerMeanEconomyRate
# This function gets the bowler mean economy rate
# 
#
###########################################################################################  
def bowlerMeanEconomyRate(df,name="A Leg Glance",plot=True, savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Description
    
    This function computes and plots mean economy rate and the number of overs bowled by the bowler
    
    Usage
    
    bowlerMeanEconomyRate(df, name)
    Arguments
    
    df	
    Data frame
    name	
    Name of bowler
    plot	
    If plot=TRUE then a plot is created otherwise a data frame is returned
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
    
    bowlerMovingAverage
    bowlerWicketPlot
    bowlerWicketsVenue
    bowlerMeanRunsConceded
    
    Examples    
    name="R Ashwin"
    team='Chennai Super Kings'
    df=getBowlerWicketDetails(team, name,dir=".")
    bowlerMeanEconomyRate(df, name)
    
    '''
    
    # Count dismissals
    rcParams['figure.figsize'] = 8, 5
    df2=df[['bowler','overs','econrate']].groupby('overs').mean().reset_index(inplace=False)
    plt.xlabel('No of overs',fontsize=8)
    plt.ylabel('Mean economy rate',fontsize=8)
    sns.barplot(x='overs',y='econrate',data=df2)
    atitle = name +  "-Mean economy rate vs overs"
    plt.title(atitle,fontsize=8)
    if(plot==True):
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
    plt.gcf().clear()
    return

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 24 Feb 2019
# Function: bowlerMeanRunsConceded
# This function gets the mean runs conceded by bowler
# 
#
###########################################################################################  
def bowlerMeanRunsConceded (df,name="A Leg Glance",plot=True, savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Description
    
    This function computes and plots mean runs conceded by the bowler for the number of overs bowled by the bowler
    
    Usage
    
    bowlerMeanRunsConceded(df, name)
    Arguments
    
    df	
    Data frame
    name	
    Name of bowler
    plot	
    If plot=TRUE then a plot is created otherwise a data frame is returned
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
    
    bowlerMovingAverage
    bowlerWicketPlot
    bowlerWicketsVenue
    bowlerMeanRunsConceded
    
    Examples    
    name="R Ashwin"
    team='Chennai Super Kings'
    df=getBowlerWicketDetails(team, name,dir=".")
    bowlerMeanRunsConceded(df, name)
    '''
    
    # Count dismissals
    rcParams['figure.figsize'] = 8, 5
    df2=df[['bowler','overs','runs']].groupby('overs').mean().reset_index(inplace=False)
    plt.xlabel('No of overs',fontsize=8)
    plt.ylabel('Mean runs conceded',fontsize=8)
    sns.barplot(x='overs',y='runs',data=df2)
    atitle = name +  "-Mean runs conceded vs overs"
    plt.title(atitle,fontsize=8)
    if(plot==True):
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
    plt.gcf().clear()
    return

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 24 Feb 2019
# Function: bowlerMovingAverage
# This function gets the bowler moving average
# 
#
###########################################################################################  
def bowlerMovingAverage (df, name,plot=True, savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Description
    
    This function computes and plots the wickets taken by the bowler over career. A loess regression fit plots the moving average of wickets taken by bowler
    
    Usage
    
    bowlerMovingAverage(df, name)
    Arguments
    
    df	
    Data frame
    name	
    Name of bowler
    plot	
    If plot=TRUE then a plot is created otherwise a data frame is returned
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
    
    bowlerMeanEconomyRate
    bowlerWicketPlot
    bowlerWicketsVenue
    bowlerMeanRunsConceded
    
    Examples  
    name="R Ashwin"
    team='Chennai Super Kings'
    df=getBowlerWicketDetails(team, name,dir=".")
    bowlerMeanEconomyRate(df, name)
    '''
    rcParams['figure.figsize'] = 8, 5
    y_av = movingaverage(df.wicket, 30)
    date= pd.to_datetime(df['date'])
    plt.plot(date, y_av,"b")
    plt.xlabel('Date',fontsize=8)
    plt.ylabel('Wickets',fontsize=8)
    plt.xticks(rotation=70)
    atitle = name +  "-Moving average of wickets"
    plt.title(atitle,fontsize=8)
    if(plot==True):
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
    plt.gcf().clear()
    return

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 24 Feb 2019
# Function: bowlerCumulativeAvgWickets
# This function gets the bowler cumulative average runs
# 
#
###########################################################################################  
def bowlerCumulativeAvgWickets(df,name="A Leg Glance",plot=True, savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Description
    
    This function computes and plots the cumulative average wickets of a bowler
    
    Usage
    
    bowlerCumulativeAvgWickets(df,name)
    Arguments
    
    df	
    Data frame
    name	
    Name of batsman
    plot	
    If plot=TRUE then a plot is created otherwise a data frame is returned
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
    
    batsmanCumulativeAverageRuns bowlerCumulativeAvgEconRate batsmanCumulativeStrikeRate batsmanRunsVsStrikeRate batsmanRunsPredict
    
    Examples  
    
    name="R Ashwin"
    team='Chennai Super Kings'
    df=getBowlerWicketDetails(team, name,dir=".")
    bowlerCumulativeAvgWickets(df, name)
    
    '''
    rcParams['figure.figsize'] = 8, 5
    cumAvgRuns = df['wicket'].cumsum()/pd.Series(np.arange(1, len( df['wicket'])+1),  df['wicket'].index)
    plt.plot(cumAvgRuns)
    plt.xlabel('No of matches',fontsize=8)
    plt.ylabel('Cumulative Average wickets',fontsize=8)
    plt.xticks(rotation=90)
    atitle = name +  "-Cumulative Average wickets vs matches"
    plt.title(atitle,fontsize=8)
    if(plot==True):
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
    plt.gcf().clear()
    return

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 24 Feb 2019
# Function: bowlerCumulativeAvgEconRate
# This function gets the  bowler cumulative average economy rate
# 
#
###########################################################################################  
def bowlerCumulativeAvgEconRate(df,name="A Leg Glance",plot=True, savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Description
    
    This function computes and plots the cumulative average economy rate of a bowler
    
    Usage
    
    bowlerCumulativeAvgEconRate(df,name)
    Arguments
    
    df	
    Data frame
    name	
    Name of batsman
    If plot=TRUE then a plot is created otherwise a data frame is returned
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
    
    batsmanCumulativeAverageRuns bowlerCumulativeAvgWickets batsmanCumulativeStrikeRate batsmanRunsVsStrikeRate batsmanRunsPredict
    
    Examples   
    name="R Ashwin"
    team='Chennai Super Kings'
    df=getBowlerWicketDetails(team, name,dir=".")
    bowlerMeanEconomyRate(df, name)
    '''
    rcParams['figure.figsize'] = 8, 5
    cumAvgRuns = df['econrate'].cumsum()/pd.Series(np.arange(1, len( df['econrate'])+1),  df['econrate'].index)
    plt.plot(cumAvgRuns)
    plt.xlabel('No of matches',fontsize=7)
    plt.ylabel('Cumulative Average economy rate',fontsize=8)
    plt.xticks(rotation=70)
    atitle = name +  "-Cumulative Average economy rate vs matches"
    plt.title(atitle,fontsize=8)
    if(plot==True):
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
    plt.gcf().clear()
    return

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 24 Feb 2019
# Function: bowlerWicketPlot
# This function gets the bowler wicket plot
# 
#
###########################################################################################  
def bowlerWicketPlot (df,name="A Leg Glance",plot=True, savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Description
    
    This function computes and plots the average wickets taken by the bowler versus the number of overs bowled
    
    Usage
    
    bowlerWicketPlot(df, name)
    Arguments
    
    df	
    Data frame
    name	
    Name of bowler
    plot	
    If plot=TRUE then a plot is created otherwise a data frame is returned
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile

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
    
    bowlerMeanEconomyRate
    bowlerWicketsVenue
    bowlerMeanRunsConceded
    
    Examples  
    name="R Ashwin"
    team='Chennai Super Kings'
    df=getBowlerWicketDetails(team, name,dir=".")
    bowlerMeanEconomyRate(df, name)
    
    '''
    rcParams['figure.figsize'] = 8, 5
    # Count dismissals
    df2=df[['bowler','overs','wicket']].groupby('overs').mean().reset_index(inplace=False)
    plt.xlabel('No of overs',fontsize=8)
    plt.ylabel('Mean wickets',fontsize=8)
    sns.barplot(x='overs',y='wicket',data=df2)
    atitle = name +  "-Mean wickets vs overs"
    plt.title(atitle,fontsize=8)
    if(plot==True):
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
    plt.gcf().clear()
    return

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 24 Feb 2019
# Function: bowlerWicketsAgainstOpposition
# This function gets the bowler's performance against opposition
# 
#
###########################################################################################  
def bowlerWicketsAgainstOpposition (df,name= "A Leg Glance", plot=True, savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Description
    
    This function computes and plots mean number of wickets taken by the bowler against different opposition
    
    Usage
    
    bowlerWicketsAgainstOpposition(df, name)
    Arguments
    
    df	
    Data frame
    name	
    Name of bowler
    plot	
    If plot=TRUE then a plot is created otherwise a data frame is returned
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
    
    bowlerMovingAverage
    bowlerWicketPlot
    bowlerWicketsVenue
    bowlerMeanRunsConceded
    
    Examples 
    name="R Ashwin"
    team='Chennai Super Kings'
    df=getBowlerWicketDetails(team, name,dir=".")
    bowlerWicketsAgainstOpposition(df, name)
    '''
    rcParams['figure.figsize'] = 8, 5
    df1 = df[['bowler', 'wicket','team2']]
    df2=df1.groupby('team2').agg(['sum','mean','count'])
    df2.columns= ['_'.join(col).strip() for col in df2.columns.values]
    # Reset index
    df3=df2.reset_index(inplace=False)
    ax=sns.barplot(x='team2', y="wicket_mean", data=df3)
    plt.xticks(rotation=90,fontsize=7)
    plt.xlabel('Opposition',fontsize=7)
    plt.ylabel('Mean wickets',fontsize=8)
    atitle=name + "-Mean wickets against opposition"
    plt.title(atitle,fontsize=8)
    if(plot==True):
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
    plt.gcf().clear()
    return

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 24 Feb 2019
# Function: bowlerWicketsVenue
# This function gets the bowler wickets at venues
# 
#
########################################################################################### 
def bowlerWicketsVenue (df,name= "A Leg Glance",plot=True, savePic=False, dir1=".",picFile="pic1.png"):
    '''
    Bowler performance at different venues
    
    Description
    
    This function computes and plots mean number of wickets taken by the bowler in different venues
    
    Usage
    
    bowlerWicketsVenue(df, name)
    Arguments
    
    df	
    Data frame
    name	
    Name of bowler
    plot	
    If plot=TRUE then a plot is created otherwise a data frame is returned
    savePic
    If savePic = True then the plot is saved
    dir1
    The directory where the plot is saved
    picFile
    The name of the savefile
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
    
    bowlerMovingAverage
    bowlerWicketPlot
    bowlerWicketsVenue
    bowlerMeanRunsConceded
    
    Examples  
    name="R Ashwin"
    team='Chennai Super Kings'
    df=getBowlerWicketDetails(team, name,dir=".")
    bowlerWicketsVenue(df, name)
    '''
    rcParams['figure.figsize'] = 8, 5
    df1 = df[['bowler', 'wicket','venue']]
    df2=df1.groupby('venue').agg(['sum','mean','count'])
    df2.columns= ['_'.join(col).strip() for col in df2.columns.values]
    # Reset index
    df3=df2.reset_index(inplace=False)
    ax=sns.barplot(x='venue', y="wicket_mean", data=df3)
    plt.xticks(rotation=90,fontsize=7)
    plt.xlabel('Venue',fontsize=7)
    plt.ylabel('Mean wickets',fontsize=8)
    atitle=name + "-Mean wickets at different venues"
    plt.title(atitle,fontsize=8)  
    if(plot==True):
        if(savePic):
            plt.savefig(os.path.join(dir1,picFile),bbox_inches='tight')
        else:
            plt.show()
    plt.gcf().clear()
    return


##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 1 March 2019
# Function: saveAllMatchesBetween2IntlT20s
# This function saves all the matches between 2 Intl T20 teams
#
###########################################################################################

def saveAllMatchesBetween2IntlT20s(dir1,odir="."):  
    '''
    Saves all matches between 2 IPL teams as dataframe
    Description
   
    This function saves all matches between 2 Intl. T20 countries as a single dataframe in the 
    current directory
    
    Usage
    
    saveAllMatchesBetween2IntlT20s(dir)
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
    teams = ["Afghanistan","Australia","Bangladesh","Bermuda","Canada","England",
             "Hong Kong","India","Ireland", "Kenya","Nepal","Netherlands",
             "New Zealand", "Oman","Pakistan","Scotland","South Africa",
             "Sri Lanka", "United Arab Emirates","West Indies", "Zimbabwe"]
    
    for team1 in teams:
        for team2 in teams:
            if team1 != team2:
                print("Team1=",team1,"team2=", team2)
                getAllMatchesBetweenTeams(team1,team2,dir=dir1,save=True,odir=odir)
                time.sleep(2) #Sleep before  next save   
                
    return    




###########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 2 Mar 2019
# Function: saveAllMatchesAllOppositionIntlT20
# This function saves all the matches between all Intl T20 teams
#
########################################################################################### 
def saveAllMatchesAllOppositionIntlT20(dir1,odir="."):  
    '''
    Saves matches against all Intl T20 teams as dataframe and CSV for an IPL team
    
    Description
    
    This function saves all Intl T20 matches agaist all opposition as a single 
    dataframe in the current directory
    
    Usage
    
    saveAllMatchesAllOppositionIntlT20(dir)
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
    https://gigadom.wordpress.com/

    
    See Also
    
    convertYaml2PandasDataframeT20
    teamBattingScorecardMatch 
    '''
    teams = ["Afghanistan","Australia","Bangladesh","Bermuda","Canada","England",
             "Hong Kong","India","Ireland", "Kenya","Nepal","Netherlands",
             "New Zealand", "Oman","Pakistan","Scotland","South Africa",
             "Sri Lanka", "United Arab Emirates","West Indies", "Zimbabwe"]
    
    for team in teams:
                print("Team=",team)
                getAllMatchesAllOpposition(team,dir=dir1,save=True,odir=odir)
                time.sleep(2) #Sleep before  next save
                   

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 2 March 2019
# Function: saveAllMatchesBetween2BBLTeams
# This function saves all the matches between 2 BBL Teams
#
###########################################################################################

def saveAllMatchesBetween2BBLTeams(dir1):  
    '''
    Saves all matches between 2 BBLteams as dataframe
    Description
   
    This function saves all matches between 2 BBL T20 countries as a single dataframe in the 
    current directory
    
    Usage
    
    saveAllMatchesBetween2BBLTeams(dir)
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
    teams = ["Adelaide Strikers", "Brisbane Heat", "Hobart Hurricanes",
             "Melbourne Renegades", "Perth Scorchers", "Sydney Sixers",
             "Sydney Thunder"]
    
    for team1 in teams:
        for team2 in teams:
            if team1 != team2:
                print("Team1=",team1,"team2=", team2)
                getAllMatchesBetweenTeams(team1,team2,dir=dir1,save=True)
                time.sleep(2) #Sleep before  next save   
                
    return    

###########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 2 Mar 2019
# Function: saveAllMatchesAllOppositionBBLT20
# This function saves all the matches between all BBL T20 teams
#
########################################################################################### 
def saveAllMatchesAllOppositionBBLT20(dir1):  
    '''
    Saves matches against all BBL T20 teams as dataframe and CSV for an IPL team
    
    Description
    
    This function saves all BBL T20 matches agaist all opposition as a single 
    dataframe in the current directory
    
    Usage
    
    saveAllMatchesAllOppositionBBLT20(dir)
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
    https://gigadom.wordpress.com/

    
    See Also
    
    convertYaml2PandasDataframeT20
    teamBattingScorecardMatch 
    '''
    teams = ["Adelaide Strikers", "Brisbane Heat", "Hobart Hurricanes",
             "Melbourne Renegades", "Perth Scorchers", "Sydney Sixers",
             "Sydney Thunder"]
    
    for team in teams:
                print("Team=",team)
                getAllMatchesAllOpposition(team,dir=dir1,save=True)
                time.sleep(2) #Sleep before  next save
                
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 2 March 2019
# Function: saveAllMatchesBetween2NWBTeams
# This function saves all the matches between 2 NWB Teams
#
###########################################################################################

def saveAllMatchesBetween2NWBTeams(dir1):  
    '''
    Saves all matches between 2 NWB teams as dataframe
    Description
   
    This function saves all matches between 2 NWB T20 countries as a single dataframe in the 
    current directory
    
    Usage
    
    saveAllMatchesBetween2NWBTeams(dir)
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
    teams = ["Derbyshire", "Durham", "Essex", "Glamorgan",
             "Gloucestershire", "Hampshire", "Kent","Lancashire",
             "Leicestershire", "Middlesex","Northamptonshire",
             "Nottinghamshire","Somerset","Surrey","Sussex","Warwickshire",
             "Worcestershire","Yorkshire"]
    
    for team1 in teams:
        for team2 in teams:
            if team1 != team2:
                print("Team1=",team1,"team2=", team2)
                getAllMatchesBetweenTeams(team1,team2,dir=dir1,save=True)
                time.sleep(2) #Sleep before  next save   
                
    return   

###########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 2 Mar 2019
# Function: saveAllMatchesAllOppositionNWBT20
# This function saves all the matches between all NWB T20 teams
#
########################################################################################### 
def saveAllMatchesAllOppositionNWBT20(dir1):  
    '''
    Saves matches against all NWB T20 teams as dataframe and CSV for an IPL team
    
    Description
    
    This function saves all NWBT20 matches agaist all opposition as a single 
    dataframe in the current directory
    
    Usage
    
    saveAllMatchesAllOppositionNWBT20(dir)
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
    https://gigadom.wordpress.com/

    
    See Also
    
    convertYaml2PandasDataframeT20
    teamBattingScorecardMatch 
    '''
    teams = ["Derbyshire", "Durham", "Essex", "Glamorgan",
             "Gloucestershire", "Hampshire", "Kent","Lancashire",
             "Leicestershire", "Middlesex","Northamptonshire",
             "Nottinghamshire","Somerset","Surrey","Sussex","Warwickshire",
             "Worcestershire","Yorkshire"]
    
    for team in teams:
                print("Team=",team)
                getAllMatchesAllOpposition(team,dir=dir1,save=True)
                time.sleep(2) #Sleep before  next save
                
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 28 Feb 2020
# Function: rankIntlT20Batting
# This function ranks Intl T20 batsman
#
###########################################################################################                

def rankIntlT20Batting(dir1):      
    countries ={"India":"india", "United States of America":"usa", "Canada":"canada", "United Arab Emirates":"uae",
                "Afghanistan":"afghanistan", "West Indies":"westindies","Oman":"oman","Germany":"germany",
                "Namibia":"namibia","Germany":"germany","Sri Lanka":"sl","Singapore":"singapore",
                "Malaysia":"malaysia","South Africa": "sa","Netherlands":"netherlands",
                "Zimbabwe":"zimbabwe","Pakistan":"pakistan","Scotland":"scotland","Kuwait":"kuwait",
                "New Zealand":"nz","Vanuatu":"vanuatu","Papua New Guinea": "png","Australia":"aus",
                "Irelaand":"ireland","England":"england","South Korea":"sk","Japan":"japan","Bangladesh":"bangladesh",
                "Nepal":"nepal","Cayman Island":"cayman","Rwanda":"rwanda","Qatar":"qatar","Botswana":"botswana",
                "Rwanda":"rwanda","Uganda":"uganda","Maldives":"maldives","Fiji":"fiji","Mozambique":"mozam",
                "Hong Kong":"hk","Denmark":"denmark","Norway":"norway"
                }
    
    df=pd.DataFrame()
    for key in countries:
        val = countries[key] + "_details"
        val= getTeamBattingDetails(key,dir=dir1, save=False,odir=".")
        df = pd.concat([df,val])
    df1=df.groupby('batsman').agg(['count','mean'])
    df1.columns = ['_'.join(col).strip() for col in df1.columns.values]
    df2 =df1[['runs_count','runs_mean','SR_mean']]
    df3=df2[df2['runs_count']>40]
    df4=df3.sort_values(['runs_mean','SR_mean'],ascending=False)
    df4.columns=['matches','runs_mean','SR_mean']
    return(df4)
    
#########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 28 Feb 2020
# Function: rankIntlT20Bowling
# This function ranks Intl T20 bowlers
#
###########################################################################################   
def rankIntlT20Bowling(dir1):
    countries ={"India":"india", "United States of America":"usa", "Canada":"canada", "United Arab Emirates":"uae",
                    "Afghanistan":"afghanistan", "West Indies":"westindies","Oman":"oman","Germany":"germany",
                    "Namibia":"namibia","Germany":"germany","Sri Lanka":"sl","Singapore":"singapore",
                    "Malaysia":"malaysia","South Africa": "sa","Netherlands":"netherlands",
                    "Zimbabwe":"zimbabwe","Pakistan":"pakistan","Scotland":"scotland","Kuwait":"kuwait",
                    "New Zealand":"nz","Vanuatu":"vanuatu","Papua New Guinea": "png","Australia":"aus",
                    "Irelaand":"ireland","England":"england","South Korea":"sk","Japan":"japan","Bangladesh":"bangladesh",
                    "Nepal":"nepal","Cayman Island":"cayman","Rwanda":"rwanda","Qatar":"qatar","Botswana":"botswana",
                    "Rwanda":"rwanda","Uganda":"uganda","Maldives":"maldives","Fiji":"fiji","Mozambique":"mozam",
                    "Hong Kong":"hk","Denmark":"denmark","Norway":"norway"
                    }
    df=pd.DataFrame()
    for key in countries:
        val = countries[key] + "_details"
        val= getTeamBowlingDetails(key,dir=dir1, save=False,odir=".")
        df = pd.concat([df,val])
    df1=df.groupby('bowler').agg(['count','mean'])
    df1.columns = ['_'.join(col).strip() for col in df1.columns.values]
    df2 =df1[['wicket_count','wicket_mean','econrate_mean']]
    df3=df2[df2['wicket_count']>40]
    df4=df3.sort_values(['wicket_mean','econrate_mean'],ascending=False)
    df4.columns=['matches','wicket_mean','econrate_mean']
    return(df4)
    
#########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 28 Feb 2020
# Function: rankIPLT20Batting
# This function ranks IPL T20 batsmen
#
###########################################################################################

def rankIPLT20Batting(dir1):      

    iplTeams ={"Chennai Super Kings":"csk","Deccan Chargers":"dc","Delhi Daredevils":"dd",
                  "Kings XI Punjab":"kxip", 'Kochi Tuskers Kerala':"kct","Kolkata Knight Riders":"kkr",
                  "Mumbai Indians":"mi", "Pune Warriors":"pw","Rajasthan Royals":"rr",
                  "Royal Challengers Bangalore":"rps","Sunrisers Hyderabad":"sh","Gujarat Lions":"gl",
                  "Rising Pune Supergiants":"rps"}
    
    df=pd.DataFrame()
    for key in iplTeams:
        val = iplTeams[key] + "_details"
        val= getTeamBattingDetails(key,dir=dir1, save=False,odir=".")
        df = pd.concat([df,val])
    df1=df.groupby('batsman').agg(['count','mean'])
    df1.columns = ['_'.join(col).strip() for col in df1.columns.values]
    df2 =df1[['runs_count','runs_mean','SR_mean']]
    df3=df2[df2['runs_count']>40]
    df4=df3.sort_values(['runs_mean','SR_mean'],ascending=False)
    df4.columns=['matches','runs_mean','SR_mean']
    return(df4)    

#########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 28 Feb 2020
# Function: rankIPLT20Bowling
# This function ranks IPL T20 bowlers
#
###########################################################################################
    
def rankIPLT20Bowling(dir1):
    iplTeams ={"Chennai Super Kings":"csk","Deccan Chargers":"dc","Delhi Daredevils":"dd",
                  "Kings XI Punjab":"kxip", 'Kochi Tuskers Kerala':"kct","Kolkata Knight Riders":"kkr",
                  "Mumbai Indians":"mi", "Pune Warriors":"pw","Rajasthan Royals":"rr",
                  "Royal Challengers Bangalore":"rps","Sunrisers Hyderabad":"sh","Gujarat Lions":"gl",
                  "Rising Pune Supergiants":"rps"}
                    
    df=pd.DataFrame()
    for key in iplTeams:
        val = iplTeams[key] + "_details"
        val= getTeamBowlingDetails(key,dir=dir1, save=False,odir=".")
        df = pd.concat([df,val])
    df1=df.groupby('bowler').agg(['count','mean'])
    df1.columns = ['_'.join(col).strip() for col in df1.columns.values]
    df2 =df1[['wicket_count','wicket_mean','econrate_mean']]
    df3=df2[df2['wicket_count']>40]
    df4=df3.sort_values(['wicket_mean','econrate_mean'],ascending=False)
    df4.columns=['matches','wicket_mean','econrate_mean']
    return(df4)
    
#########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 28 Feb 2020
# Function: rankNTBT20Batting
# This function ranks NTB T20 batsmen
#
###########################################################################################
    
def rankNTBT20Batting(dir1):      

    ntbTeams = {"Derbyshire":"der", "Durham":"dur", "Essex":"ess", "Glamorgan":"gla",
             "Gloucestershire":"glo", "Hampshire":"ham", "Kent":"ken","Lancashire":"lan",
             "Leicestershire":"lei", "Middlesex":"mid","Northamptonshire":"nor",
             "Nottinghamshire":"not","Somerset":"som","Surrey":"sur","Sussex":"sus","Warwickshire":"war",
             "Worcestershire":"wor","Yorkshire":"yor"}
    
    df=pd.DataFrame()
    for key in ntbTeams:
        val = ntbTeams[key] + "_details"
        val= getTeamBattingDetails(key,dir=dir1, save=False,odir=".")
        df = pd.concat([df,val])
        
    df1=df.groupby('batsman').agg(['count','mean'])
    df1.columns = ['_'.join(col).strip() for col in df1.columns.values]
    df2 =df1[['runs_count','runs_mean','SR_mean']]
    df3=df2[df2['runs_count']>10]
    df4=df3.sort_values(['runs_mean','SR_mean'],ascending=False)
    df4.columns=['matches','runs_mean','SR_mean']
    return(df4)  
    
#########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 28 Feb 2020
# Function: rankNTBT20Bowling
# This function ranks NTB T20 bowlers
#
###########################################################################################
    
def rankNTBT20Bowling(dir1):
    ntbTeams = {"Derbyshire":"der", "Durham":"dur", "Essex":"ess", "Glamorgan":"gla",
             "Gloucestershire":"glo", "Hampshire":"ham", "Kent":"ken","Lancashire":"lan",
             "Leicestershire":"lei", "Middlesex":"mid","Northamptonshire":"nor",
             "Nottinghamshire":"not","Somerset":"som","Surrey":"sur","Sussex":"sus","Warwickshire":"war",
             "Worcestershire":"wor","Yorkshire":"yor"}
                    
    df=pd.DataFrame()
    for key in ntbTeams:
        val = ntbTeams[key] + "_details"
        val= getTeamBowlingDetails(key,dir=dir1, save=False,odir=".")
        df = pd.concat([df,val])
    df1=df.groupby('bowler').agg(['count','mean'])
    df1.columns = ['_'.join(col).strip() for col in df1.columns.values]
    df2 =df1[['wicket_count','wicket_mean','econrate_mean']]
    df3=df2[df2['wicket_count']>10]
    df4=df3.sort_values(['wicket_mean','econrate_mean'],ascending=False)
    df4.columns=['matches','wicket_mean','econrate_mean']
    return(df4)

#########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 28 Feb 2020
# Function: rankBBLT20Batting
# This function ranks BBL T20 batsmen
#
###########################################################################################

def rankBBLT20Batting(dir1):      

    bbTteams = {"Adelaide Strikers":"as", "Brisbane Heat":"bh", "Hobart Hurricanes":"hh",
             "Melbourne Renegades":"mr", "Perth Scorchers":"ps", "Sydney Sixers":"ss",
             "Sydney Thunder":"st"}
    
    
    df=pd.DataFrame()
    for key in bbTteams:
        val = bbTteams[key] + "_details"
        val= getTeamBattingDetails(key,dir=dir1, save=False,odir=".")
        df = pd.concat([df,val])
        
    df1=df.groupby('batsman').agg(['count','mean'])
    df1.columns = ['_'.join(col).strip() for col in df1.columns.values]
    df2 =df1[['runs_count','runs_mean','SR_mean']]
    df3=df2[df2['runs_count']>20]
    df4=df3.sort_values(['runs_mean','SR_mean'],ascending=False)
    df4.columns=['matches','runs_mean','SR_mean']
    return(df4) 
    
#########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 28 Feb 2020
# Function: rankBBLT20Bowling
# This function ranks BBL T20 bowlers
#
###########################################################################################
    
def rankBBLT20Bowling(dir1):
    bbTteams = {"Adelaide Strikers":"as", "Brisbane Heat":"bh", "Hobart Hurricanes":"hh",
             "Melbourne Renegades":"mr", "Perth Scorchers":"ps", "Sydney Sixers":"ss",
             "Sydney Thunder":"st"}
                    
    df=pd.DataFrame()
    for key in bbTteams:
        val = bbTteams[key] + "_details"
        val= getTeamBowlingDetails(key,dir=dir1, save=False,odir=".")
        df = pd.concat([df,val])
    df1=df.groupby('bowler').agg(['count','mean'])
    df1.columns = ['_'.join(col).strip() for col in df1.columns.values]
    df2 =df1[['wicket_count','wicket_mean','econrate_mean']]

    df3=df2[df2['wicket_count']>10]
    df4=df3.sort_values(['wicket_mean','econrate_mean'],ascending=False)
    df4.columns=['matches','wicket_mean','econrate_mean']
    return(df4)
    
