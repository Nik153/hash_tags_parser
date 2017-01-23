import re
import signal
import sys
	
word_map = {}
max_len = 0

def exit_handler(arg1, arg2):
	print()
	print("Good bye!")
	sys.exit()

def get_words(filename):
	words = re.compile('[A-Za-z]+').findall(open(filename).read())
	count = 0
	len_before = len(word_map)
	for word in words:
		count += 1
		word = word.lower()
		if word not in word_map:
			word_map[word] = 1
		else:
			word_map[word] += 1
	len_after = len(word_map)
	print(filename + " processed.")
	print("Total words added: " + str(count))
	print("New unique words: " + str(len_after - len_before))

def upd_words(filename):
	words = re.compile('[A-Za-z]+').findall(open(filename).read())
	count = 0
	len_before = len(word_map)
	for word in words:
		if word in word_map:
			count += 1
			word = word.lower()
			word_map[word] += 1
	len_after = len(word_map)
	print(filename + " processed.")
	print("Total words added: " + str(count))
	print("New unique words: " + str(len_after - len_before))

def min_match(word):
	word = word.lower()
	word_len = len(word)
	result = []
	start = 0
	pos = 0
	
	while pos <= word_len:
		if word[start : pos] in word_map:
			result.append(word[start : pos] + ' ')
			start = pos
		pos += 1
	if start < word_len:
		result.append("... failed!")
	else:
		result.append("... good!")
	return result

def max_match(word):
	word = word.lower()
	word_len = len(word)
	result = []
	start = 0
	pos = word_len + 1

	while pos > start:
		pos -= 1
		if word[start : pos] in word_map:
			result.append(word[start :pos] + ' ')
			start = pos
			pos = word_len + 1
	if start < word_len:
		result.append("... failed!")
	else:
		result.append("... good!")
	return result

def bruteforce(word):
	variants = list(get_brute_list(word))
	variant = []
	for variant in variants:
		for part in variant:
			if part not in word_map:
				break;
			if part == variant[len(variant) - 1]:
				variant.append("... good!")
				return get_str_from_arr(variant)
	variant.append("... failed!")
	return get_str_from_arr(variant)

def get_str_from_arr(arr):
	res_str = ""
	for part in arr:
		res_str += part + " "
	return res_str


def get_brute_list(word):
    if word:
        for i in range(1, len(word) + 1):
            for p in get_brute_list(word[i:]):
                yield [word[:i]] + p
    else:
        yield []	

def smart_bruteforce(word):
	variants = list(get_smart_brute_list(word))
	variant = []
	for variant in variants:
		for part in variant:
			if part not in word_map:
				break
			if part == variant[len(variant) - 1]:
				variant.append("... good!")
				return get_str_from_arr(variant)
	variant.append("... failed!")
	return get_str_from_arr(variant)


def get_smart_brute_list(word):
    if word:
        for i in range(1, len(word) + 1):
            if word[:i] in word_map:
	            for p in get_smart_brute_list(word[i:]):
	            	yield [word[:i]] + p
    else:
        yield []	

def resolving_bruteforce(word):
	prob_map = {}
	variant = []
	variants = list(get_smart_brute_list(word))
	for variant in variants:
		curr_prob = 1
		for part in variant:
			if part not in word_map:
				break
			curr_prob *= word_map[part]
			if part == variant[len(variant) - 1]:
				prob_map[get_str_from_arr(variant)] = curr_prob				
	if len(prob_map) < 1:
		variant.append("... failed!")
		return get_str_from_arr(variant)			
	max_prob = 0
	max_prob_variant = " "
	for variant in prob_map:
		if max_prob < prob_map[variant]:
			max_prob = prob_map[variant]
			max_prob_variant = variant
	return max_prob_variant + "... good!"

if __name__ == "__main__":

	signal.signal(signal.SIGINT, exit_handler)


	get_words("dict.txt")
	upd_words("text.txt")

	for code in range(ord('b'), ord('z') + 1):
		ch = chr(code)
		if ch in word_map and ch != 'i':
			del word_map[ch]

	words_amm = len(word_map)
	for word in word_map:
		word_map[word] /= words_amm

	print()
	print("Type some Hashtags. Or 'quit' to leave.")
	print()

	while True:
		word = input()
		word = word.lower()
		print("Minimum Matching:     " + ''.join(min_match(word)))
		print("Maximum Matching:     " + ''.join(max_match(word)))
		print("Smart Bruteforce:     " + ''.join(smart_bruteforce(word)))
		print("Bruteforce resolving: " + ''.join(resolving_bruteforce(word)))
#		print("Bruteforce:           " + ''.join(bruteforce(word)))
		print()