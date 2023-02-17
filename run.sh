source venv/bin/activate
while :
do
    now=$(date +"%T")
    echo "$now - running crawler.py.."
    python crawler.py
    echo "sleeping for 1 hour.."
    sleep 3600
done
