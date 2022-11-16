"""
Usage "$  py/python tv-time.py < tv-shows.txt"
Reads the file from the standard input, strips trailing and leading whitespaces from individual lines, appends results to new list.
Function GetTvShowTotalLength using the C# application binary which path is passed via environment variable GET_TVSHOW_TOTAL_LENGTH_BIN
tries to retrieve info about the show, if all is good returns {title: totalLength(in minutes)} otherwise error is printed to standard error output.

On start, calls to GetTvShowTotalLength in parallel, filters out None values and adds everyhing to new dictonary, finds longest and shortest show, prints result
"""

import os
import subprocess
import sys
# from multiprocessing import Pool
import threading
import queue

MAX_THREADS = 5

try:
    BINARY = os.environ.get('GET_TVSHOW_TOTAL_LENGTH_BIN').replace('\"', '')
except:
    print("GET_TVSHOW_TOTAL_LENGTH_BIN not set up")
    sys.exit()

show_list = []
result_queue = queue.Queue()
clean_result = {}
semapho = threading.Semaphore(MAX_THREADS)

# Process the input file
input = sys.stdin.readlines()
for line in input:
    show_list.append(line.strip())

# Returns title of a tv-show and total runtime in minutes
def GetTvShowTotalLength(title):
    semapho.acquire()
    process = subprocess.Popen([fr'{BINARY}', '\"{q}\"'.format(q=title)], stdout=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    if stdout.isnumeric():
        stdout = int(stdout)
    exit_code = process.wait()
    
    if exit_code != 10:
        result_queue.put({title: stdout})
        semapho.release()
        # return {title: stdout}
    else:
        print('Could not get info for {q}.'.format(q=title), file=sys.stderr)
        semapho.release()

if __name__ == '__main__':
    threads = []
    for title in show_list:
        t = threading.Thread(target=GetTvShowTotalLength, args=(title,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    result = []
    while not result_queue.empty():
        result.append(result_queue.get())
    
    for item in result:
        print(item)
        clean_result.update(item)

    longest = max(clean_result.items(), key=lambda k: k[1])
    shortest = min(clean_result.items(), key=lambda k: k[1])

    print('The shortest show: {t} ({h}h {m}m)'.format(t=shortest[0], h=int(shortest[1])//60, m=int(shortest[1])%60))
    print('The longest show: {t} ({h}h {m}m)'.format(t=longest[0], h=int(longest[1])//60, m=int(longest[1])%60))
    # Run in parallel
    # with Pool() as pool:
    #     raw_result = pool.map(GetTvShowTotalLength, [title for title in show_list])
    # result = list(filter(lambda item: item is not None, raw_result))
    
    # for item in result:
    #     clean_result.update(item)

    # longest = max(clean_result.items(), key=lambda k: k[1])
    # shortest = min(clean_result.items(), key=lambda k: k[1])

    # print('The shortest show: {t} ({h}h {m}m)'.format(t=shortest[0], h=int(shortest[1])//60, m=int(shortest[1])%60))
    # print('The longest show: {t} ({h}h {m}m)'.format(t=longest[0], h=int(longest[1])//60, m=int(longest[1])%60))