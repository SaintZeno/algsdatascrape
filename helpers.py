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


def create_table_if_not_exists(pipeline_table, conn_options):
    """
    write json object to postgres database
    :param json_data: json object
    :param table_name: table name
    :return: None
    """
    conn = psycopg2.connect(
        **conn_options
    )
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS " + pipeline_table)
    conn.commit()
    conn.close()



def write_json_to_postgres(json_data, table_name, conn_options):
    """
    write json object to postgres database
    :param json_data: json object
    :param table_name: table name
    :return: None
    """
    conn = psycopg2.connect(
        **conn_options
    )
    cur = conn.cursor()
    #cur.execute("DROP TABLE IF EXISTS " + table_name)
    #cur.execute("CREATE TABLE " + table_name + " (id serial PRIMARY KEY, data json)")
    cur.execute("INSERT INTO " + table_name + " (data) VALUES (%s)", (json.dumps(json_data),))
    conn.commit()
    conn.close()


def read_json_from_postgres(table_name, conn_options):
    """
    read json object from postgres database
    :param table_name: table name
    :return: json object
    """
    conn = psycopg2.connect(
       **conn_options
    )
    cur = conn.cursor()
    cur.execute("SELECT data FROM " + table_name)
    data = cur.fetchone()
    conn.close()
    return json.loads(data[0])