# 起源: http://www.matrix67.com/blog/archives/475 中的正则表达式：^1?$|^(11+?)\1+$
# 想验证一下用这个正则表达式输出的所有数字（结果很像N以内的所有素数）与N以内的素数是什么集合关系

import sys

COLUMN = 13 	# number of column per line
def output_in_pair(sorted1, sorted2, default=None):
	i1 = i2 = 0 	# index of sorted1 and sorted2
	column = 0		# current column number, used to prettify output in rows
	not_finish = True
	lent1, lent2 = len(sorted1), len(sorted2)
	while not_finish:
		if i1 >= lent1:
		# list sorted1 exhausted or len == 0, output remaining sorted2 and exit
			for x in xrange(i2, lent2):
				print (default, sorted2[x]),
				column += 1
				if column == COLUMN:
					column = 0
					print
			not_finish = False
			break
		elif i2 >= lent2:
		# list sorted2 exhausted or len == 0, output remaining sorted1 and exit
			for x in xrange(i1, lent1):
				print (sorted1[x], default),
				column += 1
				if column == COLUMN:
					column = 0
					print
			not_finish = False
			break

		m,n = sorted1[i1], sorted2[i2]
		x = 0	# new index
		if m == n:
			print (m, n),
			column += 1
			if column == COLUMN:
				column = 0
				print
			i1 += 1
			i2 += 1
		elif m > n:
			# m > n, print sorted2 until n >= m or to the end of sorted2
			for x in xrange(i2, lent2):
				if sorted2[x] < m:
					print (default, sorted2[x]), 
					column += 1
					if column == COLUMN:
						column = 0
						print
				else:
					break
			if sorted2[x] >= m:
				i2 = x
			else:
				# reach the end
				i2 = x + 1

		else:
			# m < n, print sorted1 until m >= n or to the end of sorted1
			for x in xrange(i1, lent1):
				if sorted1[x] < n:
					print (sorted1[x], default), 
					column += 1
					if column == COLUMN:
						column = 0
						print
				else:
					break
			if sorted1[x] >= n:
				i1 = x
			else:
				# reach the end
				i1 = x + 1
	# print a new line to end the output
	if column != 0:
		print

# test case
if __name__ == "__main__":
	import random
	import re

	NUMBER_OF_GROUP = 1000	# number of test
	MAX_LEN = 30			# max number of elements in a test list
	MAX_COMMON_LEN = 10		# max number of common elements in two list

	regroup = re.compile(r'\(.*?\)')
	re_none_in_t1 = re.compile(r'\(None, \d+\)')
	re_none_in_t2 = re.compile(r'\(\d+, None\)')

	for i in range(NUMBER_OF_GROUP):
		t1 = set([random.randint(0, 10000) for j in range(random.randint(0, MAX_LEN))])
		t2 = set([random.randint(0, 10000) for j in range(random.randint(0, MAX_LEN))])
		common = set([random.randint(0, 10000) for j in range(random.randint(0, MAX_COMMON_LEN))])
		t1 = sorted(t1 | common)
		t2 = sorted(t2 | common)
		
		f = open('/tmp/result.txt', 'w')
		sys.stdout = f
		print t1
		print t2
		output_in_pair(t1, t2)
		sys.stdout = sys.__stdout__
		f.close()

		f = open('/tmp/result.txt', 'r')
		result = f.read()
		f.close()

		num_group = len(regroup.findall(result))
		num_none_t1 = len(re_none_in_t1.findall(result))
		num_none_t2 = len(re_none_in_t2.findall(result))
		if num_group != len(set(t1) | set(t2)):
			print "group No.", i
			print t1
			print t2
			print "size mismatch, num_group: ", num_group, "len t1|t2 :", len(set(t1)|set(t2))
			break
		elif num_none_t1 != len(set(t2) - set(t1)):
			print "group No.", i
			print t1
			print t2
			print "t1 None mismatch, num_group: ", num_none_t1 , "len t2-t1 :", len(set(t2) - set(t1))
			break
		elif num_none_t2 != len(set(t1) - set(t2)):
			print "group No.", i
			print t1
			print t2
			print "t2 None mismatch, num_group: ", num_none_t2 , "len t1-t2 :", len(set(t1) - set(t2))
			break
		else:
			# assume nothing wrong 
			pass
	print "after", NUMBER_OF_GROUP, "groups of test, the number of value pair, number of elements in t2 - t1, number of elements in t1 - t2 are correct. so I __assume__ the algorithm is correct"

