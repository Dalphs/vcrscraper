<?php
include ("Dao.php");


$dao = new Dao();

print_r($dao->getCount());
echo  "<br>";
print_r($dao->findByQuery("nfh"));
$dao->closeConn();
?>