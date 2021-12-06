import sys
import os
import multiprocessing as mp
import time

def current_milli_time():
    return round(time.time() * 1000)

def filter_and_replace(srcDir, ind, generateAST, size):
	print(f"filter_and_replace for {srcDir},{ind},{generateAST},{size}")
	ASTFilename = 'AST.csv'
	if not generateAST:
		os.system(f'java -jar parser.jar -s {srcDir} -f csv | python3 parser_csv1_csv2_converter.py > AST{ind}.csv')
		ASTFilename = f'AST{ind}.csv'
	newInd = ind + size
	print("Command: " + f"python3 kh_filter.py 'T{ind}T' < {ASTFilename} | xargs -n1 -d '\\n' java -jar kh-replacer/target/replacer-1.0-SNAPSHOT-jar-with-dependencies.jar -n 'T{newInd}T' -of diff.diff -os")
	os.system(f"python3 kh_filter.py 'T{ind}T' < AST.csv | xargs -n1 -d '\\n' java -jar kh-replacer/target/replacer-1.0-SNAPSHOT-jar-with-dependencies.jar -n 'T{newInd}T' -of diff.diff -os")

def main(argv):
	startTime = current_milli_time()
	pool = mp.Pool(int(argv[0]))
	srcDir = argv[1]
	isIReplacer = (argv[2] == 'true')
	size = int(argv[3])

	if isIReplacer:
		os.system(f'java -jar parser.jar -s {srcDir} -f csv | python3 parser_csv1_csv2_converter.py > AST.csv')

	for i in range(size, -1, -1):
		pool.apply_async(filter_and_replace, args = (srcDir, i, isIReplacer, size, ))

	pool.close()
	pool.join()
	print("Time: " + str(current_milli_time() - startTime))

if __name__ == "__main__":
    main(sys.argv[1:])
