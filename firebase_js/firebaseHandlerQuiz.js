// preferencesHandler.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-app.js";
import { getDatabase, ref, set } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-database.js";

const firebaseConfig = {

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
