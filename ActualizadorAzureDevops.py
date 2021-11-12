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
import pickle

class ConnectionAz:
    
    def __init__(self,token,organization):
        load_dotenv()
        self.personal_access_token = token
        self.organization= organization
        self.organization_url = f"https://dev.azure.com/{organization}"
        self.first = True
        self.project_info = {}
        self.json_repos = {}
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
        for repo in repos:
            target_dir = os.path.join("repositorios", project.name, repo.name)
            os.system(f"mkdir -p {target_dir}")
            url = f"{self.organization_url}/{project.name}/_apis/git/repositories/{repo.name}/items/documentacion/README.md"
            url_commits = f"{self.organization_url}/{project.name}/_apis/git/repositories/{repo.name}/commits"
            commits = requests.get(url_commits, allow_redirects=True, headers=headers)
            response = commits.content.decode('utf8')
            data = json.loads(response)
            if project.name in self.project_info:
                self.project_info[project.name][repo.name] = self.conditionData(data,target_dir,url,project.name, repo.name)
            else:
                self.project_info[project.name] = {}
                self.project_info[project.name][repo.name] = self.conditionData(data,target_dir,url,project.name, repo.name)

    def conditionData(self,data,target_dir,url, name_project, name_repo):
        if len(data["value"]) > 0:
                last_commit = datetime.strptime(data["value"][0]["author"]["date"], '%Y-%m-%dT%H:%M:%SZ')
                if (datetime.now()-last_commit) < timedelta(minutes=5) or self.first:
                    self.contenido = {}
                    if os.path.isdir(target_dir):
                        os.system(f"cd {target_dir}")
                        os.system(f"curl -o {target_dir}/readme.md -u username:{self.personal_access_token} {url}")
                        markdown.markdownFromFile(
                            input=f"{target_dir}/readme.md",
                            output=f"{target_dir}/readme.html",
                            extensions=['markdown.extensions.tables','markdown.extensions.attr_list','markdown.extensions.toc']
                        )
                        self.contenido = self.conditionDataJson(target_dir)
                        return self.contenido
                    else:
                        os.system(f"cd {target_dir}")
                        os.system(f"curl -o {target_dir}/readme.md -u username:{self.personal_access_token} {url}")
                        markdown.markdownFromFile(
                            input=f"{target_dir}/readme.md",
                            output=f"{target_dir}/readme.html",
                            extensions=['markdown.extensions.tables','markdown.extensions.attr_list','markdown.extensions.toc']
                        )
                        self.contenido = self.conditionDataJson(target_dir)
                        return self.contenido
                else:
                    return self.project_info[name_project][name_repo]
        else:
                return self.project_info[name_project][name_repo]

    def conditionDataJson(self,target_dir):
        f = open(f"{target_dir}/readme.html", "r")
        html = f.read()
        soup = BeautifulSoup(html)
        
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        self.contenido["dir_md"]=target_dir + "/readme.html"
        estado = False
        for i,line in enumerate(text.splitlines()):
            if i + 1 == len(text.splitlines()):
                if estado and ":" in line:
                    value = line.split(":")
                    if "," in value[1]:
                        items = []
                        for i,item in enumerate(value[1].split(",")):
                            if i + 1 == len(value[1].split(",")):
                                items.append(item)
                            else:
                                items.append(item)
                        self.contenido[value[0].replace(" ", "")] = items 
                    elif len(value) > 2:
                        urlDatos = ""
                        for i,item in enumerate(value):
                            if i!=0:
                                urlDatos += urlDatos + item
                        self.contenido[value[0].replace(" ", "")] = urlDatos.replace(" ","")
                    else:    
                        self.contenido[value[0].replace(" ", "")] = value[1]
                if line == "NOMBRE DE LA INTEGRACIÓN O DEL API":
                    estado=True
                elif line == "Tabla de contenido":
                    estado=False
            else:
                if estado and ":" in line:
                    value = line.split(":")
                    if "," in value[1]:
                        items = []
                        for i,item in enumerate(value[1].split(",")):
                            if i + 1 == len(value[1].split(",")):
                                items.append(item)
                            else:
                                items.append(item)
                        self.contenido[value[0].replace(" ", "")] = items
                    elif len(value) > 2:
                        urlDatos = value[1] + ":" + value[2]
                        self.contenido[value[0].replace(" ", "")] = urlDatos.replace(" ","")
                    else:    
                        self.contenido[value[0].replace(" ", "")] = value[1]
                if line == "NOMBRE DE LA INTEGRACIÓN O DEL API":
                    estado=True
                elif line == "Tabla de contenido":
                    estado=False
        estado=False
        self.contenido["Dominio"] = "proyecto prueba"
        return self.contenido

    # # Get the first page of projects
    def startConnect(self):
            get_projects_response = self.core_client.get_projects()
            while get_projects_response is not None:
                for project in get_projects_response.value:
                    self.clone_or_pull_repos_for_project_id(project)
                if get_projects_response.continuation_token is not None and get_projects_response.continuation_token != "":
                    # Get the next page of projects
                    get_projects_response = self.core_client.get_projects(continuation_token=get_projects_response.continuation_token)
                else:
                    # All projects have been retrieved
                    get_projects_response = None
                self.first=False
            time.sleep(15)
            self.saveJson()

    def saveJson(self):
        with open("data.json", 'w') as fp:
            json.dump(self.project_info,fp,indent=4)


#obj = ConnectionAz("eskcnx77vwndptxnqfplx2whu5gfbeomhvoftv2vbqg3limly4lq","Grupo-exito")
obj = ConnectionAz("w4bzl76t26s3zrivdpndppwwj4umbi4cfpr2ofdfcto5bkixcvgq", "juancho270")
while True:
    obj.startConnect()