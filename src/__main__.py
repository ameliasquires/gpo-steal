#!/usr/bin/env python3
import copy
from common import *
from sync import *
from add import *
from rm import *

if len(sys.argv) == 1:
    print("gentoo portage overlay steal (gpo-steal), written by amelia (https://github.com/ameliasquires)")
    print("\tlicensed under 3-clause BSD, see license for more info")
    print("")
    print("utility for copying packages from a overlay to yours")
    print("")
    print("usage:")
    print(" sync - selects repository to update from source, also updates tracked packages")
    print(" add [repository] - adds a overlay, accepts git links, github account/name (ex: gentoo/gentoo),")
    print("\tand between everything listed on https://overlays.gentoo.org/")
    print(" delete - remove a repository")
    print(" copy [package] - searches all added repositories for package, accepts package-name,")
    print("\tpackage-location/package-name, do not use : to specify repository")
    print(" rm [package] - removes or untracks a package, accepts the same params as copy, but allows : to specify repository")
    print(" ls - lists all tracked packages (not untracked, yet installed ones)")
    print("")
    exit(0)

match sys.argv[1]:
    case "sync" | "s":
        options = list(repos.keys())
        name = questionary.select("which repository", ["all", *options]).ask()
        sync_repos = repos.values()
        if name != "all":
            sync_repos = [repos[name]]

        sync(sync_repos)

    case "add" | "a":
        assert len(sys.argv) >= 3

        obj = get_repo(sys.argv[2])
 
        repos[obj["name"]] = obj
    
        save()

        if questionary.confirm("sync repository?").ask():
            sync([obj])

    case "delete" | "del" | "d":
        options = list(repos.keys())
        name = questionary.select("which repository", options).ask()
        del_repos = [repos[name]]

        oper = questionary.select("delete", ["repository", "entry & repository"]).ask()

        if not questionary.confirm("are you sure?").ask():
            print("exiting")
            exit(0)
        
        for r in del_repos:
            full_path = os.path.join(REPO_LOC, r["name"])
            print("del "+ full_path)
            
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
            if oper == "entry & repository":
                del repos[name]

        save()

    case "copy" | "c":
        assert len(sys.argv) >= 3

        search = sys.argv[2]
        full = '/' in search

        options = []

        for r in repos:
            path = os.path.join(REPO_LOC, r)

            if full:
                full_path = os.path.join(path, search)
                if os.path.isdir(full_path):
                    options.append({"path": search, "repo": r, "full_name": f"{search}:{r}"})
                    print(options)

            else:
                if not os.path.isdir(path):
                    continue
                repo = os.listdir(path) 
                for dir in repo:
                    dir_path = os.path.join(path, dir)

                    if os.path.isdir(dir_path):
                        for f in os.listdir(dir_path):
                            if f == search:

                                full_path = os.path.join(dir_path, f)
                                name = os.path.join(dir, search)
                                options.append({"path": name, "full_path": full_path, "repo": r, "full_name": f"{name}:{r}" })
                   
        use = None
        if len(options) > 1:
            choices = [i["full_name"] for i in options]
            choice = questionary.select("select an option", choices).ask()
            use = [x for x in options if x["full_name"] == choice][0]
        elif len(options) == 1:
            use = options[0]
        else:
            print("no matches")
            exit(0)
        
        cmd = copy.copy([use])
        eexec(cmd)

    case "r" | "rm":
        assert len(sys.argv) >= 3

        search = sys.argv[2]
        has_repo = ":" in search

        if has_repo:
            [search, repo] = search.split(":")

            if not repo in tracked:
                print("repository has no tracked packages")
                exit(1)
            
            rm(search, [repo])
        else:
            rm(search, tracked.keys())

    case "ls" | "l" | "list":

        if len(sys.argv) >= 3:
            if not sys.argv[2] in tracked:
                print("nothing in repo")
                exit(1)

            for i in tracked[sys.argv[2]]:
                print(i)
        else:
            for r in tracked.keys():
                for p in tracked[r]:
                    print(f"{p}:{r}")
