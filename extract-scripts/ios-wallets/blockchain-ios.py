# Copyright (c) 2022-* Emre Korkmaz. (https://linkedin.com/in/in-).
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import json
import sqlite3
import os
import NSKeyedUnArchiver
def htpl(thedata):
    my_dict=NSKeyedUnArchiver.unserializeNSKeyedArchiver(thedata)
    return(my_dict)
def htpath(path):
    my_dict=NSKeyedUnArchiver.unserializeNSKeyedArchiver(path)
    return(my_dict)
def gpth(path,file):
    fullpath=(path+file[:2]+'/'+file)
    return(fullpath)
def exists(path):
    result=(os.path.exists(path) & os.path.isfile(path))
    return(result)
path="itunesbackupdir"
connection=sqlite3.connect(path+"Manifest.db")
cur=connection.cursor()
query=cur.execute("SELECT fileID,file FROM main.Files WHERE domain LIKE '%Blockchain%';")
results=query.fetchall()
for result in results:
    fileID=result[0]
    file=result[1]
    filepath=gpth(path,fileID)
    print(filepath)
    try:
        if exists(filepath) :
            print(htpath(filepath))
    except:
        continue
