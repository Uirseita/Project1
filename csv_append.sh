OutFileName="X.csv"                       # Fix the output name
i=0                                       # Reset a counter
# @todo add echo
for filename in ./*.csv; do 
 if [ "$filename"  != "$OutFileName" ] ;      # Avoid recursion 
 then 
   if [[ $i -eq 0 ]] ; then 
      head -1  $filename >   $OutFileName # Copy header if first
   fi
   tail -n +2  $filename >>  $OutFileName # Append from each 2nd line
   i=$(( $i + 1 ))                        # Increase the counter
 fi
done
