// firebaseHandler.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-app.js";
import { getDatabase, ref, push, set, query, orderByChild, equalTo, get } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-database.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-auth.js";

const firebaseConfig = {

};

const app = initializeApp(firebaseConfig);
const database = getDatabase(app);
const auth = getAuth(app);

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function signUpUser(email, password) {
    if (!isValidEmail(email)) {
        alert('Invalid email format.');
        return; // Stop the function here
    }

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
                console.log("We are about to switch to quiz one and userID has been saved");
                window.location.href = 'quiz_one.html';
                return newUserRef.key; // Return the new userId
            });
        }
    });
}

export { signUpUser };

// const app = initializeApp(firebaseConfig);
// const database = getDatabase(app);
// const auth = getAuth(app)

// function signUpUser(email, password) {
//   const usersRef = ref(database, 'Users');
//   const emailQuery = query(usersRef, orderByChild('email'), equalTo(email));

//   return get(emailQuery).then((snapshot) => {
//       if (snapshot.exists()) {
//           throw new Error('An account with this email already exists.');
//       } else {
//           // Create a new user reference with a unique key
//           const newUserRef = push(usersRef);
//           const passwordHash = CryptoJS.SHA256(password).toString();

//           // Set the user data at the new reference
//           return set(newUserRef, {
//               email: email,
//               password: passwordHash
//           }).then(() => {
//               // Store the userId in localStorage for later use
//               localStorage.setItem('userId', newUserRef.key);
//               console.log("We are about to swtich to quiz one and userID has been saved")
//               window.location.href = 'quiz_one.html'
//               return newUserRef.key; // Return the new userId
//           });
//       }
//   });
// }

// export { signUpUser };
