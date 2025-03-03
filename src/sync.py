from common import *
import copy

def sync_obj(repo_name: str) -> str:
    if not repo_name in tracked:
        return ""

    cmds = ""
    for p in tracked[repo_name]:
        cmds += str(copy.copy([{"path":p, "repo": repo_name, "full_path": os.path.join(REPO_LOC, repo_name, p)}]))
    return cmds

def sync(sync_repos: list[repo_pair]) -> None:
    cmds = ""
    for r in sync_repos:
        print(r)
        full_path = os.path.join(REPO_LOC, r["name"])
        if os.path.isdir(full_path):

            old_hash = subprocess.getoutput(f"cd {full_path} && git rev-parse HEAD")
            os.system(f"cd {full_path} && git pull --quiet")

            new_hash = subprocess.getoutput(f"cd {full_path} && git rev-parse HEAD")
            
            if old_hash == new_hash:
                print(f"{r['name']}: up to date")
            else:
                print(f"{r['name']}: {new_hash}")
 
        else:
            os.system(f"cd {REPO_LOC} && git clone {r['url']} {r['name']}")
            new_hash = subprocess.getoutput(f"cd {full_path} && git rev-parse HEAD")

            print(f"{r['name']}: {new_hash}")

        if questionary.confirm("would you like to sync all tracked packages, from this repo?").ask():
            cmds += sync_obj(r["name"])

    if cmds != "":
        eexec(cmds)


