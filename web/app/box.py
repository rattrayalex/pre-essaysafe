from xml.dom import minidom
import httplib
import urllib2
import mimetools
import mimetypes


# Initialize and Make Connection
box_api_key = 'e74usd65esyarrz614h75i93ik10kku4'
box_ticket = 'n9bczfm5xfg1lpi3m0hv3825zk1o0vdh'
box_auth = '8kf9roqysu8jmqskys9vg0hovkmyqtv3'

conn = httplib.HTTPConnection("www.box.net")

prefix = "prof_"


## Functions
def uploadFile(data, FID=0):

  boundary = mimetools.choose_boundary()

  body = ""

  # filename
  body += "--%s\r\n" % (boundary)
  body += 'Content-Disposition: form-data; name="share"\r\n\r\n'
  body += "%s\r\n" % ('1')
  body += "--%s\r\n" % (boundary)
  body += "Content-Disposition: form-data; name=\"file\";"
  url = 'http://upload.box.net/api/1.0/upload/%s/%s' % ('8kf9roqysu8jmqskys9vg0hovkmyqtv3', FID)
  #postData = body.encode("utf_8") + data
  postData = body.encode("utf_8") + data + ("\r\n--%s--" % (boundary)).encode("utf_8")

  #print data
  request = urllib2.Request(url)
  request.add_data(postData)
  response = urllib2.urlopen(request)
  return response.read()

  

def get_content_type(filename):
  return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

def upload(filename, FID=0):
  url = 'http://upload.box.net/api/1.0/upload/%s/%s' % ('8kf9roqysu8jmqskys9vg0hovkmyqtv3', FID)

  # construct POST data
  boundary = mimetools.choose_boundary()
  body = ""

  # filename
  body += "--%s\r\n" % (boundary)
  body += 'Content-Disposition: form-data; name="share"\r\n\r\n'
  body += "%s\r\n" % ('1')

  body += "--%s\r\n" % (boundary)
  body += "Content-Disposition: form-data; name=\"file\";"
  body += " filename=\"%s\"\r\n" % filename
  body += "Content-Type: %s\r\n\r\n" % get_content_type(filename)

  #print body
  print body
  fp = file(filename, "rb")
  data = fp.read()
  fp.close()

  postData = body.encode("utf_8") + data + ("\r\n--%s--" % (boundary)).encode("utf_8")

  request = urllib2.Request(url)
  request.add_data(postData)
  request.add_header("Content-Type", "multipart/form-data; boundary=%s" % boundary)
  response = urllib2.urlopen(request)
  return response.read()

def getBox(action, inparams):
# action is the action, inparams is a dictionary where
# format would amount to &key=value for input params
# and each value is a list, even if it is a one item list
  url = '/api/1.0/rest?action=%s&api_key=%s&auth_token=%s' % (action, box_api_key, box_auth)
  for param in inparams.keys():
    if len(inparams[param]) == 1:
      url = '%s&%s=%s' % (url, param, inparams[param][0])
    else:
      for value in inparams[param]:
        url = '%s&%s=%s' % (url, '%s[]' % (param), value)
  conn.request('GET', url)
  return conn.getresponse().read()

def getText(element, name):
#element is '<name>text, etc</name>', name is the name therein
  return (element.partition('<'+name+'>')[2]).partition('</'+name+'>')[0]

def getAttribute(element, name):
#element is '<whatever name="text" att2="" .....', name is the name therein
#fails if the value of the attribute contains an escaped double-quote (")
  return (element.partition(' %s="' % name)[2]).partition('"')[0]

def chkHTTPstatus(xmlResponse, desired):
# checks if status string in xmlResponse is as "desired",
# if not raises an error naming the appropriate error
# returns response. if no parsing of xml in calling function
#   is required, chkHTTPstatus can be called without caring about this
#   If, however, in the calling function you will parse the xml, it is
#   useful and saves resources to avoid parsing it again
  xmldoc = minidom.parseString(xmlResponse)
  response = xmldoc.firstChild
  status = getText(response.getElementsByTagName("status")[0].toxml(),'status')
  if (status != desired):
    raise Exception('chkHTTPstatus Exception. Wanted "%s", received "%s"' % (desired, status))
  return response

def createProfFolder(id):
# creates a folder in the top level with name "name"
# returns the id of that folder
  response = getBox('create_folder',{'parent_id': [0], 'name': [prefix+id], 'share': [0]})
  rep = chkHTTPstatus(response, 'create_ok')
  return int(getText(rep.getElementsByTagName("folder")[0].getElementsByTagName("folder_id")[0].toxml(), 'folder_id'))

def createSubFolder(FID, name):
# creates a Folder inside FID with name "name"
# returns folder id
  response = getBox('create_folder',{'parent_id': [FID], 'name': [name], 'share': [0]})
  rep = chkHTTPstatus(response, 'create_ok')
  return int(getText(rep.getElementsByTagName("folder")[0].getElementsByTagName("folder_id")[0].toxml(), 'folder_id'))

