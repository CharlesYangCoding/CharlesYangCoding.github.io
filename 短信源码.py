from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

a = input("请输入你需要循环输出的内容：")
b = eval(input('请输入你想循环输出的次数：'))
print("数据已接收！请将光标移动到会话框")
time.sleep(2)

for i in range(3):
  print(r'距离程序运行还有%d秒！'%(3-i))
  time.sleep(1)


for i in range(b): #设置发送次数
    keyboard.type(a)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(0.1)

print('消息发送完成！请关闭窗口')

