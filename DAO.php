<?php
class Dao{
    
    public $conn;

    // Create connection
    function __construct(){
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbName = "companies";
    $this->conn = new mysqli($servername, $username, $password, $dbName);
    // Check connection
    if ($this->conn->connect_error) {
        die("Connection failed: " . $this->conn->connect_error);
        }
        echo "Connected successfully <br>";    

    }

    function find($board){
        $sql = "SELECT board, moves FROM secondrow WHERE board = '" . $this->boardToString($board) . "'";
        $result = $this->conn->query($sql);
        if ($result->num_rows > 0) {
            return true;
        } else {
            return false;
        }
    }

    function getCount(){
        $sql = "SELECT searchquery, COUNT(*) FROM info GROUP BY searchquery";
        $result = $this->conn->query($sql);
        if ($result->num_rows > 0) {
            $arr = [];
            while($row = $result->fetch_assoc()) {
                $arr[] = [$row["searchquery"], $row["COUNT(*)"]];
            }
            return $arr;
        } else {
            echo "Error counting occurences " . $this->conn->error;
        }
    }

    function findByQuery($searchquery){
        $sql = "SELECT name FROM info WHERE searchquery='" . $searchquery . "'";
        $result = $this->conn->query($sql);
        if ($result->num_rows > 0) {
            $arr = [];
            while($row = $result->fetch_assoc()) {
                $arr[] = $row["name"];
            }
            return $arr;
        } else {
            echo "Error counting occurences " . $this->conn->error;
        }
    }

    function insert($row, $board, $moves){
        $sql = "INSERT INTO " . $row . "(board, moves) VALUES ('" . $this->boardToString($board) . "', '" . $moves . "')";
        if ($this->conn->query($sql  ) === TRUE){
            
        } else {
            echo "Error inserting record: " . $this->conn->error;
        }
    }

    function delete($row, $board, $moves){
        $sql = "INSERT INTO " . $row . "(board, moves) VALUES ('" . $this->boardToString($board) . "', '" . $moves . "')";
        if ($this->conn->query($sql  ) === TRUE){
            
        } else {
            echo "Error inserting record: " . $this->conn->error;
        }
    }
    function closeConn(){
        $this->conn->close();
    }
}
?>