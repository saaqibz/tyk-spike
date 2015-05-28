#Tyk Spike Setup:

I’m running this off of an Ubuntu 14.04LTS Virtual machine. I may have some dependencies installed as global so please let me know if you run into any issues setting up the investigative prototype (a.k.a. ‘spike’). This prototype uses the tyk docker build to proxy, secure, and manage an api resource setup with a flask application server as well as an angular app.

#Stack Elements:

- Tyk Docker Setup – includes
	
	o	Mongo (Analytics Storage),
	
	o	Redis (API Mgmt Storage), 
	
	o	Tyk Host Manager (Nginx) : Port 8888, 
	
	o	Tyk Gateway : Port 8080
	
	o	Tyk Dashboard (UI Interface and API) : Port 3000

- Flask-Angular Yeoman Generator - Includes:
	
	o	Html/Angular – Front End interface
	
	o	Flask – Application Server / API resource : Port 15000
	
	o	SQLite – Resource accessed with API (app.db)

# Setup

## To Setup Tyk:

Additional References can be found here: https://tyk.io/blog/running-tyk-with-docker/

- Install docker (in Ubuntu 14.04LTS it’s `sudo apt-get install docker.io`)
- create a docker group and add your user to it so you’re not running it as root following the below directions: https://docs.docker.com/installation/ubuntulinux/#create-a-docker-group
- You will need to have a local DNS setup. You can do this by modifying the hosts file or you can setup a local dns for the desired extensions using dnsmasq set up with the following guide:

	o	https://www.computersnyou.com/3786/how-to-setup-dnsmasq-local-dns/
	
	o	note the guide sets things up for the TLD of ‘.dev’ we want it for the TLD of ‘.docker’
e.g., `server=/dev/127.0.0.1`  for us should be `server=/docker/127.0.0.1`

- Goto the docker folder and run `./tyk_quickstart.sh`
	
	o	This will take a long time so go ahead and setup flask in the meantime
	
	o	Eventually the docker images will all download and be run
	
You should be able to access the docker dashboard now. Check this by visiting http://tyk.docker:3000/ (cj@test.com / test123)

## Setup API:

- Check the docker folder for an api.json file. this has 3 api description objects in json form. These objects are the Website “API” (keyless), the Auth API (keyless), and the Restricted api (OAuth2)
- go to the dashboard and go to Apis on the left nav then to the ‘import api’ button
- Import each api one by one until you have all 3
- Edit each api so the target ip address is the ip address of your local machine. For some reason localhost or tyk.docker does not work for me but the actual LAN address does.
- Click ‘Oauth Clients’ in the Restricted api.
- Select +Add new Client and add a new one. make the redirect_uri  = http://localhost:15000/auth/store_token
- view this client and copy the client app id and store it somewhere on your computer for now. This becomes useful when you are setting up your flask app.


## To Setup Flask:

- git clone the repo
- run `./install.sh` to install the flask angular stuff
- run `npm install` to install npm packages
- run `bower install` to install bower packages
- go into app/routes/index.py and change the value of app_id in the APICONFIG class to the client app id that you had previously stored then save the file.

Test your flask install by running the following from the tyk-spike parent directory

1. ` source flask/bin/activate` - this sets you up with the python virtual environment
2. `python run.py` - this runs the flask server
3. Open your browser and go to http://localhost:15000/ to see if the server loads a page with a simple login form.