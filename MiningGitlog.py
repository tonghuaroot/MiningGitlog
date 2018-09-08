from git import Repo, exc
import re
import tempfile
import argparse
import requests

parser = argparse.ArgumentParser(description='Mining mail information from git log.')
parser.add_argument("-u", "--url", dest="git_url", help="The url address of the git repository")
parser.add_argument("-d", "--dir", dest="repo_dir", help="Local address of the git repository")
parser.add_argument("-un", "--username", dest="username", help="Please enter the github username")
parser.add_argument("-on", "--orgname", dest="orgname", help="Please enter the github organization name")
parser.add_argument("--debug", dest="debug", help="Turn on debug mode")
parser.add_argument("-t", "--token", dest="github_token", help="Please enter github token")
parser.set_defaults(git_url=None)
parser.set_defaults(repo_dir=None)
parser.set_defaults(username=None)
parser.set_defaults(orgname=None)
parser.set_defaults(debug=True)
parser.set_defaults(token=None)
args = parser.parse_args()

mail_list = []

def get_user_repos(username, page=1):
    github_token = args.github_token
    response = requests.get(url='https://api.github.com/users/' + username + '/repos?page={}&token={}'.format(page, github_token))
    json = response.json()
    if not json:
        return None
    for item in json:
        if item['private'] == False and item['fork'] == False:
            #print('searching ' + item["html_url"])
            print_result(item["html_url"])
    get_user_repos(username, page + 1)

def print_log_mail(repo_dir):
    try:
        repo = Repo(repo_dir)
    except exc.NoSuchPathError as e:
        exit('The current address is not a git repository, please re-enter.')
    git = repo.git
    log = git.log()
    pattern = re.compile(r'<.*?>')
    tmp_mail_set = set(pattern.findall(log))
    global mail_list
    for i, val in enumerate(list(tmp_mail_set)):
        val = val.strip('>').strip('<')
        mail_list.append(val)
        print('Found: {}'.format(val))

def clone_git_repo(git_url):
    project_path = tempfile.mkdtemp()
    try:
        Repo.clone_from(git_url, project_path)
    except exc.GitCommandError as e:
        exit('The git repository url is incorrect, please re-enter.')
    return project_path

def print_result(git_url):
    repo_dir = clone_git_repo(git_url)
    print_log_mail(repo_dir)

def traversing_and_print_set(set_name):
    for i in set_name:
        print(i)

def traversing_and_save_set(set_name):
    with open('result', 'w') as result:
        for i in set_name:
            result.write(i)
            result.write('\n')

if __name__ == '__main__':
    if args.git_url:
        print_result(args.git_url)
        print('The collection is complete, please check the result file.')
        traversing_and_save_set(set(mail_list))
    elif args.repo_dir:
        print_log_mail(args.repo_dir)
        print('The collection is complete, please check the result file.')
        traversing_and_save_set(set(mail_list))
    elif args.username:
        get_user_repos(args.username)
        print('The collection is complete, please check the result file.')
        traversing_and_print_set(set(mail_list))   
        traversing_and_save_set(set(mail_list))
    elif args.orgname:
        get_user_repos(args.orgname)
        print('The collection is complete, please check the result file.')
        traversing_and_print_set(set(mail_list))
        traversing_and_save_set(set(mail_list))
    else:
        print(
"""usage: MiningGitlog.py [-h] [-u GIT_URL] [-d REPO_DIR] [-un USERNAME]
                       [-on ORGNAME] [--debug DEBUG]

Mining mail information from git log.

optional arguments:
  -h, --help            show this help message and exit
  -u GIT_URL, --url GIT_URL
                        The url address of the git repository
  -d REPO_DIR, --dir REPO_DIR
                        Local address of the git repository
  -un USERNAME, --username USERNAME
                        Please enter the github username
  -on ORGNAME, --orgname ORGNAME
                        Please enter the github organization name
  --debug DEBUG         Turn on debug mode
  -t GITHUB_TOKEN, --token GITHUB_TOKEN
                        Please enter github token
"""
)

