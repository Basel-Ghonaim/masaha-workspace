import sys
open(sys.argv[1], "w", encoding="utf8", newline="").write(sys.argv[2].replace(chr(92)+"n", chr(10)))
