#coding:utf-8
import math
from HMMParams import Get_Params

A,B,E,pydict = Get_Params()

# 获取当前观测值（拼音）可能对应的所有状态（汉字）
def get_states(curobs):
	return pydict[curobs]

# 获取state状态（汉字）出现在开头的概率
def start(state):
	if state in B:
		return B[state]
	else:
		return 0
# 获取 state状态（汉字）发射得到curobs（拼音）的概率
def emission(state,cur_obs):
	if state in E:
		if cur_obs in E[state]:
			return E[state][cur_obs]
	return 0
# 获取 cur状态（汉字）下一个状态为nexts（汉字）的概率
def transition(cur, nexts):
	if cur in A:
		if nexts in A[cur]:
			return A[cur][nexts]
	return 0

# 定义HMM中的节点，包含state(汉字)，prob(该节点在改状态并且得到相应观测值的概率)，previous(当前state产生最大概率对应的前一个节点，用于寻找最优路径)
class node():
	def __init__(self,state=None,prob=0,previous_node=None):
		self.state = state
		self.prob = prob
		self.previous=previous_node

def viterbi(observations,path_num=7,min_prob=1e-10):
	L = [[]] #L[t]表示t时刻的所有状态节点的集合
	t = 0  # t指在观测值的t时刻
	if len(observations) == 0:
		return []
	cur_obs = observations[t]  #当前观测值，拼音

	# 初始状态(t == 0)
	cur_states = get_states(cur_obs)  # wordset ，获取当前观测值对应的所有状态，数据结构为['妳', '伲', '愵', '拟'....]
	for state in cur_states:
		#print(state,start(state),emission(state, cur_obs)) #蛮多状态初始是0，因为概率计算一直是相乘，因此会导致整个句子受影响，因此应该设一个min_prob作为最低概率值
		tmp_prob = max(start(state),min_prob)* max(emission(state, cur_obs),min_prob)
		#print(tmp_prob)
		L[t].append(node(state,tmp_prob))
	print(len(observations))
	# 后续转移状态 t > 0
	for t in range(1, len(observations)):
		L.append([]) #L按层（t）存储，L[t]存储第t层的所有节点的信息
		cur_obs = observations[t]  # cur_obs为当前观测值
		prev_nodes = L[t-1] #prev_nodes 为前一层的所有节点
		cur_states = get_states(cur_obs) #获取cur_obs可能对应的所有states
		for state in cur_states: # 对t层每个state
			tmp_node = node(state=state)
			max_prob = 0
			for prev_node in prev_nodes: #对t-1层每个node(state)
				tmp_prob = prev_node.prob * max(transition(prev_node.state,state),min_prob) * max(emission(state, cur_obs),min_prob)
				if tmp_prob>max_prob:
					tmp_node.prob = tmp_prob
					tmp_node.previous = prev_node
					max_prob = tmp_prob
			L[t].append(tmp_node)

	L[t] = sorted(L[t], key=lambda nodee: nodee.prob, reverse=True) # 按L[t]每个node概率排序
	# 根据L[t]的最优node找出最优路径，及其prob
	result = []
	for i in range(path_num):
		if i >= len(L[t]): # 如果L[t]层的结果比想要的path少，那就只能把pathnum设小，退出循环
			path_num = len(L[t])
			break
		cur_node = L[t][i]
		tmp_dict = {}
		tmp_list = []
		while cur_node.previous != None:
			tmp_list.append(cur_node.state)
			cur_node = cur_node.previous
		tmp_list.append(cur_node.state)

		tmp_str = "".join(tmp_list)[::-1] #字符串逆序
		result.append([tmp_str,L[t][i].prob])
	return result

'''
def get_input(pinyin):
	obs = pinyin.split()
	for ob in obs:  #拼音输入是否符合规范，符合规范的的拼音应该能在pydict里面找到该拼音
		if ob not in pydict.keys():
			return None  #返回None,不需要运行Viterbi
	return obs  #返回obs观测值列表

def pinyin2hanzi(pinyin):
	inputt = get_input(pinyin)
	print(inputt)
	if inputt == None:
		return None
	if len(inputt)==0:
		return None
	result = viterbi(inputt)
	print(result)
	return result
'''

