from tqdm import tqdm
import os
import sys
import json

def walkdir(folder):
    """Walk through each files in a directory"""
    for dirpath, dirs, files in os.walk(folder):
        for filename in files:
            yield os.path.abspath(os.path.join(dirpath, filename))

if __name__ == '__main__':
    f_name = 'RC_2015-01'
    f = open(f_name, 'r')
    out = open('out.json', 'w+')

    pure_out = open('pure_out.json', 'w+')
    s = {}
    line_count = 0
    sizecounter = 0
    sizecounter += os.stat(f_name).st_size

    try:
        with tqdm(total=sizecounter,
                unit='B', unit_scale=True, unit_divisor=1024) as pbar:
            with open(f_name, 'rb') as fh:
                for line in fh:
                    comment = json.loads(line)
                    comment_as_dict = dict(comment)

                    # body = comment_as_dict['body']
                    subreddit = comment_as_dict['subreddit']
                    # ups = comment_as_dict['ups']
                    # downs = comment_as_dict['downs']
                    # gilded = comment_as_dict['gilded']


                    # d = {}
                    # d['body'] = body
                    # d['subreddit'] = subreddit
                    # d['ups'] = ups
                    # d['down'] = downs
                    # d['gilded'] = gilded

                    if not subreddit in s.keys():
                        s[subreddit] = 1
                    else:
                        s[subreddit] += 1

                    # json.dump(d, pure_out, indent=4, separators=(',', ': '))
                    line_count += 1

                    if line_count == 1e6:
                        break

                    if line:
                        pbar.set_postfix(file=f_name[-10:], refresh=False)
                        pbar.update(sys.getsizeof(line))
    except:
        pass

    f.close()
    sorted_by_value = sorted(s.items(), key=lambda kv: kv[1])
    print(sorted_by_value)
    print(len(s))