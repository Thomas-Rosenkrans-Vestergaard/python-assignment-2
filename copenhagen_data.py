from collections import defaultdict
import operator
import json

def pretty_print(o):
    print(json.dumps(o, indent=2))

def create_statistics_dict(file):

    def nested_dd():
        return defaultdict(nested_dd)

    structure = nested_dd()
    with open(file) as f:
        for line in [line for line in f][1:]:
            values = list(map(int, line.split(",")))
            structure[values[0]][values[1]][values[2]][values[3]] = values[4]
            
    return structure


def ages_by_country(yearly_statistics, country_code):
    age_information = defaultdict(int)
    for area, ages in yearly_statistics.items():
        for age, codes in ages.items():
            if codes.get(country_code) is not None:
                age_information[age] = age_information[age] + codes.get(country_code)

    return age_information

def count_by_country(yearly_statistics, country_code):
    count = 0
    for area, ages in yearly_statistics.items():
        for age, codes in ages.items():
            if codes.get(country_code) is not None:
                count = count + codes.get(country_code)

    return count

def neighborhood_country_cmp(yearly_statistics, country_codes):
    result = {country_code: defaultdict(int) for country_code in country_codes}
    for area, ages in yearly_statistics.items():
        for age, codes in ages.items():
            for country_code in country_codes:
                if codes.get(country_code) is not None:
                    result[country_code][area] = result[country_code][area] + codes.get(country_code)
    
    return result

def top_5_in_age_range(yearly_statistics, min_age = None, max_age = None):
    result = defaultdict(int)
    for area, ages in yearly_statistics.items():
        for age, codes in ages.items():
            if (min_age is None or age >= min_age) and (max_age is None or age <= max_age):
                for code, amount in codes.items():
                    result[code] = result[code] + amount

    return {item[0]:item[1] for item in sorted(result.items(), key=operator.itemgetter(1), reverse=True)[0:5]}


country_dict = None
with open('country_codes.json') as f:
    country_dict = json.load(f)

def get_country_name(code):
    if country_dict is None:
        return "Not loaded"
        
    return country_dict.get(str(code))

def normalize(a, b, default):
    for k in a.keys():
        if k not in b:
            b[k] = default