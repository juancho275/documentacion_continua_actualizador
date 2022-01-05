from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from dotenv import load_dotenv
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import markdown
import requests
import base64
import os
from dotenv import load_dotenv
import json
import time
import pickle
import zipfile
import io

load_dotenv()



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
        os.makedirs(f"./../documentacion_continua/data/repositorios/{project.name}", exist_ok = True)
        self.createJsonResponse(headers,repos,project)

    def createJsonResponse(self,headers,repos,project):
        for repo in repos:
            target_dir = os.path.join(os.getenv('RUTA_LECTURA'), project.name, repo.name)
            os.makedirs(target_dir, exist_ok = True)

            url = f"{self.organization_url}/{project.name}/_apis/git/repositories/{repo.name}/items?path=/documentacion/&$format=zip&download=true"
            url_commits = f"{self.organization_url}/{project.name}/_apis/git/repositories/{repo.name}/commits"
            commits = requests.get(url_commits, allow_redirects=True, headers=headers)
            response = commits.content.decode('utf8')
            data = json.loads(response)
            if project.name in self.project_info:
                self.project_info[project.name][repo.name] = self.conditionData(data,target_dir, url, headers,project.name, repo.name)
            else:
                self.project_info[project.name] = {f"{repo.name}" : {} }
                print(project.name)
                print(repo.name)
                self.project_info[project.name][repo.name] = self.conditionData(data,target_dir, url, headers,project.name, repo.name)

    def conditionData(self,data,target_dir, url, headers, name_project, name_repo):
        if len(data["value"]) > 0:
                last_commit = datetime.strptime(data["value"][0]["author"]["date"], '%Y-%m-%dT%H:%M:%SZ')
                if (datetime.now()-last_commit) < timedelta(minutes=75) or self.first:
                    self.contenido = {}

                    os.system(f"cd {target_dir}")
                    # os.system(f"curl -o {target_dir}/README.md -u username:{self.personal_access_token} {url}")

                    # donwload documents files
                    print(f"Downloading... from: {url} \n")
                    res_dir = requests.get(url, headers=headers)
                    exist_readme = False
                    if res_dir.status_code == 200:
                        zip = zipfile.ZipFile(io.BytesIO(res_dir.content))
                        zip.extractall(f'{target_dir}')

                        # check if there is a img file in the folder
                        # to save all the path and the img file into the static folder
                        for zip_file in zip.filelist:
                            zip_filename = zip_file.filename
                            file_ext = zip_filename.split('.')[-1]

                            if file_ext.lower() in ['jpeg', 'png', 'jpg', '.gif']:
                                target_dir_img  = target_dir.replace('data', 'static/img')
                                os.makedirs(target_dir_img, exist_ok = True)
                                zip.extract(zip_filename, target_dir_img)
                            if file_ext.lower() in ['md']:
                                exist_readme = True
                                readme_name = zip_filename


                    else:
                        # when fails its because of it doesnot found the documentacion folder
                        # so download directly the README.md
                        print(f'Documentacion folder not found')
                        for readme_name in ["README", "readme", "Readme"]:
                            readme_name =  f"{readme_name}.md"                      
                            url_readme = f"{self.organization_url}/{name_project}/_apis/git/repositories/{name_repo}/items/{readme_name}"
                            print(f"Try donwoload {readme_name} in {url_readme}")
                            res_md = requests.get(url_readme, headers=headers)

                            if res_md.status_code == 200:
                                os.makedirs(f"{target_dir}/documentacion", exist_ok= True )
                                with open(f"{target_dir}/documentacion/{readme_name}", "wb") as f:
                                    f.write(res_md.content)
                                readme_name = f"/documentacion/{readme_name}"
                                exist_readme = True

                                break


                    if not exist_readme:
                        # ignore this repositorio
                        return {}
                    
                    try:
                        markdown.markdownFromFile(
                            input=f"{target_dir}/{readme_name}",
                            output=f"{target_dir}/documentacion/readme.html",
                            extensions=['markdown.extensions.tables','markdown.extensions.attr_list','markdown.extensions.toc']
                        )
                        self.contenido = self.conditionDataJson(target_dir)
                    except:
                        with open(f"log.txt", 'a') as f:
                            f.write(f"{url} \n")
                            
                        print(f"WARNING!!! cheg log.txt repo has something bad: {url}")
                        return {}



                    # Edit readme html file to modify the img src
                    with open(f"{target_dir}/documentacion/readme.html", "r") as f:
                        html = f.read()
                        soup = BeautifulSoup(html, features="html.parser")

                    all_img = soup.find_all('img')
                    exits_src_img = False
                    for img in all_img:
                        nameFile = img['src'].split('/')[-1]
                        file_ext = nameFile.split('.')[-1]
                        # img src file also contains another formats
                        if file_ext in ['jpeg', 'png', 'jpg', '.gif']:
                            src_img = f"/static/img/{target_dir.split('/data/')[-1]}/documentacion/{nameFile}"
                            img['src'] = src_img
                            exits_src_img = True

                    # save the edited soup html
                    if exits_src_img:
                        with open(f"{target_dir}/documentacion/readme.html", "w") as fw:
                            fw.write(str(soup))

                    return self.contenido

                else:
                    return self.project_info[name_project][name_repo]
        else:
                return self.project_info[name_project][name_repo]

    def conditionDataJson(self,target_dir):
        f = open(f"{target_dir}/documentacion/readme.html", "r")
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
        

        target_dir_front = '/'.join(target_dir.split('/')[3:])

        self.contenido["dir_md"]= f'./{target_dir_front}/documentacion/readme.html'
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

        for nombreColumna in ['Dominio', 'Proyecto', 'Área', 'AnalistaÁgil', 'PalabrasClave',
                'Infraestructuradedespliegue', 'SistemasOrigen', 'SistemasDestino', 'Tipodesarrollo',
                'VersiónLenguaje', 'URLConsumoApi']:

            if not self.contenido.get(nombreColumna):
                self.contenido[nombreColumna] = 'Default'
  
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
            time.sleep(60)
            self.saveJson()

    def saveJson(self):
        with open(os.getenv('RUTA_JSON'), 'w') as fp:
            json.dump(self.project_info,fp,indent=4)

obj = ConnectionAz(os.getenv('TOKEN'),os.getenv('ORGANIZACION'))
#obj = ConnectionAz("dbkw64dunfza546u5gee3ey7xbidvixqdhypoeiax7565bvudx4q", "grupo-exito")
while True:
    obj.startConnect()
    


	
	
	
