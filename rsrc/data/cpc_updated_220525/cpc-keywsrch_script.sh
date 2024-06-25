grep -hEir '\<genes?\>|\<genotypes?\>|\<genetics?\>|\<geneomes?\>|\<cistrons?\>' ./cpc-sec* > cpc-keywsrch-total.txt
grep -hEir '\<(poly)?proteins?\>|\<(poly)?peptides?\>|\<proteome\>|\<(poly)?amino ?acids?\>' ./cpc-sec* >> cpc-keywsrch-total.txt
grep -hEir '\<transcription factors?\>|\<(co)?repressors?\>|\<(co)?activators?\>|\<(co)?inducers?\>|\<(co)?inhibitors?\>|\<(co)?suppressors?\>|\<promoters?\>|\<receptors?\>' ./cpc-sec* >> cpc-keywsrch-total.txt
grep -hEir '\<[a-z]+DNAs?\>|\<[a-z]+RNAs?\>|\<(ribo)?nucle(ic\>|o)' ./cpc-sec* >> cpc-keywsrch-total.txt
grep -hEir '\<antibod(ies|y)\>|\<anti(gen|biotic)s?\>|\<immun(o|e)' ./cpc-sec* >> cpc-keywsrch-total.txt
grep -hEir '\<(co|iso)?enzym(e|atic)s?\>' ./cpc-sec* >> cpc-keywsrch-total.txt
grep -hEir '\<metaboli(c|te|sm)s?\>' ./cpc-sec* >> cpc-keywsrch-total.txt
grep -hEir '\<cell (growth|signal|divi|cycle|prolife|diffe)s?' ./cpc-sec* >> cpc-keywsrch-total.txt
