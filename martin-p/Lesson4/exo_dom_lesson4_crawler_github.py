""" Crawl the best GitHub users'name and sort them by stars average """

__author__ = 'martin'

import requests
from bs4 import BeautifulSoup
import json
import numpy as np
import operator

""" Class to use utils functions """
class Util:

    # Returns a soup object from a given url
    @staticmethod
    def getSoupFromUrl(url):
        result = requests.get(url)
        if result.status_code == 200:
            return BeautifulSoup(result.text, "html5lib")
        else:
            print 'Request failed', url
        return None


""" Class to use GitHub crawler """
class GitHubCrawler:

    mainUrl = "https://gist.github.com/paulmillr/2657075"

    # Get names of the contributors
    def getContributorsName(self, nbContributors):
        contributorsName = []

        soupGitHub = Util.getSoupFromUrl(self.mainUrl)
        tableInfoContributors = soupGitHub.find(class_="markdown-body js-file ").find('table').find('tbody')
        infoContributors = tableInfoContributors.find_all('tr')

        for infoContributor in infoContributors :
            if len(contributorsName) < nbContributors:
                contributorsName.append(infoContributor.select('a:nth-of-type(1)')[0].string)
            else:
                 break
        return contributorsName


""" Class to use GitHub API """
class GitHubApi:

        def __init__(self):
            self.userName = 'martin-prillard'

        # Get average stars of contributors
        def getContributorMeanStars(self, userPassword, url, nbPages):
            starsList =[]
            for nbPage in range(1, nbPages+1):
                # Get request to have informations on this contributor
                req = requests.get(url + '/repos?page=' + str(nbPage) + '&per_page=100', auth=(self.userName, userPassword))
                # Get all infos on all repos
                reposDictionnary = json.loads(req.content)
                # For each respos
                for repoInfos in reposDictionnary:
                    # Get only the number of stars
                    starsList.append(repoInfos.get('stargazers_count'))
            # Return the average stars
            if len(starsList) == 0:
                return 0
            else :
                return np.mean(starsList)



def main():
    contributorsNumber = 10
    contributorsPagesInfo = 2
    userPassword = raw_input('password : ')

    # Initialize objects crawler and API
    crawler = GitHubCrawler()
    api = GitHubApi()
    print 'Searching users contributors...'
    # Get names of the contributors
    contributorsName = crawler.getContributorsName(contributorsNumber)

    print str(len(contributorsName)) + ' usersname contributors found.'
    # Create ranking for contributors
    contributorsRank = dict()
    # For each contributors
    print 'Calculating average stars for each contributors...'
    for contributorName in contributorsName :
        # We calculate the stars average
        meanStars = api.getContributorMeanStars(userPassword, 'https://api.github.com/users/' + contributorName, contributorsPagesInfo)
        # Put contributor's name with contributor's average stars
        contributorsRank.update({contributorName : meanStars})

    # Sort the contributors by their average stars
    contributorsRank = sorted(contributorsRank.iteritems(),
                              reverse=True,
                              key=operator.itemgetter(1))
    print '\nRanking :'
    # Display the result
    for key, value in contributorsRank:
        print str(value) + " : " + key


# Launch the program
if __name__ == "__main__":
    main()