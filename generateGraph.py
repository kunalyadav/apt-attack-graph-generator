import json
import random
from expression import convert_postfix

# print systems
def createGraph(scenario, parent):
    systems = parent["systems"]
    attackParentSet = parent["attackSet"]
    defenceParentSet = parent["defenceSet"]
    graph = {}
    system = []
    attackSet = []
    defenceSet = []

    for attack in scenario["parameters"]["attack"]:
        for a in attackParentSet:
            if a["name"] == attack:
                attackSet.append(a)
                break;

    for defence in scenario["parameters"]["defence"]:
        for d in defenceParentSet:
            if d["name"] == defence:
                defenceSet.append(d)
                break;

    systemName = scenario["parameters"]["system"]
    for s in systems:
        if s["name"] == systemName:
            system = s
    nodes = generateNodes(system);
    graph["nodes"] = nodes

    graph["edges"] = generateEdges(system,nodes,attackSet, defenceSet)
    return graph


def generateNodes(system):
    nodes = list()
    nodes1 = set()
    states = system["states"]
    for state in states:
        nodes1.add(state["name"])
        if "expression" in state :
            a = convert_postfix(state["expression"])
            nodes1 = nodes1 | set(a["nodes"])
    #add init node
    node={}
    node["id"] = "init"
    node["x"] = random.randint(0,100)
    node["y"] = random.randint(0,100)
    node["size"] = 2
    node["label"] ="init"
    nodes.append(node)

    for i, node1 in enumerate(nodes1):
        node = {}
        node["id"] = node1
        node["x"] = random.randint(0,100)
        node["y"] = random.randint(0,100)
        node["size"] = 2
        node["label"] = node1
        nodes.append(node)
    return nodes

def generateEdges(system,nodes,attackSet, defenceSet):
    edges = []
    labels = {node["name"]:node for node in system["states"]}
    edgeCount=0
    for v in attackSet:
        for attack in v["vulnerabilities"]:
            for l in attack["attack-scenario"]:

                edge = {}
                edge["type"] = ["arrow"]
                edge["size"] = 2
                edge["label"]=attack["name"]
                edge["color"] = "blue"
                edge["label"]=attack["name"]
                edge["id"] = "e"+str(edgeCount)
                edgeCount += 1
                if l["pre"] == "" :
                    edge["source"] = "init"
                    edge["target"] = l["post"]
                    edges.append(edge)
                elif l["pre"] in labels.keys() and l["post"] in labels.keys():
                    if "expression" not in labels[l["post"]]:
                        edge["source"] = l["pre"]
                        edge["target"] = l["post"]
                        edges.append(edge)

    for node in system["states"]:
        if "expression" in node:
            eds = convert_postfix(node["expression"])
            print "-----------"
            print eds["edges"]
            print eds["nodes"]
            print "-----------"
            for i,ed in enumerate(eds["edges"]):
                if i < len(eds["edges"])-1:
                    edge = dict()
                    edge["type"] = ["arrow"]
                    edge["size"] = 2
                    edge["color"] = "blue"
                    edge["source"] = ed[0]
                    edge["id"] = "e" + str(edgeCount)
                    edgeCount += 1
                    edge["target"] = ed[3]
                    if ed[2]=="AND": edge["color"] = "green"
                    edges.append(edge)

                    edge = dict()
                    edge["type"] = ["arrow"]
                    edge["size"] = 2
                    edge["color"] = "blue"
                    edge["source"] = ed[1]
                    edge["target"] = ed[3]
                    edge["id"] = "e" + str(edgeCount)
                    edgeCount += 1
                    if ed[2] == "AND": edge["color"] = "green"
                    edges.append(edge)
                else:
                    edge = dict()
                    edge["type"] = ["arrow"]
                    edge["size"] = 2
                    edge["color"] = "blue"
                    edge["source"] = ed[0]
                    edge["target"] = node["name"]
                    edge["id"] = "e" + str(edgeCount)
                    edgeCount += 1
                    if ed[2] == "AND": edge["color"] = "green"
                    edges.append(edge)

                    edge = dict()
                    edge["type"] = ["arrow"]
                    edge["size"] = 2
                    edge["color"] = "blue"
                    edge["source"] = ed[1]
                    edge["target"] = node["name"]
                    edge["id"] = "e" + str(edgeCount)
                    edgeCount += 1
                    if ed[2] == "AND": edge["color"] = "green"
                    edges.append(edge)

    # for df in defenceSet:
    #     for m in df["defence-mechanisms"]:
    #         for ds in m["defence-scenarios"]:
    #             prevent = ds["prevents"]
    #             pre = ds["pre"]
    #             for e in edges:
    #                 if e["source"] == pre and e["target"] == prevent:
    #                     edges.remove(e)
    #                 elif pre == "" and e["target"] == prevent:
    #                     edges.remove(e)
    return edges

