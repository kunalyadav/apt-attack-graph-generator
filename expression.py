import json
class Stack:
     def __init__(self):
         self.items = []
     def isEmpty(self):
         return self.items == []
     def push(self, item):
         self.items.append(item)
     def pop(self):
         return self.items.pop()
     def peek(self):
         return self.items[len(self.items)-1]
     def size(self):
         return len(self.items)
     def __repr__(self):
         return repr(self.items)


def convert_postfix(exprs):
    splits = exprs.split('~')
    st = Stack()
    lists = list()
    st1 = Stack()

    edges = list()
    nodes = set()

    #print(splits)
    for ch in splits:
        #print(st)
        if ch == "(":
            st.push(ch)
        elif ch == "OR" or ch == "AND":
            st.push(ch)
        elif ch == ")":
            while st.peek() != "(":
                lists.append(st.pop())
            st.pop()
        else: lists.append(ch)

    while not st.isEmpty():
        lists.append(st.pop())

    #print(lists)
    count = 0
    for ch in lists:
        if ch == "OR" or ch == "AND":
            op1 = st1.pop()
            op2 = st1.pop()

            tempNode = "temp" + str(count)
            count += 1
            edges.append((op1, op2, ch, tempNode))
            nodes.add(op1)
            nodes.add(op2)
            nodes.add(tempNode)
            st1.push(tempNode)
        else:
            st1.push(ch)

    #print(edges)
    #print(nodes)
    if st1.peek() in nodes: nodes.remove(st1.peek())

    return {"nodes": list(nodes), "edges": edges}
    #print(result)


# res = convert_postfix("(~A~OR~B~)~AND~C")
# print(res)