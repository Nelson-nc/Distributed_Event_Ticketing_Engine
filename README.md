# <center> Event Ticketing System </center>
An Event Ticketing system for handling selling tickets for an Event with Queueing to handle large amount of user and unpaid
ticket, and database atomicity effeciently handle database queries.

## Features
- **instant Ticket Reservation**: when a user reserver's a ticket they don't immediately pay. 
The system temporarily locks a ticket for them and give them a **5-minute countdown timer** to complete their payment.

- **Secure Payment Verification**: it uses a mock payment(similar to PayStack) using secure cryptographic signature.

- **Automated Clean-up**: if the user fails to pay within 5-minute of reserving a ticket their resrvation is completely
wiped out, and the ticket is handed back to the pool.

## Problems fixed
- Double-Booking: if there is only 5 ticket remaining and 10 people wants it at the same time it might oversell but because
the system locks row during transactions we can prevent this from happening

- Server Bottlenecks & crashes: this is prevented due to the asynchronous manner of the program.

- Ticket hoarding: prevent bots or user from ruining sale by hoarding many tickets.


## Tech Stack 
- python
- Django
- rest_framework
- celery
- redis

## Getting Started
To run this project locally.

### Prerequisites
- git
- Python
- pip

### Installation
1. Clone this repository and change into its directory
```sh
git clone <this repo url>

# or download the project zip from github

cd ./path/to/cloned_dir
```
2. Setup a virtual environment
```sh
python -m venv .venv

# for Windows(CMD)
.venv\Scripts\activate.bat

# for Windows(Powershell)
.venv\Scripts\activate.ps1

# for macOS and linux
source .venv/bin/activate
```
3. Install dependencies
```sh
pip install -r requirements.txt
```
4. Make and apply migrations
```sh
python manage.py makemigrations
python manage.py migrate
```
5. CreateSuperuser for add event (for now)
```sh
python manage.py createsuperuser
```
6. Run the application
```sh
python manage.py runserver
```
## Contributing
contributions are a great thing, maybe you found a bug, something you feel needs to be changed or maybe it's just as an hobby your contributions are highly welcomed so feel free to contribute.

1. Fork this project repository
2. Create your **Feature branch**
```sh
git checkout -b <feature branch name>
```
3. Make your changes and commit
```sh
git commit -m "<feature commit message>"
```
4. Push your changes to the repository
```sh
git push origin <feature branch name>
```
5. Open up a Pull Request