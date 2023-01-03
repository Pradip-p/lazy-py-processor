import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
import ipdb
import requests
import json

# https://resultsdata.elections.qld.gov.au/state2020-preference-count-district-mermaidbeach.json
# https://resultsdata.elections.qld.gov.au/state2020-primary-count-district-mermaidbeach.json

class LazyCrawler(LazyBaseCrawler):

    name = "elections"

    custom_settings = {
        'DOWNLOAD_DELAY': 0,'LOG_LEVEL': 'DEBUG','CHANGE_PROXY_AFTER':1,'USE_PROXY':True,
        'CONCURRENT_REQUESTS' : 1,'CONCURRENT_REQUESTS_PER_IP': 1,'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'JOBDIR': './crawls', 'RETRY_TIMES': 200, "COOKIES_ENABLED": True,'DOWNLOAD_TIMEOUT': 180
    }
    

    def start_requests(self): #project start from here.
        
        settings = get_project_settings()
        url = 'https://resultsdata.elections.qld.gov.au/state2020-electorates.json'

        yield scrapy.Request(url, self.parse, dont_filter=True)

    def parse(self, response):
        load = json.loads(response.text)
        electorates = load['electorates'] 
        for name in electorates:
            electorateName = name.get('electorateName')
            stub = name.get('stub')
            url = 'https://resultsdata.elections.qld.gov.au/state2020-primary-count-district-'+stub+'.json'
            yield scrapy.Request(url, self.parse_get_details, dont_filter=True, meta={'electorateName':electorateName, 'stub':stub})


    def parse_get_details(self, response):

        stub = response.meta['stub']
        electorateName = response.meta['electorateName']

        # ipdb.set_trace()

        data = json.loads(response.text)

        try:
            candidates = data['candidates']
        except: 
            pass

        Winner = False
        Runner_up = False
        
        largest = 0

        second_largest = 0

        for a in candidates:

            if not largest or  a.get('count')  > largest:
                if largest:
                    second_largest = largest
                largest = a.get('count')
    


        for candidate in candidates:

            candiate_name = candidate.get('ballotName')

            party = candidate.get('party')

            if party:
                party = party
            else:
                party = 'Independent'

            primary_vote = candidate.get('count')

            if primary_vote == largest:
                Winner = True
                # _pp = largest
            else:
                Winner = False
                # _pp = 0
            
            if primary_vote == second_largest:
                Runner_up = True
                # _pp = second_largest
            else:
                Runner_up = False
                # _pp = 0
            
            candidate_ballotOrderNumber = candidate.get('ballotOrderNumber')
            if candidate_ballotOrderNumber:
                pass
            else:
                print("No ballotOrederNumber")

            # next part is to get get_distribution_of_preferences details
            url = 'https://resultsdata.elections.qld.gov.au/state2020-preference-count-district-'+stub+'.json'
            
            return_data = get_distribution_of_preferences(url, candiate_name, candidate_ballotOrderNumber)
            ######################################### votind data
            

            url = 'https://resultsdata.elections.qld.gov.au/state2020-table-booths-'+ stub +'.json'

            ret_value = get_voting_type_data(url, candidate_ballotOrderNumber )


            yield{
                'Candiate':candiate_name,
                'Electorate':electorateName, 
                'Party':party,
                'Primary Vote':primary_vote,
                'Winner':Winner,
                'Runner_up': Runner_up,
                "2PP": return_data.get('2PP'),
                '1st Distribution': return_data.get('distribution_1st'),
                '2nd Disribution':return_data.get('disribution_2nd'),
                '3rd Distrubution': return_data.get('distrubution_3rd'),
                '4th Distribution': return_data.get('distribution_4th'),
                '5th Distribution':return_data.get('distribution_5th'),
                '6th Distribution': return_data.get('distribution_6th'),
                '7th Distribution': return_data.get('distribution_7th'),
                '8th Distribution': return_data.get('distribution_8th'),
                'Absent Early Voting' : ret_value.get('absent_early_voting'),
                'Absent Election Day':ret_value.get('absent_election_day'),
                'In Person Declaration Votes': ret_value.get('person_Declaration_Votes'),
                'Ordinary Votes': ret_value.get('ordinary_vote'),
                'Postal Declaration Votes': ret_value.get('postal_declaration_votes'),
            }


