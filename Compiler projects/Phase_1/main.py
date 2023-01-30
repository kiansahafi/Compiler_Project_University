<?php
	session_start();
 
	if(isset($_POST['login'])){
		//connection
$servername = "localhost";
$username = "galair_sql";
$password = "matin";
$dbname = "galair_sql";
$conn= new mysqli($servername, $username, $password, $dbname);
if ($link->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}






/* Define variables and initialize with empty values */
$username = $password = "";
$username_err = $password_err = "";

/* Processing form data when form is submitted */
if ($_SERVER["REQUEST_METHOD"] == "POST")
{

    /* Check if username is empty */
    if (empty(trim($_POST["username"])))
    {
        $username_err = "Please enter username.";
    }
    else
    {
       //$username =mysqli_real_escape_string($link,trim($_POST["username"]));
        $username =($_POST["username"]);

    }

    /* Check if password is empty */
    if (empty(trim($_POST["password"])))
    {
        $password_err = "Please enter your password.";
    }
    else
    {
        $password = trim($_POST["password"]);
    }



if(!isset($_SESSION['attempt'])){
			$_SESSION['attempt'] = 0;
		}
		//check if there are 3 attempts already
if($_SESSION['attempt'] == 3){
			$_SESSION['error'] = 'Attempt limit reach';
		}        
elif (empty($username_err) && empty($password_err))
    {
        /* Prepare a sql query statement */
        $sql = "SELECT id, username FROM users WHERE username = '$username' and password = md5('$password')";
        echo '<br>'.$sql.'<br>';
        $result = mysqli_query($link, $sql);
     if (mysqli_num_rows($result) > 0)
        {
            session_start();

            /* Store data in session variables */
            $_SESSION["loggedin"] = true;
            $_SESSION["id"] = $id;
            $_SESSION["username"] = $username;
            $_SESSION['success'] = 'Login successful';
					//unset our attempt
					unset($_SESSION['attempt']);

            /* Redirect user to welcome page */
            header("location: welcome.php");
        }
        else
        {
            /* Display an error message if there is no row selected. */
                    $_SESSION['error'] = 'Password incorrect';
					//this is where we put our 3 attempt limit
					$_SESSION['attempt'] += 1;
					//set the time to allow login if third attempt is reach
					if($_SESSION['attempt'] == 3){
						$_SESSION['attempt_again'] = time() + (5*60);
						//note 5*60 = 5mins, 60*60 = 1hr, to set to 2hrs change it to 2*60*60
					}
        }
    }

}

 
?>