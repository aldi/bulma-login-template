// firebaseHandler.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-app.js";
import { getDatabase, ref, push, set, query, orderByChild, equalTo, get } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-database.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-auth.js";

const firebaseConfig = {
    //replace here with api info
    apiKey: "AIzaSyCN-En8Aggb8gRm9OcNnkn9BpoqImHsiOs",
    authDomain: "gpt-tutor-85689.firebaseapp.com",
    projectId: "gpt-tutor-85689",
    storageBucket: "gpt-tutor-85689.appspot.com",
    messagingSenderId: "749346035662",
    appId: "1:749346035662:web:e4fcae5979840da3503d9f",
    measurementId: "G-YXQQHJEHT8"

  };

const app = initializeApp(firebaseConfig);
const database = getDatabase(app);
const auth = getAuth(app)

function signUpUser(email, password) {
  const usersRef = ref(database, 'Users');
  const emailQuery = query(usersRef, orderByChild('email'), equalTo(email));

  return get(emailQuery).then((snapshot) => {
      if (snapshot.exists()) {
          throw new Error('An account with this email already exists.');
      } else {
          // Create a new user reference with a unique key
          const newUserRef = push(usersRef);
          const passwordHash = CryptoJS.SHA256(password).toString();

          // Set the user data at the new reference
          return set(newUserRef, {
              email: email,
              password: passwordHash
          }).then(() => {
              // Store the userId in localStorage for later use
              localStorage.setItem('userId', newUserRef.key);
              console.log("We are about to swtich to quiz one and userID has been saved")
              window.location.href = 'quiz_one.html'
              return newUserRef.key; // Return the new userId
          });
      }
  });
}

export { signUpUser };
