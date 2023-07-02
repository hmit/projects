# rename -n s/2021-\([0-9]{2}\).*\.pdf/2021-\\1.pdf/ *
for fn in `ls eStatement${ACCT4}IN_$1-*`;
do 
  echo $fn; 
  qpdf --password=$PDFPASS --decrypt "./$fn" "./open$fn"; 
done

