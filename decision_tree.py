
import math
import json

headers = ['Color', 'Size', 'Shape', 'Edible']

dataset = [
    ['Color', 'Size', 'Shape', 'Edible'],
    ['Yellow', 'Small', 'Round', 'Yes'],
    ['Yellow', 'Small', 'Round', 'No'],
    ['Green', 'Small', 'Irregular', 'Yes'],
    ['Green', 'Large', 'Irregular', 'No'],
    ['Yellow', 'Large', 'Round', 'Yes'],
    ['Yellow', 'Small', 'Round', 'Yes'],
    ['Yellow', 'Small', 'Round', 'Yes'],
    ['Yellow', 'Small', 'Round', 'Yes'],
    ['Green', 'Small', 'Round', 'No'],
    ['Yellow', 'Large', 'Round', 'No'],
    ['Yellow', 'Large', 'Round', 'Yes'],
    ['Yellow', 'Large', 'Round', 'No'],
    ['Yellow', 'Large', 'Round', 'No'],
    ['Yellow', 'Large', 'Round', 'No'],
    ['Yellow', 'Small', 'Irregular', 'Yes'],
    ['Yellow', 'Large', 'Irregular', 'Yes']
]


def getColumn(dataset, colId):
    return [row[colId] for row in dataset]


def getDecisionOfColumn(col):
    decision = []
    for x in col:
        if x not in decision:
            decision.append(x)
    return decision


def calcEntropy(dataset, colId):
    ent = 0
    count = {}
    col = getColumn(dataset, colId)
    decisions = getDecisionOfColumn(col)
    for decision in col:
        if decision not in count.keys():
            count[decision] = 1
        else:
            count[decision] += 1
    for x in count:
        prob = count[x] / len(col)
        ent -= prob * math.log2(prob)

    return ent


def selectAttribute(dataset):
    min = 999
    selected = -1
    for x in range(len(dataset[0])-1):
        ent = calcEntropy(dataset[1:], x)
        if ent < min:
            min = ent
            selected = x
    return selected


def selectData(dataset, colId, decision):
    selected = []
    headers = list(dataset[0])
    del headers[colId]
    selected.append(headers)
    for row in dataset[1:]:
        if row[colId] == decision:
            newRow = list(row)
            del newRow[colId]
            selected.append(newRow)
    return selected


def buildTree(dataset):
    tree = {}
    attr = selectAttribute(dataset)
    col = getColumn(dataset[1:], attr)
    tree[dataset[0][attr]] = {}

    decisions = getDecisionOfColumn(col)
    for decision in decisions:
        tree[dataset[0][attr]][decision] = {}
        buildBranch(dataset, tree[dataset[0][attr]][decision], attr, decision)
    return tree


def buildBranch(ds, parent, parentAttr, decision):
    subData = selectData(ds, parentAttr, decision)
    attr = selectAttribute(subData)
    col = getColumn(subData[1:], attr)
    parent[subData[0][attr]] = {}
    decisions = getDecisionOfColumn(col)
    if len(decisions) == 1 or attr == -1:
        parent[subData[0][attr]][decisions[0]] = {}
        parent[subData[0][attr]][decisions[0]
                                 ]["answer"] = subData[0][-1]+" = "+decisions[0]
        return
    for dec in decisions:
        parent[subData[0][attr]][dec] = {}
        buildBranch(subData, parent[subData[0][attr]][dec], attr, dec)


tree = buildTree(dataset)
file_out = open("result.js", "w")
file_out.write("const tree = " + str(tree))
file_out.close()
print(tree)
