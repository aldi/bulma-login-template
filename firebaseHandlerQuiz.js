// preferencesHandler.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-app.js";
import { getDatabase, ref, set } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-database.js";

const firebaseConfig = {
  // Replace with your Firebase API info
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

function saveLearningPreferences(userId, learningPreferences) {
    const preferencesRef = ref(database, 'Users/' + userId + '/learningPreferences');
    return set(preferencesRef, learningPreferences);
}

const userId = localStorage.getItem('userId'); // Retrieve the userId stored earlier
localStorage.setItem('userId', userId);
export { saveLearningPreferences };