def constructGraph(parent):
    # jsonString = '{"systems":[{"name":"system1","states":[{"name":"Infect users personal computer"},{"name":"Gain users terminal access"},{"name":"Gain admin credentials to victims server"},{"name":"Gain access to target server"},{"name":"Data transfer from target server to attacker server"}]},{"name":"system2","states":[]}],"defenceSet":[{"name":"set1","defence-mechanisms":[{"name":"input-sanitization","defence-scenario":[{"prevents":"sql-injection","pre":"","post":""}]}]}],"attackSet":[{"name":"set1","vulnerabilities":[{"name":"spear-phishing","attack-scenario":[{"probability":"0.001","pre":"","post":"Infect users personal computer"}]},{"name":"FEATHEADER-vulnerability","attack-scenario":[{"probability":"0.001","pre":"Infect users personal computer","post":"Remotely run command in victims terminal"},{"probability":"0.001","pre":"Remotely run command in victims terminal","post":"Gain users terminal access"}]},{"name":"keylogger","attack-scenario":[{"probability":"0.001","pre":"Gain users terminal access","post":"Gain admin credentials to victims server"}]},{"name":"access_more_instances","attack-scenario":[{"probability":"0.001","pre":"Gain admin credentials to victims server","post":"Gain access to target server"}]},{"name":"SimpleFileMover","attack-scenario":[{"probability":"0.001","pre":"Gain access to target server","post":"Data transfer from target server to attacker server"}]}]}],"scenarios":[{"name":"shady-rat","parameters":{"system":"system1","attack":["set1"],"defence":["set1"]}}]}';
    # parent = json.loads(jsonString)
    # systems = parent["systems"]
    scenarios = parent["scenarios"]
    graphs=[]
    for scenario in scenarios:
        graphs.append(createGraph(scenario,parent))
    print json.dumps(graphs)
    return json.dumps(graphs)

# constructGraph(json.loads(('{"systems":[{"name":"system1","states":[{"name":"Infect users personal computer"},{"name":"Gain users terminal access"},{"name":"Gain admin credentials to victims server"},{"name":"Gain access to target server"},{"name":"Remotely run command in victims terminal"},{"name":"Data transfer from target server to attacker server","expression":"(~Gain access to target server~OR~Gain users terminal access~)~AND~Infect users personal computer"}]},{"name":"system2","states":[]}],"defenceSet":[{"name":"set1","defence-mechanisms":[{"name":"input-sanitization","defence-scenarios":[{"prevents":"Gain admin credentials to victims server","pre":""}]}]}],"attackSet":[{"name":"set1","vulnerabilities":[{"name":"spear-phishing","attack-scenario":[{"probability":"0.001","pre":"","post":"Infect users personal computer"}]},{"name":"FEATHEADER-vulnerability","attack-scenario":[{"probability":"0.001","pre":"Infect users personal computer","post":"Remotely run command in victims terminal"},{"probability":"0.001","pre":"Remotely run command in victims terminal","post":"Gain users terminal access"}]},{"name":"keylogger","attack-scenario":[{"probability":"0.001","pre":"Gain users terminal access","post":"Gain admin credentials to victims server"}]},{"name":"access_more_instances","attack-scenario":[{"probability":"0.001","pre":"Gain admin credentials to victims server","post":"Gain access to target server"}]},{"name":"SimpleFileMover","attack-scenario":[{"probability":"0.001","pre":"Gain access to target server","post":"Data transfer from target server to attacker server"}]}]}],"scenarios":[{"name":"shady-rat","parameters":{"system":"system1","attack":["set1"],"defence":["set1"]}}]}')))
# for system in systems:
#     nodes = generateNodes(system)
#     edges = generateEdges()
#     print json.dumps(nodes)
