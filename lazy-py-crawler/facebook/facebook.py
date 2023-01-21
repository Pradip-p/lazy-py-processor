

import requests
# Replace YOUR_ACCESS_TOKEN with a valid access token
access_token = 'EAAEvrZB6VrBABAHIah52s4XGRhaUtclskA3k8ASfhlj7OdJL7YZB5NIG5uYqmuAb9sOsoXxzb0AAOtxyxaBsZBZBqzZBVj0X2lv8INHZCntk2EmetaOdc0Gid54XXRa0vU2tIfIPPvO49klY4Dju1IHfqIUO6R5oDcuyd0Xn0sIBSuNdufBMcGhvl3QG1XWNyfZBEFnFQaHMPQLGHGHO2ZA1z6ka6gF8NI4ZD'
# Replace GROUP_ID with the ID of the public group you want to retrieve data from
group_id = '317269872328396'

# Use the Facebook Graph API to retrieve data from the group
url = f'https://graph.facebook.com/v11.0/{group_id}?fields=name,description,feed&access_token={access_token}'
response = requests.get(url)
data = response.json()
print(data)
# Print the group name, description, and the last 5 posts on the group's feed
# print(data['name'])
# print(data['description'])
# for post in data['feed']['data'][:5]:
#     print(post['message'])
