"""
Usage "$  py/python tv-time.py < tv-shows.txt"
Script reads the file from the standard input, strips trailing and leading whitespaces from individual lines, appends results to new list.
Function GetTvShowTotalLength using the C# application binary which path is passed via environment variable GET_TVSHOW_TOTAL_LENGTH_BIN
tries to retrieve info about the show, if succeeds resturns {title: totalLength(in minutes)} otherwise error is printed to standard error output.

On start, calls to GetTvShowTotalLength in parallel, filters None values and adds everyhing to new dictonary, finds longest and shortest show, prints result
"""

import os
import subprocess
import sys
from multiprocessing import Pool

try:
    BINARY = os.environ.get('GET_TVSHOW_TOTAL_LENGTH_BIN').replace('\"', '')
except:
    print("GET_TVSHOW_TOTAL_LENGTH_BIN not set up")
    sys.exit()

show_list = []
clean_result = {}

# Process the input file
input = sys.stdin.readlines()
for line in input:
    show_list.append(line.strip())

# Returns title of a tv-show and total runtime in minutes
def GetTvShowTotalLength(title):
    process = subprocess.Popen([fr'{BINARY}', '\"{q}\"'.format(q=title)], stdout=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    if stdout.isnumeric():
        stdout = int(stdout)
    exit_code = process.wait()
    
    if exit_code != 10:
        return {title: stdout}
    else:
        print('Could not get info for {q}.'.format(q=title), file=sys.stderr)

if __name__ == '__main__':
    # Run in parallel
    with Pool() as pool:
        raw_result = pool.map(GetTvShowTotalLength, [title for title in show_list])
    result = list(filter(lambda item: item is not None, raw_result))
    
    for item in result:
        clean_result.update(item)

    longest = max(clean_result.items(), key=lambda k: k[1])
    shortest = min(clean_result.items(), key=lambda k: k[1])

    print('The shortest show: {t} ({h}h {m}m)'.format(t=shortest[0], h=int(shortest[1])//60, m=int(shortest[1])%60))
    print('The longest show: {t} ({h}h {m}m)'.format(t=longest[0], h=int(longest[1])//60, m=int(longest[1])%60))