# goal: append last column of file2.txt onto file1.txt
# goal: then append last column of file3.txt onto file1.txt
# write it all to output.txt

# awk '{getline f1 <"file1.txt" ; print f1,$3}' < file2.txt > temp.txt
# awk '{getline tl <"temp.txt" ; print tl,$3}' < file3.txt > output.txt

awk '{ print $3 }' file2.txt > file2_lastcol.txt
awk '{ print $3 }' file3.txt > file3_lastcol.txt
paste -d' ' file1.txt file2_lastcol.txt > temp.txt
paste -d' ' temp.txt file3_lastcol.txt > output.txt
rm file2_lastcol.txt
rm file3_lastcol.txt
rm temp.txt
