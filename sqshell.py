# Shell for playing with SQL
# Based on example at https://docs.python.org/3.4/library/sqlite3.html
# But better at dealing with multi-line statements and printing stuff

import sqlite3
import sys

con = sqlite3.connect(sys.argv[1])
cur = con.cursor()

print("\nLoaded {}\n".format(sys.argv[1]))

buffer = ""

def print_cursor(cur):

	# First determine the lengths of our columns when printing...

	lengths = [0 for desc in cur.description]
	rows = []

	for i, col in enumerate(cur.description):
		lengths[i] = len(col[0])

	for row in cur:
		rows.append(row)
		for i, col in enumerate(row):
			if len(str(col)) > lengths[i]:
				lengths[i] = len(str(col))

	# Fine, now print the columns...

	print()
	for i, col in enumerate(cur.description):
		print("{0:<{1}}".format(col[0], lengths[i]), end="  ")
	print()
	for length in lengths:
		print("-" * length + "  ", end="")
	print()
	for row in rows:
		for i, col in enumerate(row):
			print("{0:<{1}}".format(str(col), lengths[i]), end="  ")
		print()
	print()


while 1:
	inp = input("> ")
	inp = inp.strip()

	if len(inp) == 0:
		continue

	buffer += " " + inp
	if sqlite3.complete_statement(buffer):

		try:
			cur.execute(buffer)
			if buffer.lstrip().upper().startswith("SELECT"):
				print_cursor(cur)
		except sqlite3.Error as e:
			print()
			print("An error occurred:", e.args[0])
			print()

		buffer = ""
