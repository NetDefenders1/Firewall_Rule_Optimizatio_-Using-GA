import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, sendPasswordResetEmail } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js";
import { getFirestore, setDoc, doc } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyCTV78WkUngNt_Ykw8z-NOLRAyyBGtEggw",
  authDomain: "login-78855.firebaseapp.com",
  projectId: "login-78855",
  storageBucket: "login-78855.appspot.com",
  messagingSenderId: "1062193064964",
  appId: "1:1062193064964:web:dae0b6780718b853d3d951",
  measurementId: "G-D83TC2X700"
};

const app = initializeApp(firebaseConfig);

function showMessage(message, divId) {
  var messageDiv = document.getElementById(divId);
  messageDiv.style.display = "block";
  messageDiv.innerHTML = message;
  messageDiv.style.opacity = 1;
  setTimeout(function() {
    messageDiv.style.opacity = 0;
  }, 5000);
}

const signUp = document.getElementById('submitSignUp');
signUp.addEventListener('click', (event) => {
  event.preventDefault();
  const email = document.getElementById('rEmail').value;
  const password = document.getElementById('rPassword').value;
  const firstName = document.getElementById('fName').value;
  const lastName = document.getElementById('lName').value;

  const auth = getAuth();
  const db = getFirestore();

  createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      const user = userCredential.user;
      const userData = {
        email: email,
        firstName: firstName,
        lastName: lastName,
        password: password
      };
      showMessage('Account Created Successfully', 'signUpMessage');
      const docRef = doc(db, "users", user.uid);
      setDoc(docRef, userData)
        .then(() => {
          window.location.href = 'home.html';
        })
        .catch((error) => {
          console.error("error writing document", error);
        });
    })
    .catch((error) => {
      const errorCode = error.code;
      if (errorCode == 'auth/email-already-in-use') {
        showMessage('Email Address Already Exists !!!', 'signUpMessage');
      } else {
        showMessage('unable to create User', 'signUpMessage');
      }
    })
});

const signIn = document.getElementById('submitSignIn');
signIn.addEventListener('click', (event) => {
  event.preventDefault();
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const auth = getAuth();

  signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      showMessage('login is successful', 'signInMessage');
      const user = userCredential.user;
      localStorage.setItem('loggedInUserId', user.uid);
      window.location.href = 'home.html';
    })
    .catch((error) => {
      const errorCode = error.code;
      if (errorCode === 'auth/invalid-credential') {
        showMessage('Incorrect Email or Password', 'signInMessage');
      } else {
        showMessage('Account does not Exist', 'signInMessage');
      }
    })
});

const auth = getAuth();
const repass = document.getElementById("repass");
repass.addEventListener("click", function() {
  const email = document.getElementById('email').value;
  if (email) {
    sendPasswordResetEmail(auth, email)
      .then(() => {
        alert("Password reset email sent");
      })
      .catch((error) => {
        alert("Error: " + error.message);
      });
  } else {
    alert("Please enter your email address first");
  }
});
