# PSoC1Term for Linux and Mac user

# please install pyserial
import serial
import argparse

# 27443 only
LastBlock = 215

# 引数処理
parser = argparse.ArgumentParser(description='how to use')
parser.add_argument('-o', dest='ttypath', required=True, metavar='SerialPort',
					help='set SerialPort absolute path')
parser.add_argument('-i', dest='fname', required=True, metavar='filename',
					help='PSoC1duino HEXcode filename')
args = parser.parse_args()
fname = args.fname
tty = args.ttypath 
# デバッグ用
# print(fname)
# print(tty)

try:
	# serial port open
	com = serial.Serial(tty, 115200, timeout=1)

	# 7byte読み込む
	for i in range(0,7):
		com.read(1)

	# OK! と書き込む
	com.write(bytearray("OK!",'ascii'))

	# 3byte読み込む
	for i in range(0,3):
		com.read(1)

	# connected!
	print("connect!")

	# ファイル読み込み
	f = open(fname,'r')

	# 1行飛ばす
	f.readline()

	for j in range(1,LastBlock):
		# 進捗どうですか？
		print(str(int(j*100/LastBlock)) + "%",end="\r")
		# Sを書き込む
		com.write(bytearray("S",'ascii'))
		# ファイルから1行読み込み
		line = f.readline()
		for i in range(1,137,2):
			# 2文字を1byteに変換
			two = line[i:(i+2)]
			val = int(two,16)
			# 書き込み
			com.write(bytes((val,)))
		# Fを書き込む
		com.write(bytearray("F",'ascii'))
		# 2byte読み込む
		com.read(1)
		com.read(1)

	# 書き込み完了
	print("100%")
	print("finish!")

finally:
	# 何か起きたらとりあえず閉じる
	# file close
	f.close
	# serial close
	com.close()
