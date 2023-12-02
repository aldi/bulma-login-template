// Import the functions you need from the Firebase SDKs
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-auth.js";
import { getDatabase, ref, get, query, orderByChild, equalTo } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-database.js";
// import CryptoJS from 'https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js';
const firebaseConfig = {
    // Replace here with your Firebase API info
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app); // Initialize Firebase Auth
const database = getDatabase(app); // Initialize Firebase Database

// Function to log in user and retrieve preferences
function loginUser(email, password) {
    const usersRef = ref(database, 'Users');
    const emailQuery = query(usersRef, orderByChild('email'), equalTo(email));
  
    return get(emailQuery).then((snapshot) => {
      if (!snapshot.exists()) {
        throw new Error('No account found with the provided email.');
      }
  
      // Check the password hash against the one stored in the database
      const userData = snapshot.val();
      const userId = Object.keys(userData)[0]; // This assumes that emails are unique
      const user = userData[userId];
  
      const passwordHash = CryptoJS.SHA256(password).toString();
      if (passwordHash === user.password) {
        // Password is correct, retrieve the user information
        console.log('User logged in:', user);
        // Store the userId in localStorage or in your app's state
        localStorage.setItem('userId', userId);
        // Here you could redirect to a new page or do something else
        return user;
      } else {
        throw new Error('Incorrect password.');
      }
    }).catch((error) => {
      console.error('Login error:', error);
      alert('Login failed: ' + error.message);
      return Promise.reject(error);
    });
  }
  
  export { loginUser };
  

function fetchLearningPreferences(userId) {
    const userPreferencesRef = ref(database, 'Users/' + userId + '/learningPreferences');
    return get(userPreferencesRef)
        .then((snapshot) => {
            if (snapshot.exists()) {
                return snapshot.val();
            } else {
                console.log("No learning preferences found!");
                return {};
            }
        })
        .catch((error) => {
            console.error("Error fetching learning preferences:", error);
        });
}


// Event listener for login form submission
document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    loginUser(email, password)
        .then(learningPreferences => {
            // Handle learning preferences
            if (learningPreferences) {
                localStorage.setItem('learningPreferences', JSON.stringify(learningPreferences));
                window.location.href = 'chat.html';
            }
        })
        .catch(error => {
            // Handle login errors
            console.error('Login error:', error);
            alert('Login failed: ' + error.message);
        });
});
