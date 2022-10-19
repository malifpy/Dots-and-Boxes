import time
timeout = time.time() + 5   # 5 minutes from now
while True:
    test = 0
    if test == 5 or time.time() > timeout:
        print("pantek")
        break
    test = test - 1