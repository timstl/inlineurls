import urllib2
import os
import requests
import json
import time

# time to pause between each file.
# not sure if inliner.cm would block us if we went too fast.
pause = 10

# current directory
dir = os.path.dirname(os.path.realpath(__file__))

count = 0

# open urls.txt file and put urls into list
with open(dir + '/urls.txt') as u: 
	urls = u.read().splitlines()
	total = len(urls)
	print "Total URLs: " + str(total)
	
	for url in urls :	
		
		# remove trailing slash
		url = url.rstrip('/')
		
		# HTML filename for output
		filename = url.split('/')[-1] + '.html'
		
		try :
			# read the HTML from the URL
			response = urllib2.urlopen(url)
			html = response.read()
			
			try :
				# post HTML to inliner.cm for inlining
				payload = {'code' : html }
				r = requests.post('https://inliner.cm/inline.php', data=payload)
				
				# 200
				if r.status_code == requests.codes.ok :
					
					# read json response
					j = json.loads(r.text)
					
					# write to file
					with open(dir + '/' + filename, 'w') as f:
						f.write(j['HTML'].encode('utf8'))
						f.close()
						count += 1
						print "Created: #" + str(count) + " " + filename
						
				else :
					print 'Ooops, response 200 not received for: ' + filename
				
			except :
				print 'Failed getting HTML from the URL: ' + filename
			
		except :
			print 'Failed: ' + filename
	
		if count < total:
			time.sleep(pause)

print "Completed URLs: " + str(count)