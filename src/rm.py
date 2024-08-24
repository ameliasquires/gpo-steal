from common import *

def rm_pkg(pkg) -> None:
    cmd = f"{root} rm -fr {os.path.join(FULL_REPOS_LOCATION, pkg)}"
    print(cmd)
    os.system(cmd)

def rm(pkg, repos) -> None:

    found = []
    for r in repos:
        for t in tracked[r]:
            if t.endswith(pkg):
                found.append({"path": t, "repo": r})

    use = None

    if len(found) == 0:
        print("not found")
        exit(1)
    elif len(found) == 1:
        use = found[0]
    else:
        names = [f"{x["path"]}:{x["repo"]}" for x in found]
        selected = questionary.select(f"{pkg} is ambiguous, select a more specific package", names).ask().split(":")
        use = [x for x in found if x["path"] == selected[0] and x["repo"] == selected[1]][0]
        print(use)
    
    op = questionary.select("remove", ["package", "track", "package & track"]).ask()

    if op == "package" or op == "package & track":
        rm_pkg(use["path"])
    if op == "track" or op == "package & track":
        tracked[use["repo"]].remove(use["path"])
        save()


