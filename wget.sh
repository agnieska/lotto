# DOWNLOAD="wget --no-check-certificate"
DOWNLOAD="curl --insecure"
REP="../HTML"
mkdir $REP
for i in {1957..2019}
do
  $DOWNLOAD "http://megalotto.pl/wyniki/lotto/losowania-z-roku-$i" > "$REP/$i-wyniki.html"
done