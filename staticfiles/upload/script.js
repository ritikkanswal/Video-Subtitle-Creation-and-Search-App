// const title = document.getElementsByClassName('videoTitle');
// const fileInput = document.querySelector('#videoFile');
// const url = 'http://127.0.0.1:8001/accounts/';

// const formData = new FormData();
// formData.append('title', title);
// formData.append('document', fileInput.files[0]);

// fetch(url, {
//   method: 'POST',
//   body: formData
// })
//   .then(response => response.json())
//   .then(data => {
//     console.log('Response:', data);
//     // Handle the response data as needed
//   })
//   .catch(error => {
//     console.error('Error:', error);
//     // Handle any errors
//   });


const form = document.getElementById('uploadForm');
const videoTitleInput = document.getElementById('videoTitle');
const videoFileInput = document.getElementById('videoFile');

form.addEventListener('submit', (event) => {

// Show alert box
alert('Video Will Upload Soon Check "Videos Uploaded Section"');
event.preventDefault(); // Prevent form submission

const videoTitle = videoTitleInput.value;
const videoFile = videoFileInput.files[0]; // Get the selected file

// Now you can use the extracted values (videoTitle and videoFile) as needed, e.g., send them to the server using AJAX or fetch API.

// Example: Display the extracted values in the console
console.log('Video Title:', videoTitle);
console.log('Video File:', videoFile);
const url = 'http://13.50.129.179:8000/api/upload/';
const formData = new FormData();
formData.append('title', videoTitle);
formData.append('document', videoFile);
fetch(url, {
  method: 'POST',
  body: formData
})
  .then(response => response.json())
  .then(data => {
    console.log('Response:', data);
    // Handle the response data as needed
  })
  .catch(error => {
    console.error('Error:', error);
    // Handle any errors
  });

// Reset the form
form.reset();
});
 
  
  
  
  
  