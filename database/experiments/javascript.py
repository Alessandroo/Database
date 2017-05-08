import execjs


# print(execjs.eval("'red yellow blue'.split(' ')"))
# ctx = execjs.compile("""
#      function add(x, y) {
#          return x + y;
#      }
#  """)
# print(ctx)
# print(ctx.call("add", 1, 2))


if __name__ == '__main__':
    # car0 = execjs.compile("""
    # function get0(array){
    #     return array[0]
    # }
    # """)
    # print(car0.call("get0", [1, 2, 5]))
    ctx = execjs.compile("""
        function f(dict){
            return function add(x, y) {
                let c = 5;
                return x + y + c;
         }(dict.x, dict.y)
        }
     """)
    # ctx = execjs.compile("function f(dict){ return function add(x, y) { let c = 5; return x + y + c;}(dict.x, dict.y)}")
    # print(ctx)
    dic = {
        'x': 1,
        'y': 2
    }
    print(ctx.call("f", dic))
