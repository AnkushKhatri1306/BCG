# BCG
Hi, Guide for Frontend and Backend code for Insurance Policy

Frontend :
	1. First install all the dependencies using cmd npm install 
	2. After installing run the cmd ng serve
	3. Serve will up and running
	

Backend :
	1. Open the folder where the backend code is present 
	2. Install all the dependencies mentioned in requirements.txt file using cmd pip install <dependency name>
	3. Now go to setting.py file present in insurance app and change the database settings for postgresql
	4. After setting the things in setting file
	5. Go to the path where manage.py file exists and run the follwing command
		- python manage.py makemigrations
		- python manage.py migrate
		- python manage.py runserver 127.0.0.1:9001
		
	6. For first time data need to upload in the database for that you can hit the URL mentioned below from postman 
		and need to paas params as :
			file : <file object>
		http:127.0.0.1:9001/policy/home/data_upload/
	
		

Now go to localhost:4200 in browser and reload it and see the application running .
