a,b,c = {},{},{}

def return_min_dict(dict_list):
    min = 100
    min_dict = {}
    for dict in dict_list:
        if dict['blah'] < min:
            min = dict['blah']
            min_dict = dict
    return min_dict


a['blah'] = 3
b['blah'] = 4
c['blah'] = 5

dicts = [a,b,c]

min_dict = return_min_dict(dicts)
print str(min_dict['blah'])

dicts.remove(b)

for dict in dicts:
    print dict

if 5 > 2:
    print 'yep'
elif 5 > 3:
    print 'yep2'