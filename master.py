import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import math

# 创建一个空的多重有向图
G = nx.MultiDiGraph()

# 读取Excel文件
df = pd.read_excel('lib.xlsx', index_col=0, engine='openpyxl')

# 获取name列的所有元素
names = df.index.tolist()

# 添加节点
for name in names:
    G.add_node(name)

# 选择第二列到最后一列
df_selected = df.iloc[:, 1:]
for col in df_selected.columns:
    # 获取值为1的节点和值为0的节点
    nodes_1 = df_selected[df_selected[col] == 1]
    nodes_0 = df_selected[df_selected[col] == 0]
    
    if not nodes_1.empty and not nodes_0.empty:
        node_1 = nodes_1.index[0]
        node_0 = nodes_0.index[0]
        
        # 将这两个节点链接起来
        G.add_edge(node_1, node_0)
        #读取这一列最上方的日期，作为边的weight
        date = pd.to_datetime(col)
        month_day = f"{date.month}-{date.day}"
        #print({month_day})
        G[node_1][node_0][0]['weight'] = month_day

# # 添加边
# G.add_edge("A", "B")
# G.add_edge("A", "B")
# G.add_edge("A", "B")
# G.add_edge("B", "C")
# G.add_edge("C", "D")
# G.add_edge("D", "A")


# 获取节点的位置
pos = nx.shell_layout(G)

# 绘制节点
nx.draw_networkx_nodes(G, pos)

# 绘制标签
nx.draw_networkx_labels(G, pos)

# 绘制边
for i, (u, v, d) in enumerate(G.edges(data=True)):
    if 'rad' not in d:
        d['rad'] = 0.05 * math.sin(i)
    nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], connectionstyle=f'arc3, rad = {d["rad"]}')

# 获取边的权重
in_degrees = G.in_degree()
out_degrees = G.out_degree()

# 创建一个字典，键是节点，值是入度和出度的字符串
labels = {node: f"\n\n in:{in_deg}\n\n out:{out_deg} \n\n" for node, in_deg in in_degrees for node, out_deg in out_degrees}

# 绘制节点的标签
nx.draw_networkx_labels(G, pos, labels=labels)

# 获取边的权重
edge_labels = nx.get_edge_attributes(G, 'weight')

edge_labels_dict = {(u, v): label for (u, v, key), label in edge_labels.items()}

# 绘制边的标签
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_dict)

# 显示图形
plt.show()