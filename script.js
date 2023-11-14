
const buttons = document.querySelectorAll('.button');

// Add a click event listener to each button
buttons.forEach(button => {
    button.addEventListener('click', function(e) {
        // const text1 = this.querySelector('.text1').textContent;
        // const text2 = this.querySelector('.text2').textContent;
        // console.log(`Button Clicked: ${text1} - ${text2}`);
        if(this.classList.contains("occupied-button"))
        {
            if (this.classList.contains("plain-button")) {
                this.classList.remove("plain-button");
                this.classList.add("expanded-button");
                button.style.height = button.scrollHeight + "px";
            }
            else if (this.classList.contains("expanded-button")) {
                button.style.height = "30px"
                this.classList.remove("expanded-button");
                this.classList.add("plain-button");
            }
        }
    });
});

const apibutton = document.querySelector('.api-button')

apibutton.addEventListener('click', function(e) {
    if(!this.classList.contains('api-button-cooldown')) {
        // send update request
        fetch('http://127.0.0.1:5001/api/refresh', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })

        // prevent user from spamming
        this.classList.add("api-button-cooldown");
        this.querySelector('.status-text').textContent = 'Updated! Available in ~1m';
        setTimeout(() => {
            this.classList.remove('api-button-cooldown');
            this.querySelector('.status-text').textContent = 'API Update';
        }, 60000);
    }
})

const headers = {'Content-Type':'application/json',
                    'Access-Control-Allow-Origin':'*',
                    'Access-Control-Allow-Methods':'POST,PATCH,OPTIONS'}

const dateInput = document.getElementById("dateInput");
const startTimeInput = document.getElementById("startTime");
const endTimeInput = document.getElementById("endTime");

// Add input event listeners to the input fields
dateInput.addEventListener("input", sendDataToAPI);
startTimeInput.addEventListener("input", sendDataToAPI);
endTimeInput.addEventListener("input", sendDataToAPI);

function sendDataToAPI() {
    // Get input values
    const date = dateInput.value;
    const startTime = startTimeInput.value;
    const endTime = endTimeInput.value;

    // Create a data object to send to the API
    const data = {
        date: date,
        startTime: startTime,
        endTime: endTime
    };

    resetButtons();

    // receive data from backend
    fetch('http://127.0.0.1:5001/api/get_events', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data) // Convert data to a JSON string
    })
    .then(response => response.json())
    .then(data => {
        if (data) {
            resetButtons()
        

            const occupied = [];
            const reason = [];

            data.forEach(item => {
                occupied.push(...item.roomid);
                item.roomid.forEach(i => {
                    reason.push(item);
                })
            })

            let index = 0;

            occupied.forEach(roomId => {
                const elementId = `room${roomId}`;
                const element = document.getElementById(elementId);
                if(element)
                {
                    element.className = "plain-button occupied-button";
                    element.querySelector('.text1').textContent = "Booked"
                    
                    const text3Elt = element.querySelector('.text3')
                    if(text3Elt){
                        text3Elt.innerHTML += `${reason[index]['name']}<br>${reason[index]['start_time']}-${reason[index]['end_time']}<br>`;
                    }

                    
                }
                index++;
            })

        }
        
    })
    .catch(error => {
        // Handle errors.
        console.error(error);
    });
};

// return buttons to original state
function resetButtons() {
    buttons.forEach(button => {
        button.className = "plain-button button";
        button.style.height = "30px";
        button.querySelector('.text1').textContent = "Available";
        button.querySelector('.text3').innerHTML = "";
    })
}

