import requests

verbose = False
# Response Parsing Template
# {
#     "total_count": 16171506,
#     "incomplete_results": False,
#     "items": [
#         {
#             "private": False,
#             "url": "https://api.github.com/repos/Snailclimb/JavaGuide",
#             "html_url": "https://github.com/Snailclimb/JavaGuide",
#             "fork": False,
#             "stargazers_count": 143601,
#             "language": "Java",
#             "topics":
#             [
#                 "algorithms",
#                 "interview",
#                 "java",
#                 "jvm",
#                 "mysql",
#                 "redis",
#                 "spring",
#                 "system",
#                 "system-design",
#                 "zookeeper",
#             ],
#             "visibility": "public",
#         },
#     ],
# }

class GitHubAPI:
    def __init__(self, access_token, languages = ["Java"], topics = ["maven"], filename = "pom.xml", results_per_page=100) -> None:
        self.parameters = {
            "access_token": access_token,
            "languages": languages,
            "topics": topics,
            "filename": filename,
            "results_per_page": results_per_page,
        }
        self.headers = {
            "Accept": "application/vnd.github.text-match+json",
            "Authorization": f"Bearer {access_token}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        self.base_apiurl =  "https://api.github.com/search/repositories"
        self.base_query = self.build_base_query()
    
    def build_base_query(self):
        query = "?q="

        # Add requested languages to the search query
        if len(self.parameters["languages"]) > 0: query += "language:" + self.parameters["languages"][0]
        for language in self.parameters["languages"][1:]:
            query += f"+language:{language}"

        # Add requested topics to the search query
        if len(self.parameters["topics"]) > 0:
            if len(self.parameters["languages"]) > 0:
                query += "+topic:" + self.parameters["topics"][0]
            else:
                query += "topic:" + self.parameters["topics"][0]
        for topic in self.parameters["topics"][1:]:
            query += f"+topic:{topic}"

        # Only search for public repositories
        if len(self.parameters["languages"]) > 0 or len(self.parameters["topics"]) > 0: query += "+"
        query += "is:public"

        # Only include main repositories
        # excluding any forks
        query += "+-is:fork"

        # Append number of search results
        # per page to the base query
        query += f"&per_page={self.parameters['results_per_page']}"

        return query
    
    def perform_search(self, page_num):
        # Extend the base URL to fetch
        # multiple pages of the search.
        final_url = self.base_apiurl + self.base_query + f"&page={page_num}"
  
        if verbose: print(f"{'Index':6s} - {'HTML_URL':85s} - {'Private':7s} - {'Visibility':10s} - {'Language':10s} - {'Fork':5s}")
        
        # Query and fetch results
        indx = 1
        valid_repos = []
        response = requests.get(url=final_url, headers=self.headers)
        if response.status_code == 200:
            response_dict = response.json()
            # Use field URL to query if the response
            # repositories contains desired filename
            for item in response_dict["items"]:
                if self.validity_check(url=item["url"]):
                    valid_repos += [item['html_url']]
                    if verbose: print(f"{str(indx):6s} - {item['html_url']:85s} - {str(item['private']):7s} - {str(item['visibility']):10s} - {str(item['language']):10s} - {str(item['fork']):5s}")
                    indx += 1

        # Return final list of repositories
        return valid_repos
  
    def validity_check(self, url):
        # Make a query to the github api
        response = requests.get(url=url+f"/contents/{self.parameters['filename']}", headers=self.headers)
        if response.status_code == 200: return True    
        return False