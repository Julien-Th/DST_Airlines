# Github project Best practices
## Init Github

First steps :
- join the Repository (after invitation)
- On VS Code : 
    - connect to a machine (Via a DST lesson by example)
    - `ssh-keygen` and Enter 3 times
    - copy the content of /home/ubuntu/.ssh/id_rsa.pub
- On github :
    - go into your profile > Settings > SSH and GPG keys
    - **New SSH Key** and choose your title and copy the previous content in **Key**
- On VS Code :
    - clone the project : `git clone https://github.com/Julien-Th/DST_Airlines.git`

## Developer's guide
### Develop on your branch
- update your main branch : `git checkout main` then `git pull`
- create a new branch : `git branch feature\my_new_feature`
- go on your branch : `git checkout feature\my_new_feature`
- develop your things
- (optional) if someone has pushed some devs on the main branch since you created your branch, you need to include these devs by rebasing :
    - `git checkout main`
    - `git pull`
    - `git checkout feature\my_new_feature`
    - `git rebase main`
    - if needed, correct the conflicts
- once you've finished your feature :
    - `git add .`
    - `git commit -m "a message explaining what you developed"`
    - `git push`

### Common commands
- `git status` : you can spam this command => it tells you the status of your branch
- `git checkout` : change branch