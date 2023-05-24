
fetch('http://127.0.0.1:8000/accounts/?format=json')
.then(response => response.json())
.then(data => {
  const videoTable = document.getElementById('video-table');
  const tbody = videoTable.querySelector('tbody');
  
  data.forEach(video => {
    const row = document.createElement('tr');
    
    const idCell = document.createElement('td');
    idCell.textContent = video.id;
    row.appendChild(idCell);
    
    const titleCell = document.createElement('td');
    titleCell.textContent = video.title;
    row.appendChild(titleCell);
    
    const createdAtCell = document.createElement('td');
    createdAtCell.textContent = video.created_at;
    row.appendChild(createdAtCell);
    
    const upload_statusCell = document.createElement('td');
    upload_statusCell .textContent = video.upload_status;
    row.appendChild(upload_statusCell);

    const linkCell = document.createElement('td');
    const linkElement = document.createElement('a');
    linkElement.href = video.link;
    linkElement.textContent = 'Click Here'; // Displayed text for the link
    linkCell.appendChild(linkElement);
    row.appendChild(linkCell);

    tbody.appendChild(row);
  });
})
.catch(error => {
  console.error('Error:', error);
});