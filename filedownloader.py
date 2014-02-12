import httplib
import urllib2
import math


#url of the file to be downloaded
url = "http://content.rim.com.edgesuite.net/content/Desktop/BlackBerryLink122/bundle010/122_b010_multilanguage.exe"

#get the name of the file to be downloaded
file_name = url.split('/')[-1]
print file_name

#initaiating the connection
conn = httplib.HTTPConnection("192.168.1.10",8000)
#send the reqeust
conn.request("HEAD", url)
#get the response
res = conn.getresponse()
print res.status,res.reason
print res.getheaders()

#get the size of the file
file_size = res.getheader('content-length')
print file_size
#close the connection
conn.close()

#create a file with the above file name and file size
f = open(file_name,"wb")
f.seek(int(file_size)-1)
f.write("\0")
f.close()

#declare the number of MBs in each chunk
no_of_mbs = 1
#decide the chunk size
chunk_size = no_of_mbs * 1000000 #this is in bytes, which is equal to no_of_mbs MB(s)
#get the number of chunks
no_of_chunks = math.ceil(float(file_size)/chunk_size);
no_of_chunks = int(no_of_chunks)
print no_of_chunks

#set the request
req = urllib2.Request(url);

#set the proxy
proxy = urllib2.ProxyHandler({'http': '192.168.1.88:8000'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)

#open the file
f = open(file_name, 'wb')

#download file chunk by chunk
for i in range(0, no_of_chunks):
    req.headers['Range'] = 'bytes=%s-%s' % (i*chunk_size, ((i+1)*chunk_size)-1)
    u = urllib2.urlopen(req)
    #print the content-length
    print u.info().getheader('content-length')
    #seek the correct place to write
    f.seek(i*chunk_size)
    #write to the file
    f.write(u.read())

#close the file
f.close()

