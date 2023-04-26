# 传播模型trace生成说明

已知用户post 记录，可以使用传播模型模拟post在社交网络中的传播过程，当post在某个时间点t传播到用户结点n时，便认为该节点产生了一条view记录，具体地，一条view记录用（t, view_node, post_id）三元组表示。

有关传播模型生成trace的工作目录为 `code/trace/propagation_model/`，该目录下包含了使用**不同的传播模型**生成**不同社交网络**用户数据的脚本。其中传播模型脚本的命名规则为: `model_` + `模型名称` + `.py` ，社交网络trace生成的脚本明明规则为：`make_` + `社交网络名称` + `trace.py` 

### 1 获取post trace

post trace的获取可以是真实的用户签到、发帖记录，或者是依据相关分布模拟的用户post记录。

不同数据集获取post的方式可能有所不同，因此在 `code/trace/propagation_model`目录下包含了

#### 1.1  twitter post

对于当前系统使用的twitter数据集来说，只有用户的社交网络关系图，没有其他的信息，因此twitter post仍然需要自己模拟生成。

具体地，先使用 `code/trace/make_trace_twitter.py` 脚本生成 `all_timeline.txt`， 即利用最初的仿真方法生成包含post和view的trace，可以忽略这里的view trace

### 2 传播模型生成trace

在获取了用户的post之后，可以选择使用不同的传播模型来生成view trace，一般来说，使用post和传播模型生成trace的一般步骤为:

1. 导入社交网络关系图
2. 导入节点地理位置（如果数据集本身已经包含，则不需要）
3. 导入post trace
4. 根据不同的传播模型生成view trace
5. 合并post和view，并根据时间戳生成完整的trace并导出

```python
if __name__ == "__main__":
    print("make twitter trace")
    twitter_file = "TwitterSmall"
    mtt = make_twitter_trace("./data/traces/" + twitter_file +"/all_timeline.txt")
    mtt.load_graph("./data/traces/" + twitter_file + "/relations.txt")
    mtt.load_location("./data/static/user_country.csv")
    mtt.load_post("./data/traces/" + twitter_file + "/all_timeline.txt")
    mtt.gen_trace()
    mtt.export_trace()
```

#### 2.1  独立级联模型(idenpendent cascade)

该模型的**基本假设**是节点 u试图激活其邻接节点 v 的行为能否成功是一个概率为 p（u,v ）的事件。且一个处于非活跃状态的节点被刚进入活跃状态的邻居节点激活的概率独立于之前曾尝试过激活该节点的邻居的活动。

此外该模型还做出了这样的假设：网络中任意的节点 u 只有一次机会尝试激活其邻居节点 v，无论能否成功，在以后的时刻中，u 本身虽然仍保持活跃状态，但它已经不再具备影响力，这一类节点称为 **无影响力的活跃节点** 。

**算法如下：**

1. 初始的活跃节点集合 A。
2. 在 t 时刻，新近被激活的节点 u 对它的邻接节点 v 产生影响，成功的概率为 p（u,v ）。若v有多个邻居节点都是新近被激活的节点，那么这些节点将以任意顺序尝试激活节点v。
3. 如果节点 v 被激活成功，那么在 t+1 时刻，节点 v 转为活跃状态，将对其邻接非活跃节点产生影响；否则，节点 v 在 t+1 时刻状态不发生变化。
4. 该过程不断进行重复，直到网络中不存在有影响力的活跃节点时，传播过程结束。

**脚本实现:** 

```python
def propagation(G, seed, interval=600, p=0.5, max_time=6):
    '''
    G: easygraph.Graph
    seed: list of seed nodes
    p: float(0, 1) activation probability
    max_time: int max time of propagation
    '''
    trace = []
    all_active_nodes = []
    all_active_nodes.append(G.nodes[seed])

    time = 0
    active_nodes = [seed]
    while len(active_nodes) > 0 and time <  max_time * interval :
        new_active_nodes = []

        # traverse all active nodes in last round
        for node in active_nodes:
            # try to active neighbors of each active node
            for neighbor in G.neighbors(node):
                if neighbor in all_active_nodes or neighbor in new_active_nodes:
                    # if neighbor is already active, continue
                    continue
        
                if random.random() < p:
                    # not chosed to be active, continue
                    continue

                new_active_nodes.append(neighbor)
                all_active_nodes.append(neighbor)

                randtime = (time + interval * random.randint(1, 10000)/10000)
                trace.append((randtime, neighbor))

        active_nodes = new_active_nodes
        time += interval

    return trace
```

包含三个可以调节的参数：interval、p、max_time

- interval: 相邻两次传播的时间间隔，其中view时间在该时间步长内随机生成
- p: 激活概率，影响力节点激活邻居节点的概率
- max_time: 传播过程的最大迭代次数
