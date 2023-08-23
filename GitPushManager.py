import os
from SubprocessHandler import run
import datetime


# A concise interface function to other module:  
def listpush(list_of_repo):
    return GitPushManager.listpush(list_of_repo)

# Complete structure: 
class GitPushManager:
    def __init__(self, root_folder):
        self.root_folder = root_folder
        self.success_repo = []
        self.failed_repo = []
        self.no_effect_repo = []
        os.chdir(self.root_folder)


    def listpush(self, list_of_repo):

        for repo in list_of_repo:
            print("+" * 72)
            print(f"Current working directory: {os.getcwd()}")
            print(f"Working on repository: {repo}")
            
            # Git checkout
            return_code, _ = run(["git", "checkout", "main"], loc = repo)
            if return_code != 0:
                self.failed_repo.append(repo)
                print("Gheckout failed")
                # Continue: terminate the process for this element, proceed next element in the for-loop
                continue 

            # Git status
            return_code, stdout = run(["git", "status"], loc=repo)
            # 3 cases in 'git status': Case 1: there is something new (no need to stop). Case 2 and 3: stop the `listpush` for that repo.
            # Case 3: Other case 
            if return_code != 0:
                self.failed_repo.append(repo)
                print("Git status command failed.")
                continue # type: ignore
            # Case 2: 'Your branch is up to date'
            if "nothing to commit, working tree clean" in stdout:
                self.no_effect_repo.append(repo)
                print("This repo is new. Proceed the next repo.")
                continue # type: ignore

            # Git add all
            return_code, _ = run(["git", "add", "--all"], loc=repo)
            if return_code != 0:
                self.failed_repo.append(repo)
                print("Failed. Code: a1sd32")
                continue # type: ignore

            # Git commit
            tag_message="Automated add-commit-push"
            timetag_for_commit = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            commit_command = ["git", "commit", "-m", f"{tag_message}. Datetime tag: {timetag_for_commit}"]
            return_code, stdout = run(commit_command, loc=repo)
            # Case 2: Any other case
            if return_code != 0:
                self.failed_repo.append(repo)
                print("Failed. Code: 1zsxer2")
                continue # type: ignore
            # Case 3 (Trivial): The staging area is empty (But it is most probably blocked due to the previous `git add` control flow)
            if "nothing to commit" in stdout:
                print("No changes to commit.")
                self.no_effect_repo.append(repo)
                print("No effect to the repo. Code: t5gs2")
                continue # type: ignore
            print(f"Commit successful. Output:\n{stdout}")

            # Git push origin main
            push_command = ["git", "push", "origin", "main"]
            _, push_output = run(push_command, loc=repo)
            if "Total" in push_output:
                self.success_repo.append(repo)
                # Future development: Scrape the terminal output and collect those data to summary variable.
                print("Push completed")
            else:
                print(f"Push failed. Output:\n{push_output}")
                self.failed_repo.append(repo)
            print("=" * 72)

            self.success_repo.append(repo)
            print(f"Add-commit-push completed.")
            print("=" * 72)
            
        print("Summary:")
        print(f"Successful repos: {self.success_repo}")
        print(f"Failed repos: {self.failed_repo}")
        print(f"No effect repos: {self.no_effect_repo}")


# Testing unit: 
if __name__ == "__main__":
    # locate to the root folder 
    root_folder = os.path.join(os.path.expanduser("~"), "All_Github_Repos")
    os.chdir(root_folder)

    # get all folders 
    all_items = os.listdir(root_folder)
    repo_list = [os.path.join(".", item) for item in all_items if os.path.isdir(os.path.join(root_folder, item)) and not item.startswith('.')]
    print(f"Totally there are {len(repo_list)} repos to work on. They are: {repo_list}")
    # The result would be : ['./Video materials', './Git management', './Textual notes', './Guides', './Tutorial template', './JS webpage coding gym', './Python coding gym', './Git-flow-master']

    GitPushManager(root_folder).listpush(repo_list)


