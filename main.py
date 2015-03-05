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
    price = list()
    fucker = list()
    bonus = list()

    code_input=request.form['codeinput']
    the_list=request.form['thelist']
    for i in range(date_dis.days+1):

        date = datetime.date(*map(int, date_list_from.split('-'))) + datetime.timedelta(days=i)
        m = ''.join(map(lambda s: s if len(s) > 1 else '0' + s, map(str, date.timetuple()[:2])))
        proc = subprocess.Popen(['./mini','-p', 'price/' + code_input + '/' + m + '_' + code_input + '.csv', date.isoformat().replace('-', '/')], stdout=subprocess.PIPE)
        (out_price, err) = proc.communicate()

        if len(out_price.split("\t"))>1:
            price.append([time.mktime(date.timetuple())*1000] + [out_price.split("\t")[6]] )


        if the_list == "投信買賣超統計":
            proc = subprocess.Popen(['./mini','-toshin','toshin/' + date.isoformat().replace('-', '') + '.csv', code_input], stdout=subprocess.PIPE)
        elif the_list == "外資買賣超統計":
            proc = subprocess.Popen(['./mini','-waitsu','waitsu/' + date.isoformat().replace('-', '') + '.csv', code_input], stdout=subprocess.PIPE)
        elif the_list == "自營商買賣超統計":
            proc = subprocess.Popen(['./mini','-tsuyinshan', 'tsuyinshan/' + date.isoformat().replace('-', '') + '.csv', code_input], stdout=subprocess.PIPE)
        (out, err) = proc.communicate()
        message.append([date.isoformat()] + out.split("\t"))

        if len(out.split("\t"))>1:
            fucker.append([time.mktime(date.timetuple())*1000] + [out.split("\t")[4]] )

    cmd = './mini -bonus bonus/%s.csv > bonus.temp' % (code_input)
    os.system(cmd)

    sc = open('bonus.temp', 'r')
    for line in sc.readlines():
        bonus.append(line.split("\t"))

    sc.close()

    os.system('rm bonus.temp')

    templateData = {
        'message' : message,
        'fucker' : fucker,
        'price' : price,
        'code'  : code_input,
        'bonus' : bonus
    }
    return render_template('result.htm',**templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
