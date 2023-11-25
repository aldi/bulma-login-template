// firebaseHandler.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-app.js";
import { getDatabase, ref, push, set, query, orderByChild, equalTo, get } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-database.js";
import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-auth.js"; // Import for Firebase Authentication


// var learningPreferences = localStorage.getItem('learningPreferences');


const firebaseConfig = {
    //replace here with api info
  };

const app = initializeApp(firebaseConfig);
const database = getDatabase(app);
const auth = getAuth(app); // Initialize Firebase Authentication

// Function to get current user ID
function getCurrentUserId() {
  return new Promise((resolve, reject) => {
      onAuthStateChanged(auth, (user) => {
          if (user) {
              // User is signed in, return the User ID.
              resolve(user.uid);
          } else {
              // No user is signed in.
              reject('No user logged in');
          }
      });
  });
}
document.getElementById('signupForm').addEventListener('submit', function(e) {
    e.preventDefault();
  
    var email = document.querySelector('[name="username"]').value;
    var password = document.querySelector('[name="password"]').value;
  
    // Check if username and password are not empty
    if (!email || !password) {
      alert('Username and password are required!');
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      alert('Please enter a valid email address.');
      return;
    }
  
    if (!password) {
      alert('Password is required!');
      return;
    }
  
    var passwordHash = CryptoJS.SHA256(password).toString();
  
// Reference to the users in the database
const usersRef = ref(database, 'Users');
  
// Query the database for the submitted email
const emailQuery = query(usersRef, orderByChild('email'), equalTo(email));

get(emailQuery).then((snapshot) => {
  if (snapshot.exists()) {
    alert('An account with this email already exists.');
    return;
  }

  // If no existing user, create a new user reference with a unique key
  const newUserRef = push(usersRef);

  // Set the user data at the new reference
  set(newUserRef, {
    email: email,
    password: passwordHash
  }).then(() => {
    alert('Sign Up Successful!');
    window.location.href = 'quiz_one.html';
  }).catch((error) => {
    console.error('Error saving data: ', error);
    alert('Error during sign up. Please try again.');
  });

}).catch((error) => {
  console.error('Error querying database: ', error);
  alert('Error checking user existence.');
});

});

function saveLearningPreferences(userId, learningPreferences) {
  return new Promise((resolve, reject) => {
      const preferencesRef = ref(database, 'Users/' + userId + '/learningPreferences');
      set(preferencesRef, learningPreferences)
      .then(() => resolve())
      .catch(error => reject(error));
  });
}

function processSurveyResults(userId) {
  var learningPreferences = JSON.parse(localStorage.getItem('learningPreferences'));
  if (learningPreferences) {
      saveLearningPreferences(userId, learningPreferences).then(() => {
          console.log('Learning preferences saved for user:', userId);
          // Additional logic after saving...
      }).catch((error) => {
          console.error('Error saving learning preferences: ', error);
      });
  }
}

export { getCurrentUserId };
export { processSurveyResults };

  
