from MiningGitlog import print_log_mail
from MiningGitlog import clone_git_repo
from MiningGitlog import print_result
from MiningGitlog import get_user_repos
from MiningGitlog import mail_list
from MiningGitlog import traversing_and_save_set

def test_print_log_mail():
    repo_dir = '/home/ubuntu/github-project/SecTools'
    print_log_mail(repo_dir)

def test_clone_git_repo():
    repo_url ='https://github.com/WhaleShark-Team/cobra.git'
    print(clone_git_repo(repo_url))

def test_print_result():
    git_url = 'https://github.com/WhaleShark-Team/cobra.git'
    print_result(git_url)

def test_get_user_repos():
    get_user_repos('omg2hei')

def test_traversing_and_save_set():
    set_name = {'root@vultr.guest', 'omg2hei@163.com', 'omg2hei@gmail.com'}
    list_name = ['aaa', 'bbb', 'ccc']
    traversing_and_save_set(set_name)    

if __name__ == '__main__':
    # test_print_log_mail()
    # test_clone_git_repo()
    # test_print_result()
    # test_get_user_repos()
    # print(mail_list)
    test_traversing_and_save_set()