def listFoldersIn(FID):
# returns a dictionary of Folder Names in the folder with
# id = FID, as key with id as value
  response = getBox('get_account_tree',{'folder_id': [FID], 'params': ['onelevel', 'nozip','simple']})
  rep = chkHTTPstatus(response, 'listing_ok')
  folderDict = {}
  
  if (rep.toxml().find('<folders>') >= 0):
    folders = rep.getElementsByTagName("tree")[0].firstChild.getElementsByTagName("folders")
    for folder in folders:
      nextseg = (folder.toxml().partition('</folders>')[0]).partition('<folders><fold')[2]
      while (nextseg != ""):
        segs = nextseg.partition('<fold')
        folderseg = segs[0]
        nextseg = segs[2]
        fid = getAttribute(folderseg, 'id')
        name = getAttribute(folderseg, 'name')
        folderDict[name] = fid
  return folderDict

def createSubFolder(FID, name):
# creates a Folder inside FID with name "name"
# returns folder id
  response = getBox('create_folder',{'parent_id': [FID], 'name': [name], 'share': [0]})
  rep = chkHTTPstatus(response, 'create_ok')
  return int(getText(rep.getElementsByTagName("folder")[0].getElementsByTagName("folder_id")[0].toxml(), 'folder_id'))

def listProfFolders():
# returns a dictionary of Professor Folder Names as key with id as value
  return listFoldersIn('0')

def listFilesIn(FID,ftype='all'):
# lists files in folder with id FID. values for ftype:
# format is a dict, with keys file_names and values ids
#    'all' - list all files
#    future implementation - list student files assoc with a specific
#    prof file --- not implemented yet
#      'prof' - professor uploaded files
#      'student' - student uploaded files
  response = getBox('get_account_tree',{'folder_id': [FID], 'params': ['onelevel', 'nozip','simple']})
  rep = chkHTTPstatus(response, 'listing_ok')
  if (ftype != 'all'):
    raise Exception('listFilesIn Exception - functionality not yet implemented. please try with parameter "all"')
  fileDict = {}
  # if (rep.toxml().find('<file>') >= 0):
  try:
    newrep = rep.getElementsByTagName('tree')[0].getElementsByTagName('folder')[0].getElementsByTagName('files')[0].getElementsByTagName('file')
  except:
    return fileDict
  for doc in newrep:
    name = getAttribute(doc.toxml(), 'file_name')
    fid = getAttribute(doc.toxml(), 'id')
    fileDict[name] = fid
  return fileDict

def chkStuTime(fID, method):
# date range per folder
# method is FID or list of IDs
  # wait
  return 0

def getFileInfo(ID):
# returns a dictionary containing information on the
# name, id, created, updated, and size of a file
  response = getBox('get_file_info',{'file_id': [ID]})
  rep = chkHTTPstatus(response, 's_get_file_info')
  info = rep.getElementsByTagName('info')[0]
  fileDict = {}
  print '%s\n' % (info.toxml())
  for att in ['file_name', 'file_id', 'created', 'updated', 'size']:
    fileDict[att] = getText(info.getElementsByTagName(att)[0].toxml(), att)
  return fileDict

def downloadFileURL(ID):
# returns a link to download a file specified by ID
  return 'https://www.box.net/api/1.0/download/%s/%s' % (box_auth, ID)

def downloadFilesIn(FID):
# downloads all files in folder with id FID
# returns the files or something
  return 0

def uploadNewDocP(FID, name):
# uploads a document with name "name" in folder with id FID 
# tags as created by Professor
  #check new
  return 0

def uploadNewDocS(FID, name, student):
# uploads a document with name "name" in folder with id FID
# tags as created by Student with name Student
  #check new
  return 0

def uploadNewDocPbyN(prof, name):
# uploads a document with name "name" in professor folder called prof
# tags as created by Professor
  #check new
  # wait
  return 0

def uploadNewDocS(prof, name, student):
# uploads a document with name "name" in professor folder called prof
# tags as created by Student with name Student
  #check new
  # wait
  return 0


def uploadEditedDoc(ID):
# overwrites a document with id ID
  return 0

def uploadEditedDocP(prof, name):
# overwrites a document with name "name" in professors folder "prof"
  # wait
  return 0

def renameDoc(ID, name):
# changes a document with id ID to name "name"
  return 0


#print getBox('get_account_tree',{'folder_id': [23610430], 'params': ['onelevel', 'nozip']})

#####################################

#check if can download file, if cant then can upload to it
#prevent overwriting on a createFile, have an OverwriteFile


# Authorization
# xmldoc = minidom.parse('ticket.xml')
# response = xmldoc.firstChild

# def getText(element, name):
#element is '<name>text, etc</name>', name is the name therein
#     return (element.partition('<'+name+'>')[2]).partition('</'+name+'>')[0]


# print getText(response.getElementsByTagName("status")[0].toxml(),'status')
# print getText(response.getElementsByTagName("ticket")[0].toxml(),'ticket')
