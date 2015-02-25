#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import sys
import os
import subprocess
import datetime, time

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/<search>" ,methods=['GET' , 'POST'])
def network(search):

    date_list_from = request.form['datelist_from']
    if date_list_from.rfind('-') - date_list_from.find('-') < 3:
        date_list_from = date_list_from[:date_list_from.find('-') + 1] + '0' + date_list_from[date_list_from.find('-') + 1:]
    if len(date_list_from) - date_list_from.rfind('-') < 3:
        date_list_from = date_list_from[:date_list_from.rfind('-') + 1] + '0' + date_list_from[date_list_from.rfind('-') + 1:]

        #date_list_from= date_list_from.replace('-', ',')

    date_list_to = request.form['datelist_to']
    if date_list_to.rfind('-') - date_list_to.find('-') < 3:
        date_list_to = date_list_to[:date_list_to.find('-') + 1] + '0' + date_list_to[date_list_to.find('-') + 1:]
    if len(date_list_to) - date_list_to.rfind('-') < 3:
        date_list_to= date_list_to[:date_list_to.rfind('-') + 1] + '0' + date_list_to[date_list_to.rfind('-') + 1:]

    date_dis = datetime.datetime(*map(int, date_list_to.split('-'))) - datetime.datetime(*map(int, date_list_from.split('-')))
    message = list()
    test = list()
    page = ''
    total_price=0

    mode=''
    code_input=request.form['codeinput']
    the_list=request.form['thelist']
    #date_list_from= date_list_from.replace('-', '')

    if the_list == "股價統計":
        mode='price'
        #date_list_from= date_list_from.replace('-', '')
        total_cnt=0
        for i in range(date_dis.days+1):
          date = datetime.date(*map(int, date_list_from.split('-'))) + datetime.timedelta(days=i)
          m = ''.join(map(lambda s: s if len(s) > 1 else '0' + s, map(str, date.timetuple()[:2])))
          proc = subprocess.Popen(['./mini','-p', 'price/' + code_input + '/' + m + '_' + code_input + '.csv', date.isoformat().replace('-', '/')], stdout=subprocess.PIPE)

          (out, err) = proc.communicate()

          if len(out.split("\t"))>=5:
            total_price+=float(out.split("\t")[6])
            total_cnt+=1

          message.append(out.split("\t"))
#         message = [[l.split('\t') for l in b.split('\n')] for b in out]
#         message = [l.split('\t') for l in out.split('\n')]
          #total_price=round(total_price/total_cnt,2)
    else :
        mode='3p'
        for i in range(date_dis.days):
            date = datetime.date(*map(int, date_list_from.split('-'))) + datetime.timedelta(days=i)
            if the_list == "投信買賣超統計":
                proc = subprocess.Popen(['./mini','-toshin','toshin/' + date.isoformat().replace('-', '') + '.csv', code_input], stdout=subprocess.PIPE)
            elif the_list == "外資買賣超統計":
                proc = subprocess.Popen(['./mini','-waitsu','waitsu/' + date.isoformat().replace('-', '') + '.csv', code_input], stdout=subprocess.PIPE)
            elif the_list == "自營商買賣超統計":
                proc = subprocess.Popen(['./mini','-tsuyinshan', 'tsuyinshan/' + date.isoformat().replace('-', '') + '.csv', code_input], stdout=subprocess.PIPE)
            (out, err) = proc.communicate()
            message.append([date.isoformat()] + out.split("\t"))

            if len(out.split("\t"))>1:
                test.append([time.mktime(date.timetuple())*1000] + [out.split("\t")[4]] )
            else:
                test.append([time.mktime(date.timetuple())*1000] + ['0'] )

    templateData = {
#        'price_avg' : total_price,
        'message' : message,
        'mode' : mode,
        'test' : test
    }
    return render_template('result.htm',**templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
