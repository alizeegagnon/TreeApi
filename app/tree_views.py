from app import app
from flask import request, jsonify
from flask_cors import CORS
from flask import send_file, send_from_directory, safe_join, abort
import networkx as nx
import random
import time

#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


#app.config["DEBUG"] = True
#app.config['CORS_HEADERS'] = 'Content-Type'
app.config["CLIENT_IMAGES"] = "/home/alizee/Work/code/treeApi/flaskApp/app/static"

@app.route("/learn/flask")
def tutorial():
    return "Hello world!"

@app.route('/api/v1/getTree', methods=['GET'])
def api_get_tree():
    try:
        arity = int(request.args['arity'])
        depth = int(request.args['depth'])
        qty = int(request.args['qty'])
    except ValueError:
        abort(400)
    print(arity,depth,qty)
    if arity > 10 or depth > 20 or qty > 300:
        abort(413)

    if  not paramsAreNotValid(arity,depth,qty):

        val = getTree(arity,depth,qty) 
    else:
        val = "La quantité de sommets soumise est trop grosse pour l'arité et la profondeur. Il faudrait une quantité qui n'est pas plus grande que " + str(getMaxNodes(arity,depth))+"."
    response = jsonify({"val": str(val)})
    response.headers.add("Access-Control-Allow-Origin", "*")
    print(val)
    return response


@app.route('/api/v1/putTree', methods=['PUT'])
def api_put_tree():
    data = getList(request.data.decode("utf-8"))
    arity = int(data[0])
    depth = int(data[1])
    qty = int(data[2])
    if  not paramsAreNotValid(arity,depth,qty):

        val = getTree(arity,depth,qty) 
    else:
        val = "La quantité de sommets donnée est trop grosse pour l'arité et la profondeur. Il faudrait une quantité qui n'est pas plus grande que " + str(getMaxNodes(arity,depth))
    response = jsonify({"val": str(val)})
    response.headers.add("Access-Control-Allow-Origin", "*")
    print(val)
    return response


@app.route('/api/v1/getTreeImage', methods=['PUT'])
def api_get_tree_image():
    #arity = request.args.get('arity')
    #depth = request.args.get('depth')
    #qty  = request.args.get('qty')

    #val = arity + depth + qty
    data = getList(request.data.decode("utf-8"))
    arity = int(data[0])
    depth = int(data[1])
    qty = int(data[2])
    if  not paramsAreNotValid(arity,depth,qty):

        val = getTree(arity,depth,qty) 
    
        H = nx.Graph(val)
        nx.draw(H, with_labels=True, font_weight='bold')
        timestamp = time.time()
        path = "/home/alizee/Work/code/treeApi/treegenerator/src/graph"+str(timestamp)+".png"
        plt.savefig(path)
        plt.savefig("./app/static/graph.png")
        plt.clf() 
    else:
        val = "La quantité de sommets donnée est trop grosse pour l'arité et la profondeur. Il faudrait une quantité qui n'est pas plus grande que " + str(getMaxNodes(arity,depth))
        path = "/home/alizee/Work/code/treeApi/blank.png"

    response = jsonify({"val": str(val), "url": path})
    response.headers.add("Access-Control-Allow-Origin", "*")
    try:
        return send_from_directory("/home/alizee/Work/code/treeApi/flaskApp/app/static", path="graph.png",as_attachment=True)
    except FileNotFoundError:
        abort(404)



def getTree(arity,depth,qty):
    nodesLeft = [qty-i for i in range(qty)]
    maxNodes = getMaxNodes(arity,depth)
    if len(nodesLeft) == 0 or len(nodesLeft) == 1:
        return []
    
    root = nodesLeft.pop()
    treeStruct = [None for i in range(maxNodes)]
    treeStruct[0] = root
    for i in getChildren(0,arity):
        treeStruct[i] = 0
    adjList = []

    while len(nodesLeft) > 0:
        node = nodesLeft.pop()
        index = random.choice(getZeroIndices(treeStruct))
        treeStruct[index] = node
        for i in getChildren(index,arity):
            if i < maxNodes:
                treeStruct[i] = 0

    for i in range(len(treeStruct)):
        if treeStruct[i] is not None:
            for j in getChildren(i, arity):
                if j < maxNodes and isANode(treeStruct[j]):
                    adjList.append((treeStruct[i], treeStruct[j]))

    return(adjList)

def getList(string):
    string = string[1:-1]
    print(string)
    return string.split(',')

def getZeroIndices(array):

    indices = []
    for i in range(len(array)):
        if array[i] == 0:
            indices.append(i)
    return indices

def padWithNones(array, length):
  
    while length >= len(array):
        array.append(None)
    return array

def isANode(value):
    return value is not None and value != 0

def getMaxNodes(arity,depth):
    if arity > 1:
        return int((1 - arity**(depth+1))/(1-arity))
    else:
        return arity*depth

def paramsAreNotValid(arity,depth,qty):
    maxNodes = getMaxNodes(arity,depth)
    return maxNodes < qty

def getChildren(index,arity):
    children = []
    for i in range(arity):
        children.append(index*arity+i+1)
    return children

    
