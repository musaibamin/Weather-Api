
        // Function to delete application
        function deleteApplication(applicationId) {
            if (confirm('Are you sure you want to delete this application?')) {
                fetch('/applications/' + applicationId, {
                    method: 'DELETE',
                })
                .then(response => {
                    if (response.ok) {
                        // Reload dashboard after deletion
                        loadDashboard();
                    } else {
                        console.error('Error deleting application');
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        }




    function loadDashboard() {
//       document.getElementById("dashboard").innerHTML= `  <div id="dashboard" style="display:block;">
//            <h1>Dashboard</h1>
//            <div class="row">
//                <div class="col-md-4" style="">
//                    <div class="card height300">
//                        <div class="card-body d-flex justify-content-center align-items-center">
//                            <canvas id="circularGraph"></canvas>
//
//                        </div>
//                    </div>
//                </div>
//
//            <div class="col-md-8" style="">
//                    <div class="card height300">
//                        <div class="card-body d-flex justify-content-center align-items-center">
//
//                            <canvas id="lineGraph"></canvas>
//
//                        </div>
//                    </div>
//                </div>
//            </div>
//            <div class="row">
//                <div class="col-md-12" style="">
//                    <div class="card heightmin150">
//                        <h6 style="padding:10px 10px 10px 10px;"> Active Applications</h6>
//                            <div class="card-body d-flex justify-content-center align-items-center" id="activeApplications">
//
//                        </div>
//                        </div>
//                    </div>
//                </div>
//        </div>  `;
       document.getElementById("dashboard").style.display="block";
       document.getElementById("updateProfile").style.display="none";
       document.getElementById("createApplication").style.display="none";
       fetch('/applications')
                  .then(response => {
                    if (!response.ok) {
                      throw new Error('Network response was not ok');
                    }
                    alert(response)
                    return response.json();
                  })
                  .then(data => {
                    // Handle the JSON data
                    console.log(data);
                    })
              .catch(error => {
                // Handle any errors that occurred during the fetch
                console.error('Fetch error:', error);
              });

//        fetch('/applications')
//                .then(response => response.json())
//                .then(applications => {
//                let html=""
//                    applications.forEach(application => {
//                        html += application.name;
//                    });
//                alert(html);
//                })
//                .catch(error => console.error('Error:', error));
        // Fetch applications from server
       //apps=[ {"id": 1, "name": "Application 1", accesstoken:'acecedew-ddere-fefefefe1'}, {"id": 2, "name": "Application 2",accesstoken:'2acecedew-ddere-fefefefe1'}, {"id": 3, "name": "Application 3",accesstoken:'3acecedew-ddere-fefefefe1'}]
                // Generate dummy data for circular graph (loading bar)
                const circularGraphData = {
                    labels: ['App1','App2','Available/Unused'],
                    datasets: [{
                        data: [30, 50, 100-(30+50)],
                        backgroundColor: [
                            'rgba(155, 0, 83, 0.9)',
                            'rgba(0, 138, 190, 0.9)',
                            'rgba(99, 177, 102, 0.9)'
                        ],
                        borderColor: [
                            'rgba(155, 0, 83, 1)',
                            'rgba(0, 138, 190, 1)',
                            'rgba(99, 177, 102, 1)'
                        ],
                        borderWidth: 1
                    }]
                };


                // Render circular graph (loading bar)
                const circularGraphCtx = document.getElementById('circularGraph').getContext('2d');
                if(circularGraphCtx){
                new Chart(circularGraphCtx, {
                    type: 'doughnut',
                    data: circularGraphData,
                    options: {
                        responsive: true,

                    }
                });
                }

                // Render pie chart


        var colors = ['#007bff','#28a745','#333333','#c3e6cb','#dc3545','#6c757d'];
        // Render line graph
        const lineGraphData = {
            labels: ['Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Saturday'],
            datasets: [{
                label: 'Daily API Requests',
                backgroundColor: 'rgba(255, 99, 132, 0)',
                borderColor: colors[0],
                borderWidth: 3,
                data: [589, 445, 483, 503, 689, 692, 634] // Dummy data
            }]
        };



//         Configure line graph options
        const lineGraphOptions = {
            responsive: true
        };
//
        // Create line graph
        const lineGraphCtx = document.getElementById('lineGraph').getContext('2d');
        if(lineGraphCtx){
        new Chart(lineGraphCtx, {
            type: 'line',
            data: lineGraphData,
            options: lineGraphOptions
        });
        }


       //ADD APPLICATIONS LIST


       let applicationshtml = '<tbody>';
       apps.forEach(application => {applicationshtml += '<tr> <th scope="row">'+application.id +'</th><td>'+application.name+'</td> <td>' + application.accesstoken + ' <button class="badge badge-success" onclick="navigator.clipboard.writeText(\''+application.accesstoken+'\');"> Copy </button></td><td><button class="badge badge-danger" onclick="deleteApplication(' + application.id + ')">Delete</button></td></tr>';});
       applicationshtml += '</tbody>';
       document.getElementById("activeApplications").innerHTML = applicationshtml;
    }


function loadUpdateProfileForm()
{
       document.getElementById("updateProfile").style.display="block";
       document.getElementById("dashboard").style.display="none";
       document.getElementById("createApplication").style.display="none";

}


function loadCreateApplicationForm()
{
       document.getElementById("createApplication").style.display="block";
       document.getElementById("updateProfile").style.display="none";
       document.getElementById("dashboard").style.display="none";


}