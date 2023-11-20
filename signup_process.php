<?php
include 'db_connect.php'; // Include your database connection script

// Check if the form data is posted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Retrieve the form data
    $username = isset($_POST['username']) ? trim($_POST['username']) : null;
    $password = isset($_POST['password']) ? trim($_POST['password']) : null;

    // Check if username and password have been provided
    if ($username && $password) {
        // Hash the password
        $passwordHash = password_hash($password, PASSWORD_DEFAULT);

        // SQL to insert data into the users table
        $sql = "INSERT INTO Users (Username, PasswordHash) VALUES (?, ?)";
        $stmt = $conn->prepare($sql);

        // Bind the parameters to the SQL query
        $stmt->bind_param("ss", $username, $passwordHash);

        // Attempt to execute the prepared statement
        if ($stmt->execute()) {
            // After successful insertion, redirect to survey.html
            header("Location: survey.html");
            exit();
        } else {
            // Handle error appropriately
            echo "Error: " . $stmt->error;
        }

        // Close the statement
        $stmt->close();
    } else {
        // Handle validation error appropriately
        echo "Username and password are required.";
    }

    // Close the database connection
    $conn->close();
} else {
    // Handle the error appropriately if the server request method is not POST
    echo "Invalid request method.";
}
?>
