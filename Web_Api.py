#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import cgi
import cgitb; cgitb.enable()
import json
import time

start=time.time()
inp_grid =""
out_grid =""
matrix_size = 0
try:
    from FramePython import FramePython
    from inpData     import inpData
    from outData     import outData

    # arg 
    form = cgi.FieldStorage()
    inp_grid = form.getfirst("inp_grid", "")

    # input 
    inp  = inpData()
    if len(inp_grid) == 0:
        inp.rText()
    else:
        inp.setJSON(inp_grid)

    # calcration 
    out = FramePython().Nonlinear3D(inp)

    # output 
    dict_Json = out.getDictionary()

    dtime=time.time()-start
    dict_Json['matrix_size'] = inp.n
    dict_Json['dtime'] = dtime

    out_grid = json.dumps(dict_Json)


    if len(inp_grid) == 0:
        out_text = json.dumps(dict_Json, indent=4)
        fout=open('out_grid.json', 'w')
        print(out_text, file=fout)
        fout.close()
    else:
        print("Content-type: text/javascript; charset=utf-8")
        print()
        print(out_grid)

except:
    print("Content-type: text/javascript; charset=utf-8")
    print()
    for err in sys.exc_info():
        print(err)


