from tkinter import * 
from MyViterbi import *

alphabet = [chr(i) for i in range(97,123)]
alphabet.append("'")
numbers = [str(i) for i in range(0,10)]
stopword = list(',，.。“”‘┤’、\'\";:?![]}(「){\n\t\b》《')
global result  #为执行Viterbi算法之后的到的各种可能的结果列表
global output  #为输出的汉字结果
global prev_pbuffer  #保存前一个输入buffer
global pbuffer  #保存当前buffer
prev_pbuffer = ""
pbuffer = ""
output = "Output:"

# 对连续英文字符串进行切分，切成一个一个拼音存成列表形式
def divide_pinyin(pinyin):
	pinyinlist = []
	maxPylen = 6	 
	tmp_p = ""
	i = 0
	pylen = maxPylen #一个字的拼音最大长度
	while i < len(pinyin):
		if pinyin[i]=="'": #处理“西安”这种词“xi'an”
			i += 1
		if pinyin[i:i+pylen] in pydict and "'" not in  pinyin[i:i+pylen]:
			pinyinlist.append(pinyin[i:i+pylen])
			i += pylen
			pylen = maxPylen
		else:
			pylen -= 1
			if pylen == 0:
				break
	return pinyinlist

# 键盘输入一个a-z或是0-9都会产生相应的反应，a-z用于输入拼音，0-9用于选择Viterbi算法得到的中文结果
def oneKeyPress(event):
	global pbuffer
	global result
	global output
	ibuffer = event.char #输入的按键
	# 输入了a-z
	if ibuffer in alphabet:
		pbuffer += ibuffer
		# 切割拼音
		inputlist = divide_pinyin(pbuffer)
		print(inputlist)
		result = viterbi(inputlist) #维特比算法计算
		hanzi.set(list2str(result)) #更新结果框
	# 输入了1-9
	elif ibuffer in numbers:
		if len(pbuffer)==0: #当pbuffer中没有字符时输入数字直接输入进去
			output+=ibuffer
		else:
			index = int(ibuffer)-1
			prev_pbuffer = pbuffer
			pbuffer = ''
			output+=result[index][0]
		otext.set(output)
	elif ibuffer in stopword:
		output+= ibuffer
		otext.set(output)
	print("It's "+pbuffer)	
	itext.set(pbuffer)

# 通过按<Up>可以获取输入的一串拼音字符串,再按一次回到原来的那串字符串
def prev(event):
	global pbuffer
	global prev_pbuffer
	tmp = pbuffer
	pbuffer = prev_pbuffer
	prev_pbuffer = tmp
	print("It's "+pbuffer)

# 将result中存储的结果转成str，用于更新输入结果使用
def list2str(result):
	tmp_str = ""
	for i in range(len(result)):
		tmp_str += "{0} {1} prob:{2}\n".format(i+1,result[i][0],result[i][1])
	return tmp_str

# Backspace退格，在拼音输入过程使用删去一个英文字符，pbuffer为空时删去output中的一个中文字符
def Backspace(event):
	global result
	global pbuffer
	global output
	if len(pbuffer) != 0:
		pbuffer = pbuffer[:-1]
		itext.set(pbuffer)
		# 切割拼音
		inputlist = divide_pinyin(pbuffer)
		print(inputlist)
		result = viterbi(inputlist) #维特比算法计算
		hanzi.set(list2str(result)) #修改结果框
		print('Backspace is pressed')
		print("It's ",pbuffer)
	else:
		if len(output)>7: #保证output栏固定的“Output:”不消失
			output = output[:-1]
			otext.set(output)


root = Tk()
root.geometry('500x300')

itext = StringVar()
lb_I = Label(textvariable = itext,background='black',foreground='white',font=('Comic Sans MS',12))
lb_I.pack()
# 拼音候选栏
hanzi = StringVar()
lb_Q = Label(textvariable=hanzi, font=('Comic Sans MS',12))
lb_Q.place(x=120, y=75)
lb_Q.pack()
# 最终汉字文本栏
otext = StringVar()
lb_O = Label(textvariable=otext, font=('Comic Sans MS',12))
lb_O.place()
lb_O.pack()
#pinyin = StringVar()


#root.bind('<Return>', Return)
root.bind('<BackSpace>', Backspace)
root.bind('<Up>',prev)
root.bind('<KeyPress>',oneKeyPress)

root.mainloop()
