import random,os
from kubernetes import client,config,watch

schedule_name = "tim"
config.load_kube_config("config")
v1 = client.CoreV1Api()

def nodes_available():
    ready_nodes = []
    for n in v1.list_node().items:
        for status in n.status.conditions:
            if status.status == "True" and status.type == "Ready":
                ready_nodes.append(n.metadata.name)
    return ready_nodes


def scheduler(name,node,namespces="default"):
    target = client.V1ObjectReference()
    target.kind = "Node"
    target.api_version = "v1"
    target.name = node

    meta = client.V1ObjectMeta()
    meta.name = name
    body = client.V1Binding(target=target)
    body.target = target
    body.metadata = meta

    try:
        v1.create_namespaced_binding(namespces, body)
        return True
    except Exception as e:
        print('exception' + str(e))
        return False

def main():
    print("------------create watch----------")
    w = watch.Watch()
    for event in w.stream(v1.list_namespaced_pod,"default"):
        # print("------------stream event----------")
        # print("------------stream event----------:", event['object'])
        print("watch event：",event['object'].status.phase)
        if event['object'].status.phase == "Pending" or event['object'].status.phase == "Running":
            try:
                print ("pending state of pod:",event['object'].metadata.name)
                print("begin scheduler:")
                res = scheduler(event['object'].metadata.name,random.choice(nodes_available()))
                print("node",random.choice(nodes_available()))
                print("end scheduler:")
                get_pod = v1.read_namespaced_pod("pod-nginx","default")
                print(f"Pod is:{get_pod}")
                return True
            except Exception as e:
               print (f"error:{e}")
    print("------------end watch----------")

if __name__ == '__main__':
    main()
