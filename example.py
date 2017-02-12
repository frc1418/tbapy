import tbapy

tba = tbapy.TBA('frc1418:tba_python_example:v1.0')

team = tba.team(254)
districts = tba.team_history_districts(1418)

print('Team 254 is from %s.' % team['location'])
print('Team 1418 is/was in the %s district in 2016.' % districts['2016'])
