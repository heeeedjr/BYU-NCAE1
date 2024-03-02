touch /home/blueteam/report.txt

echo "#" > /home/blueteam/report.txt
echo "# Contents of /etc/passwd" >> /home/blueteam/report.txt
echo "#" >> /home/blueteam/report.txt
echo "" >> /home/blueteam/report.txt
cat /etc/passwd >> /home/blueteam/report.txt
echo "" >> /home/blueteam/report.txt

echo "#" >> /home/blueteam/report.txt
echo "# Result of netstat -tuln" >> /home/blueteam/report.txt
echo "#" >> /home/blueteam/report.txt
echo "" >> /home/blueteam/report.txt
netstat -tuln >> /home/blueteam/report.txt
echo "" >> /home/blueteam/report.txt

echo "#" >> /home/blueteam/report.txt
echo "# Result of ps aux" >> /home/blueteam/report.txt
echo "#" >> /home/blueteam/report.txt
echo "" >> /home/blueteam/report.txt
ps aux >> /home/blueteam/report.txt
echo "" >> /home/blueteam/report.txt

echo "#" >> /home/blueteam/report.txt
echo "# Result of /etc/apt/sources.list" >> /home/blueteam/report.txt
echo "#" >> /home/blueteam/report.txt
echo "" >> /home/blueteam/report.txt
cat /etc/apt/sources.list >> /home/blueteam/report.txt
echo "" >> /home/blueteam/report.txt

echo "#" >> /home/blueteam/report.txt
echo "# Result of /etc/sudoers" >> /home/blueteam/report.txt
echo "#" >> /home/blueteam/report.txt
echo "" >> /home/blueteam/report.txt
cat /etc/sudoers >> /home/blueteam/report.txt
echo "" >> /home/blueteam/report.txt