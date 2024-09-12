-- CREATE DATABASE WeatherAPIMusaib;alter
USE WeatherAPIMusaib;

CREATE TABLE Apps
(
 appID VARCHAR(30) PRIMARY KEY,
 appName VARCHAR(30),
 appAccessToken VARCHAR(50),
 uID INT,
 FOREIGN KEY(uID) REFERENCES Users(uID),
 requests INT
);


CREATE TABLE  Users
(
 uID INT UNIQUE auto_increment,
 uEmail VARCHAR(30) PRIMARY KEY,
 uPass VARCHAR(50)
);


CREATE TABLE AppRequests
(
 appID VARCHAR(30) PRIMARY KEY,
 appAccessToken VARCHAR(50),
 uID INT,
 requests INT,
 FOREIGN KEY(uID) REFERENCES Users(uID)
);


select * from Users;
select * from Apps;

UPDATE Apps SET requests = 0 WHERE appID='h4';'

-- DROP TABLE Apps;
-- DROP TABLE Users;

SELECT SUM(requests) AS totalrequests FROM Apps WHERE uID = (SELECT uID FROM Apps WHERE appID = 'h4');
