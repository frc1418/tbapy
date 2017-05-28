import tbapy

# This key should ONLY be used for this example. If using this library in your own project,
# follow the steps in the README to generate your own key.
tba = tbapy.TBA('TjUTfbPByPvqcFaMdEQVKPsd8R4m2TKIVHMoqf3Vya0kAdqx3DlwDQ5Sly4N2xJS')

team = tba.team(254)
districts = tba.team_districts(1418)
match = tba.match(year=2017,
                  event='chcmp',
                  type='sf',
                  number=2,
                  round=1)
events = tba.team_events(148, 2016)
robots = tba.team_robots(4131)

print('-' * 10 + ' Object Syntax' + '-' * 10)
print('Team 254 is from %s in %s, %s.' % (team.city, team.state_prov, team.country))
print('Team 1418 is/was in the %s district in the most recent year of competition.' % districts[-1].display_name)
print('The second qual match at the 2017 CHS District Championship was predicted to start at Unix Time %s.' % match.predicted_time)
print('In 2016, team 148 was in %d events: %s.' % (len(events), ', '.join(event.event_code for event in events)))
print('Team 4131\'s robots: ' + ', '.join('%s (%d)' % (robot.robot_name, robot.year) for robot in robots))
print()

print('-' * 8 + ' Dictionary Syntax' + '-' * 8)
print('Team 254 is from %s in %s, %s.' % (team['city'], team['state_prov'], team['country']))
print('Team 1418 is/was in the %s district in the most recent year of competition.' % districts[-1]['display_name'])
print('The second qual match at the 2017 CHS District Championship was predicted to start at Unix Time %s.' % match['predicted_time'])
print('In 2016, team 148 was in %d events: %s.' % (len(events), ', '.join(event['event_code'] for event in events)))
print('Team 4131\'s robots: ' + ', '.join('%s (%d)' % (robot['robot_name'], robot['year']) for robot in robots))
print()

print('-' * 5 + ' .json Dictionary Syntax' + '-' * 5)
print('Team 254 is from %s in %s, %s.' % (team.json['city'], team.json['state_prov'], team.json['country']))
print('Team 1418 is/was in the %s district in the most recent year of competition.' % districts[-1].json['display_name'])
print('The second qual match at the 2017 CHS District Championship was predicted to start at Unix Time %s.' % match.json['predicted_time'])
print('In 2016, team 148 was in %d events: %s.' % (len(events), ', '.join(event.json['event_code'] for event in events)))
print('Team 4131\'s robots: ' + ', '.join('%s (%d)' % (robot.json['robot_name'], robot.json['year']) for robot in robots))
