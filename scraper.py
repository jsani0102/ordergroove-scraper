import urllib2

# constants
url = 'http://ordergroove.com/company'

def process_html_str(html):
	total_tags = 0
	tag_counts = {}

	while len(html) > 0:
		start_index = html.find('<')
		if (start_index == -1):
			break

		end_index = html[start_index:].find('>')
		tag = html[start_index:start_index + end_index + 1]
		if is_valid_start_tag(tag):
			total_tags += 1

			html_elt = extract_tag_element(tag)
			if html_elt in tag_counts:
				tag_counts[html_elt] += 1
			else:
				tag_counts[html_elt] = 1

		html = html[start_index + end_index + 1:]

	return total_tags, tag_counts

def is_valid_start_tag(tag):
	if len(tag) >= 3:
		# examining first character after opening tag
		first_ch_tag = ord(tag[1])
		if first_ch_tag >= ord('a') and first_ch_tag <= ord('z'):
			return True

	return False

def extract_tag_element(tag):
	# do not want opening tag character
	components = tag[1:].split()
	# there are other attributes (class, href, etc.) in the tag 
	if len(components) > 1:
		return components[0]
	else:
		# the tag has no attributes, slice off ending tag character
		return components[0][:-1]

# unit tests
test_total, test_counts = process_html_str('<div><p></p></div>')
assert(test_total == 2)
assert(test_counts['p'] == 1)
assert(test_counts['div'] == 1)

assert(is_valid_start_tag('<h4>') == True)
assert(is_valid_start_tag('<div class=\"cell-wrapper layout-widget-wrapper\"') == True)
assert(is_valid_start_tag('</script>') == False)
assert(is_valid_start_tag('<!--end footer -->') == False)

assert(extract_tag_element('<li>') == 'li')
assert(extract_tag_element('<strong>') == 'strong')
assert(extract_tag_element('<script type=\"text/javascript\"') == 'script')
assert(extract_tag_element('<p style=\"text-align: center;\"') == 'p')


# main routine
response = urllib2.urlopen(url)
html = response.read()

total, counts = process_html_str(html)
print "Total HTML Elements: %s \n" % str(total)

elements = counts.keys()
elements.sort(key=lambda elt: counts[elt], reverse=True)
elts_to_print = min(len(elements), 5)
print "Top %s HTML Elements:" % str(elts_to_print)

for i in range(elts_to_print):
	elt = elements[i]
	print elt + " - " + str(counts[elt])
