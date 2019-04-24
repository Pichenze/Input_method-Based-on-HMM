#coding:utf-8
from os.path import exists
import pickle

def Get_Params(param_filename = 'param.pkl',reloaded=False):
	if exists(param_filename) and not reloaded:
		A,B,E,pydict = pickle.load(open(param_filename, 'rb'))
		return A,B,E,pydict
	else:
		Pset = [] # Pinyin 集合，暂时没用到
		ChineseSet = []  # 中文集合，暂时没用到
		pydict = {}  #记录某个拼音对应的汉字列表
		# 统计pydict , PSet , ChineseSet
		with open('pinyin.txt','r') as f:
			for row in f.readlines():
				s = row.strip('\n').split(':') #将读取的行先除去后面的\n，然后用：将其分开，s[0]是拼音，s[1]是该拼音对应的所有中文汉字组成的字符串
				pydict[s[0]] = list(s[1])  #将一串字符串转为list就可以得到字符串所有单个字符组成的列表
				Pset.append(s[0])
				ChineseSet = ChineseSet+list(s[1])

		# 统计E 发射矩阵的信息
		E = {}
		for key,chinese in zip(pydict.keys(),pydict.values()):
			for i in range(len(chinese)):
				if chinese[i] not in E:
					E[chinese[i]]={}
					E[chinese[i]][key]=1
				else:
					if key not in E[chinese[i]]:
						E[chinese[i]][key]=1
					else:
						E[chinese[i]][key]+=1


		#无stopword版本
		A = {} #A保存每个字符后面对应字符出现的次数
		B = {} #B保存单个字符出现的在句首的次数
		stopword = list(',，.。“”‘┤’、\'\";:?![]}(「){\n\t\b》《')
		# 统计A,B中的矩阵信息，A[x,y]即y出现在x后面的次数
		with open('pinyin_train.txt','r',encoding='utf-8') as f:
			# 每一行
			for row in f.readlines():
				# 每一行的首个汉字，计算B
				word = row[0]
				if word in stopword: #当前字符就是符号，直接continue
					continue;
				if word not in B:
					B[word] = 1
				else:
					B[word] += 1
				# 第row行的后续汉字，统计A
				for i in range(len(row)-1):
					word = row[i]
					if word in stopword: #当前字符就是符号，直接continue
						continue;
					if row[i+1] in stopword: #当前单词的后面是字符，那就不需要在A中添加
						continue;
					if word not in A:
						A[word] = {}
						A[word][row[i+1]]=1
					else:
						if row[i+1] not in A[word]:
							A[word][row[i+1]]=1
						else:
							A[word][row[i+1]] += 1


		# 计算 A 转移矩阵的概率值
		for cur,nexts in zip(A.keys(),A.values()):
			cur_sum = sum(A[cur].values())
			for nextword in nexts:
				A[cur][nextword] = A[cur][nextword]/cur_sum

		# 计算 B 初态矩阵的概率值
		start_sum = sum(B.values())
		for key in B.keys():
			B[key] = B[key]/start_sum

		#计算 E 发射矩阵的概率值
		for Chinese,pinyins in zip(E.keys(),E.values()):
			ch_sum = sum(E[Chinese].values())
			for pinyin in pinyins:
				E[Chinese][pinyin] = E[Chinese][pinyin]/ch_sum
		pickle.dump((A,B,E,pydict), open(param_filename, 'wb'))
		return A,B,E,pydict


