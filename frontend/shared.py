user_dict = {'amy':'pw'}
routine_dict = {
# 'routine1':{
# 'start_point':"138600, UTown Residence",
# "end_point":"126754, 103 West Coast Vale",
# "start_time_value":'12:00',
# "end_time_value":'12:30',
# 'days_of_week':'Mon Tue Wed'}
}

def generate_routine_options():
    options = []
    count = 1
    for routine_id in routine_dict.keys():
        option = {'label': routine_id, 'value': str(count)}
        count += 1
        options.append(option)
    return options