from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from dotenv import load_dotenv
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import markdown
import requests
import base64
import os
import json
import time

class ConnectionAz:
    
    def __init__(self,token,organization):
        load_dotenv()
        self.personal_access_token = token
        self.organization= organization
        self.organization_url = f"https://dev.azure.com/{organization}"
        self.first = True
        # Create a connection to the org
        self.credentials = BasicAuthentication('', self.personal_access_token)
        self.connection = Connection(base_url=self.organization_url, creds=self.credentials)
        # Get a client (the "core" client provides access to projects, teams, etc)
        self.core_client = self.connection.clients.get_core_client()

    def clone_or_pull_repos_for_project_id(self,project):
        git_client = self.connection.clients.get_git_client()
        repos = git_client.get_repositories(project.id)
        authorization = str(base64.b64encode(bytes(':'+self.personal_access_token, 'ascii')), 'ascii')
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Basic '+authorization
        }
        os.system(f"mkdir -p repositorios/{project.name}")
        self.createJsonResponse(headers,repos,project)

    def createJsonResponse(self,headers,repos,project):
        json_repos = {}
        for repo in repos:
            target_dir = os.path.join(os.getcwd(),"repositorios", project.name, repo.name)
            os.system(f"mkdir -p {target_dir}")
            url = f"{self.organization_url}/{project.name}/_apis/git/repositories/{repo.name}/items/documentacion/README.md"
            url_commits = f"{self.organization_url}/{project.name}/_apis/git/repositories/{repo.name}/commits"
            commits = requests.get(url_commits, allow_redirects=True, headers=headers)
            response = commits.content.decode('utf8').replace("'", '"')
            data = json.loads(response)
            self.conditionData(data,target_dir,url,project.name, repo.name)
            
        

    def conditionData(self,data,target_dir,url, name_project, name_repo):
        if len(data["value"]) > 0:
                last_commit = datetime.strptime(data["value"][0]["author"]["date"], '%Y-%m-%dT%H:%M:%SZ')
                if ((datetime.now()+timedelta(hours=5))-last_commit) < timedelta(seconds=70) or self.first:
                    if os.path.isdir(target_dir):
                        os.system(f"cd {target_dir}")
                        os.system(f"curl -o {target_dir}/readme.md -u username:{self.personal_access_token} {url}")
                        markdown.markdownFromFile(
                            input=f"{target_dir}/readme.md",
                            output=f"{target_dir}/readme.html",
                            extensions=['markdown.extensions.tables','markdown.extensions.attr_list','markdown.extensions.toc']
                        )
                    else:
                        os.system(f"cd {target_dir}")
                        os.system(f"curl -o {target_dir}/readme.md -u username:{self.personal_access_token} {url}")
                        markdown.markdownFromFile(
                            input=f"{target_dir}/readme.md",
                            output=f"{target_dir}/readme.html",
                            extensions=['markdown.extensions.tables','markdown.extensions.attr_list','markdown.extensions.toc']
                        )

    # # Get the first page of projects
    def startConnect(self):
            get_projects_response = self.core_client.get_projects()
            index = 0
            while get_projects_response is not None:
                for project in get_projects_response.value:
                    index += 1
                    self.clone_or_pull_repos_for_project_id(project)
                if get_projects_response.continuation_token is not None and get_projects_response.continuation_token != "":
                    # Get the next page of projects
                    get_projects_response = self.core_client.get_projects(continuation_token=get_projects_response.continuation_token)
                else:
                    # All projects have been retrieved
                    get_projects_response = None
                self.first=False
            time.sleep(60)


obj = ConnectionAz("n3v2clv6wvup6hqnjfkvv5yuggnlyiooemrtewhpxqif7d5lnjsa","juancho270")
while True:
    obj.startConnect()