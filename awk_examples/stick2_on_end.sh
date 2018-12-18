awk '{getline f1 <"file1.txt" ; print f1,$2}' < file2.txt > file3.txt
