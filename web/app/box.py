from xml.dom import minidom
import httplib

# Initialize and Make Connection
box_api_key = 'e74usd65esyarrz614h75i93ik10kku4'
box_ticket = 'n9bczfm5xfg1lpi3m0hv3825zk1o0vdh'
box_auth = '8kf9roqysu8jmqskys9vg0hovkmyqtv3'

conn = httplib.HTTPConnection("www.box.net")

## Functions
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

def createProfFolder(name):
# creates a folder in the top level with name "name"
# returns the id of that folder
  response = getBox('create_folder',{'parent_id': [0], 'name': [name], 'share': [0]})
  rep = chkHTTPstatus(response, 'create_ok')
  return int(getText(rep.getElementsByTagName("folder")[0].getElementsByTagName("folder_id")[0].toxml(), 'folder_id'))

def listProfFolders():
# returns a dictionary of Professor Folder Names as key with id as value
  response = getBox('get_account_tree',{'folder_id': [0], 'params': ['onelevel', 'nozip','simple']})
  rep = chkHTTPstatus(response, 'listing_ok')
  folderDict = {}
  for folder in rep.getElementsByTagName("tree")[0].firstChild.getElementsByTagName("folders"):
    # need to check if a file? [*]
    fid = getAttribute(folder, 'id')
    name = getAttribute(folder, 'name')
    folderDict[name] = fid
  return folderDict

listProfFolders()
#print getAttribute('<folder id="4387" name="Incoming" shared="0"><tags><tag id="34" /></tags><files></files></folder>', 'name')

def createSubFolder(FID, name):
# creates a Folder inside FID with name "name"
# returns folder id
  response = getBox('create_folder',{'parent_id': [FID], 'name': [name], 'share': [0]})
  rep = chkHTTPstatus(response, 'create_ok')
  return int(getText(rep.getElementsByTagName("folder")[0].getElementsByTagName("folder_id")[0].toxml(), 'folder_id'))

def listFoldersIn(FID):
# returns a dictionary of Folder Names in the folder with
# id = FID, as key with id as value
  return 0

def listFilesIn(FID,ftype):
# lists files in folder with id FID. values for ftype:
#    'all' - list all files
#    'prof' - professor uploaded files
#    'student' - student uploaded files
#    future implementation - list student files assoc with a specific
#    prof file --- not implemented yet
  return 0

def chkStuTime(fID, method):
# date range per folder
# method is FID or list of IDs
  # wait
  return 0

def getFileInfo(ID):
# returns a dictionary containing information on the
# name, id, created, updated, and size of a file
  return 0

def downloadFile(ID):
# downloads a file specified by ID
# returns the file or something
  return 0

def downloadFilesIn(FID):
# downloads all files in folder with id FID
# returns the files or something
  return 0

def uploadNewDoc(FID, name):
# uploads a document with name "name", in folder with id FID
# returns id of that document
  #check new
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
