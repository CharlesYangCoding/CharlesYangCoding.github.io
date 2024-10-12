print("复制代码至此")
s  = input()  
r = compile(s,"<string>", "exec")  
r
exec(r)
