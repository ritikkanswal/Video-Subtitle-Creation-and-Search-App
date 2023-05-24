

function filterVideos() {
    
    var videoSelect = document.getElementById("video-select").value;
    var searchText = document.getElementById("search-text").value;
    var resultTable = document.getElementById("result-table");
    console.log(videoSelect)
    console.log(searchText)
    // Clear existing results
    resultTable.innerHTML = "";
    // let videoData;
    // const videoSelect = 1;
    // const searchText = 'GOOD';

    const apiUrl = `http://127.0.0.1:8000/api/search/?video_id=${videoSelect}&search_text=${searchText}`;

    fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
      // Extract video_id, text, start_time, end_time
      const videoData = data.results.map(result => ({
        video: result.video_id,
        text: result.text,
        startTime: result.start_time,
        endTime: result.end_time
      }));

      // Use the extracted data
      // console.log(videoData);
      // Generate HTML for the filtered results
      videoData.forEach(function(video) {
        var row = document.createElement("tr");
        var startTimeCell = document.createElement("td");
        var endTimeCell = document.createElement("td");
        var textCell = document.createElement("td");
        
        startTimeCell.textContent = video.startTime;
        endTimeCell.textContent = video.endTime;
        textCell.textContent = video.text;
    
        row.appendChild(startTimeCell);
        row.appendChild(endTimeCell);
        row.appendChild(textCell);
        resultTable.appendChild(row);
    
        });
    })
    .catch(error => {
      // Handle any errors
      console.error('Error:', error);
    });
    
}



// Fetch the API to retrieve videos
fetch('http://127.0.0.1:8000/accounts/?format=json')
  .then(response => response.json())
  .then(data => {
    // console.log(data)
    // Iterate over the videos and create options
    const videoSelect = document.getElementById('video-select');
    data.forEach(video => {
      const option = document.createElement('option');
      option.value = video.id;
      option.textContent = video.id+'. '+video.title;
    //   console.log(video.id)
      videoSelect.appendChild(option);
    });
  })
  .catch(error => console.log(error));