def get_distribution_of_preferences(url, candiate_name, candidate_ballotOrderNumber):
    distribution_1st = ''
    disribution_2nd = ''
    distrubution_3rd = ''
    distribution_4th = ''
    distribution_5th='' 
    distribution_6th = ''  
    distribution_7th = ''
    distribution_8th = ''
    p = 0
    data = {}
    # url = 'https://resultsdata.elections.qld.gov.au/state2020-preference-count-district-mermaidbeach.json'

    preference_response = requests.get(url)
    preference = json.loads(preference_response.text)
    
    preferenceDistributionDetails=preference.get('preferenceDistributionDetails')
    distributions = preferenceDistributionDetails.get('distributions')
    test = []
    for item in distributions:
        preferences = item.get('preferences')


        for candidate in preferences:
            
            if candidate.get('ballotName') == candiate_name:
                preferences_value = candidate.get('preferences')
                test.append(preferences_value)

        for index, value in enumerate(test):
            if index == 0:
                distribution_1st = value
            
            if index == 1:
                disribution_2nd = value
            
            if index == 2:
                distrubution_3rd = value
            if index == 3:
                distribution_4th = value
            
            if index == 4:
                distribution_5th = value
            
            if index == 5:
                distribution_6th = value
            
            if index == 6:
                distribution_7th = value
            
            if index == 7:
                distribution_8th = test.append(value)
    # to get 2pp value 
    # candidate_ballotOrderNumber
    # preference = json.loads(preference_response.text)
    candidates_pp=preference.get('candidates')

    
    # print(candidates)
    for candidate__p in candidates_pp:
        if candidate__p.get('ballotOrderNumber') == candidate_ballotOrderNumber:
            p = candidate__p.get('count')
    
    # ipdb.set_trace()
    data.update({"distribution_1st" :distribution_1st})
    data.update({"disribution_2nd": disribution_2nd})
    data.update({"distrubution_3rd" :distrubution_3rd})
    data.update({"distribution_4th": distribution_4th})
    data.update({"distribution_5th" :distribution_5th})
    data.update({"distribution_6th": distribution_6th})
    data.update({"distribution_7th" :distribution_7th})
    data.update({"distribution_8th": distribution_8th})
    data.update({'2PP': p})
    return data

def get_voting_type_data(url , candidate_ballotOrderNumber):
    absent_early_voting = '' 
    absent_election_day = ''
    person_Declaration_Votes = ''
    ordinary_vote = ''
    postal_declaration_votes = ''

    voting_count_data = requests.get(url)
    voting_data  = json.loads(voting_count_data.text)
    primary = voting_data.get('primary') #,Absent Early Voting, Absent Election Day, In Person Declaration Votes, Postal Declaration Votes
    
    for candidates in primary['booths']:
        if candidates.get('venueName') == "Absent Early Voting": #id  = 99994
            for candidate in candidates.get('candidates'):
                # print(candidate)
                if candidate.get('ballotOrderNumber') == candidate_ballotOrderNumber:
                    absent_early_voting = candidate.get('count')
    
        if candidates.get('venueName') == "Absent Election Day": #id = 99993 I
            for candidate in candidates.get('candidates'):
                # print(candidate)
                if candidate.get('ballotOrderNumber') == candidate_ballotOrderNumber:
                    absent_election_day = candidate.get('count')

        if candidates.get('venueName') == "In Person Declaration Votes": #id = 99992 
            for candidate in candidates.get('candidates'):
                # print(candidate)
                if candidate.get('ballotOrderNumber') == candidate_ballotOrderNumber:
                    person_Declaration_Votes = candidate.get('count')
        
        if candidates.get('venueName') == "Postal Declaration Votes": #id = 99991 

            for candidate in candidates.get('candidates'):
                # print(candidate)
                if candidate.get('ballotOrderNumber') == candidate_ballotOrderNumber:
                    postal_declaration_votes = candidate.get('count')
    


    for candidate in  primary['ordinary_votes'].get('candidates'):
        if candidate.get('ballotOrderNumber') == candidate_ballotOrderNumber:
            ordinary_vote = candidate.get('count')
    
        
    
    return {
        'absent_early_voting' : absent_early_voting,
        'absent_election_day' : absent_election_day,
        'person_Declaration_Votes' : person_Declaration_Votes,
        'ordinary_vote' :ordinary_vote,
        'postal_declaration_votes': postal_declaration_votes,
    }



settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
