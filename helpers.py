import time
import sys
import psycopg2
import json

def progressbar(it, prefix="", size=60, out=sys.stdout): 
    '''S/O progress bar. thank you! 
    No external packages. A ready-made piece of code.
    You can customize bar progress symbol "#", bar size, text prefix etc.

    Python 3.3+
    import sys
    def progressbar(it, prefix="", size=60, out=sys.stdout): # Python3.3+
        count = len(it)
        def show(j):
            x = int(size*j/count)
            print("{}[{}{}] {}/{}".format(prefix, "#"*x, "."*(size-x), j, count), 
                    end='\r', file=out, flush=True)
        show(0)
        for i, item in enumerate(it):
            yield item
            show(i+1)
        print("\n", flush=True, file=out)
    Usage:
    import time    
    for i in progressbar(range(15), "Computing: ", 40):
        time.sleep(0.1) # any code you need
    '''
    count = len(it)
    def show(j):
        x = int(size*j/count)
        print(f"{prefix}[{u'█'*x}{('.'*(size-x))}] {j}/{count}", end='\r', file=out, flush=True)
    #show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)

