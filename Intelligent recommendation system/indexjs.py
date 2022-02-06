import execjs

def get_js():
    f = open("./qd/index.js", 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr

jsster = get_js()
ctx = execjs.compile(jsster)
print(ctx.call('enString','123456'))