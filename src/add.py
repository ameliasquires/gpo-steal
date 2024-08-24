from common import *

def get_name(url: str) -> str:
    name = url.split("/")[-1]

    if str(name).endswith(".git"):
        name = name[0:-4]
    return name
                

def get_repo(inp: str) -> repo_pair:
    if str(inp).startswith("http"):
        obj: repo_pair = {"url" : inp, "name":""}
        name = get_name(inp)

        obj["name"] = name

        return obj
    elif '/' in str(inp):
        return get_repo(f"https://github.com/{inp}")
    else:
        data = requests.get("https://qa-reports.gentoo.org/output/repos/repositories.xml")
        xml = xmltodict.parse(data.text)
        close = [x for x in xml["repositories"]["repo"] if x["name"] == inp or SequenceMatcher(None, inp, x["name"]).ratio() > 0.6]
        found = [x for x in close if x["name"] == inp]
        
        if len(found) > 0:
            if len(found) == 1:
                valid_sources = [x for x in found[0]["source"] if x["@type"] == "git"]

                return get_repo(valid_sources[0]["#text"])
            else:
                print("multiple results found (TODO)")
                exit(1)
        else:
            if len(close) == 0:
                print("no exact or close matches")
                exit(1)

            names = [x["name"] for x in close]
            choice = questionary.select("no direct matches found, similar results", names).ask()
            use = [x for x in close if x["name"] == choice]
            valid_sources = [x for x in use[0]["source"] if x["@type"] == "git"]

            return get_repo(valid_sources[0]["#text"])


