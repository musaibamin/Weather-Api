    function loadDashboard() {
        var applicationsA =[]
        X = fetch('/applications').then(response => response.json())
                .then(applications => {
                    return applications;
                    })
                .catch(error => console.error('Error:', error));
console.log(X);
console.log(X.length);

    }

    loadDashboard();