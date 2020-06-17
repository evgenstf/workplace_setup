#!/usr/bin/python3.6
import os
import argparse, sys

parser=argparse.ArgumentParser()

parser.add_argument('--branch', help='Branch name', required=True)
parser.add_argument('--ticket', help='Ticket id', required=True)
parser.add_argument('--message', help='Message', required=True)
parser.add_argument('--review', help='Review id')
parser.add_argument('--no-review', help='Disable review', const=True, action='store_const')
parser.add_argument('--to', help='Distination branch', default='master')
parser.add_argument('--no-push', help='Only commit, without push', const=True, action='store_const')

args=parser.parse_args()


message = args.ticket + ': ' + args.message
if (args.no_review != True):
    if (args.review == None):
        print('Specify review id or use --no-review flag')
        exit()
    if (args.review[0] != '#'):
        print('Review id should start from #')
        exit()
    message += ' (' + args.review + ')'

print()
print(message)
print('From: ', args.branch)
print('To: ', args.to)

print()
print('Approve (y):', end='')
approve = input()

if approve == 'y':
    commit_command = 'git checkout ' + args.to + ' && git pull && git merge --squash ' + args.branch + ' && git commit -m "' + message + '"'
    os.system(commit_command)
    if (args.no_push != True):
        os.system('git push')
else:
    print('Merge abandoned')
