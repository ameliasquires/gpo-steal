from common import *

def copy(use_d) -> None: 
        
    srcs = []
    dests = []
    for use in use_d:
        if not use["repo"] in tracked:
            tracked[use["repo"]] = []
        if not use["path"] in tracked[use["repo"]]:
            tracked[use["repo"]].append(use["path"])
        save()

        srcs.append(os.path.join(REPO_LOC, use["repo"], use["path"]))
        dests.append(os.path.join(FULL_REPOS_LOCATION, use["path"]))

    cmd = f"{root} sh -c 'mkdir -p {' '.join(dests)};"
    for i in range(len(dests)):
        cmd += f"cp -r {srcs[i]}/* {dests[i]};"
    cmd += "'"
    print(cmd)
    os.system(cmd)


