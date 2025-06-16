const calendar = document.querySelector(".calendar"),
    date = document.querySelector(".date"),
    daysContainer = document.querySelector(".days"),
    prev = document.querySelector(".prev"),
    next = document.querySelector(".next"),
    todayBtn = document.querySelector(".today-btn"),
    gotoBtn = document.querySelector(".goto-btn"),
    dateInput = document.querySelector(".date-input"),
    eventDay = document.querySelector(".event-day"),
    eventDate = document.querySelector(".event-date"),
    eventsContainer = document.querySelector(".events"),
    addEventBtn = document.querySelector(".add-event"),
    addEventWrapper = document.querySelector(".add-event-wrapper"),
    addEventCloseBtn = document.querySelector(".close"),
    addEventTitle = document.querySelector(".event-name"),
    addEventFrom = document.querySelector(".event-time-from"),
    addEventTo = document.querySelector(".event-time-to"),
    addTaskTitle = document.querySelector(".task-name"),
    // addTaskDeadline = document.querySelector(".task-deadline"),
    // addTaskDuration = document.querySelector(".task-duration"),
    addEventSubmit = document.querySelector(".add-event-btn"),
    eventTypeRadios = document.querySelectorAll('input[name="flexibility"]'),
    fixedFields = document.querySelector(".fixed-fields"),
    flexibleFields = document.querySelector(".flexible-fields"),
    flexibleTasksContainer = document.querySelector(".flexible-tasks");

let today = new Date();
let activeDay;
let month = today.getMonth();
let year = today.getFullYear();

const months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
];

const eventsArr = [];
getEvents();

// Toggle fields based on event type
// eventTypeRadios.forEach(radio => {
//     radio.addEventListener("change", () => {
//         if (radio.value === "fixed") {
//             fixedFields.style.display = "block";
//             flexibleFields.style.display = "none";
//         } else {
//             fixedFields.style.display = "none";
//             flexibleFields.style.display = "block";
//         }
//     });
// });

// Initialize calendar (unchanged from original)
function initCalendar() {
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const prevLastDay = new Date(year, month, 0);
    const prevDays = prevLastDay.getDate();
    const lastDate = lastDay.getDate();
    const day = firstDay.getDay();
    const nextDays = 7 - lastDay.getDay() - 1;

    date.innerHTML = months[month] + " " + year;

    let days = "";
    for (let x = day; x > 0; x--) {
        days += `<div class="day prev-date">${prevDays - x + 1}</div>`;
    }
    for (let i = 1; i <= lastDate; i++) {
        let event = false;
        eventsArr.forEach((eventObj) => {
            if (
                eventObj.day === i &&
                eventObj.month === month + 1 &&
                eventObj.year === year
            ) {
                event = true;
            }
        });
        if (
            i === new Date().getDate() &&
            year === new Date().getFullYear() &&
            month === new Date().getMonth()
        ) {
            activeDay = i;
            getActiveDay(i);
            updateEvents(i);
            days += event ? `<div class="day today active event">${i}</div>` : `<div class="day today active">${i}</div>`;
        } else {
            days += event ? `<div class="day event">${i}</div>` : `<div class="day">${i}</div>`;
        }
    }
    for (let j = 1; j <= nextDays; j++) {
        days += `<div class="day next-date">${j}</div>`;
    }
    daysContainer.innerHTML = days;
    addListner();
}

// Other calendar functions (prevMonth, nextMonth, addListner, etc.) remain unchanged
function prevMonth() {
    month--;
    if (month < 0) {
        month = 11;
        year--;
    }
    initCalendar();
}

function nextMonth() {
    month++;
    if (month > 11) {
        month = 0;
        year++;
    }
    initCalendar();
}

prev.addEventListener("click", prevMonth);
next.addEventListener("click", nextMonth);

function addListner() {
    const days = document.querySelectorAll(".day");
    days.forEach((day) => {
        day.addEventListener("click", (e) => {
            getActiveDay(e.target.innerHTML);
            updateEvents(Number(e.target.innerHTML));
            activeDay = Number(e.target.innerHTML);
            days.forEach((day) => {
                day.classList.remove("active");
            });
            if (e.target.classList.contains("prev-date")) {
                prevMonth();
                setTimeout(() => {
                    const days = document.querySelectorAll(".day");
                    days.forEach((day) => {
                        if (
                            !day.classList.contains("prev-date") &&
                            day.innerHTML === e.target.innerHTML
                        ) {
                            day.classList.add("active");
                        }
                    });
                }, 100);
            } else if (e.target.classList.contains("next-date")) {
                nextMonth();
                setTimeout(() => {
                    const days = document.querySelectorAll(".day");
                    days.forEach((day) => {
                        if (
                            !day.classList.contains("next-date") &&
                            day.innerHTML === e.target.innerHTML
                        ) {
                            day.classList.add("active");
                        }
                    });
                }, 100);
            } else {
                e.target.classList.add("active");
            }
        });
    });
}

todayBtn.addEventListener("click", () => {
    today = new Date();
    month = today.getMonth();
    year = today.getFullYear();
    initCalendar();
});

dateInput.addEventListener("input", (e) => {
    dateInput.value = dateInput.value.replace(/[^0-9/]/g, "");
    if (dateInput.value.length === 2) {
        dateInput.value += "/";
    }
    if (dateInput.value.length > 7) {
        dateInput.value = dateInput.value.slice(0, 7);
    }
    if (e.inputType === "deleteContentBackward") {
        if (dateInput.value.length === 3) {
            dateInput.value = dateInput.value.slice(0, 2);
        }
    }
});

gotoBtn.addEventListener("click", gotoDate);

function gotoDate() {
    const dateArr = dateInput.value.split("/");
    if (dateArr.length === 2 && dateArr[0] > 0 && dateArr[0] < 13 && dateArr[1].length === 4) {
        month = dateArr[0] - 1;
        year = dateArr[1];
        initCalendar();
        return;
    }
    alert("Invalid Date");
}

function getActiveDay(date) {
    const day = new Date(year, month, date);
    const dayName = day.toString().split(" ")[0];
    eventDay.innerHTML = dayName;
    eventDate.innerHTML = date + " " + months[month] + " " + year;
}
//to change
function updateEvents(date) {
    let events = "";
    eventsArr.forEach((event) => {
        if (
            date === event.day &&
            month + 1 === event.month &&
            year === event.year
        ) {
            event.events.forEach((event) => {
                if(event.type!=="flexible")
                {
                    events += `<div class="event">
                    <div class="title">
                        <i class="fas fa-circle"></i>
                        <h3 class="event-title">${event.title}</h3>
                    </div>
                    <div class="event-time">
                        <span class="event-time">${event.time}</span>
                    </div>
                </div>`;
            }
                // else {
                //     events += `<div class="event">
                //     <div class="title">
                //         <i class="fas fa-circle"></i>
                //         <h3 class="event-title">${event.title}</h3>
                //     </div>
                //     <div class="event-time">
                //         <span class="event-time">${event.time}</span>
                //         <span class="event-time">${event.priority}</span>
                //     </div>
                // </div>`;
                // }
            });
        }
    });
    if (events === "") {
        events = `<div class="no-event"><h3>No Fixed Events</h3></div>`;
    }
    eventsContainer.innerHTML = events;
    saveEvents();
}

addEventBtn.addEventListener("click", () => {
    addEventWrapper.classList.toggle("active");
});

addEventCloseBtn.addEventListener("click", () => {
    addEventWrapper.classList.remove("active");
});

document.addEventListener("click", (e) => {
    if (e.target !== addEventBtn && !addEventWrapper.contains(e.target)) {
        addEventWrapper.classList.remove("active");
    }
});

addEventTitle.addEventListener("input", (e) => {
    addEventTitle.value = addEventTitle.value.slice(0, 60);
});

addEventFrom.addEventListener("input", (e) => {
    addEventFrom.value = addEventFrom.value.replace(/[^0-9:]/g, "");
    if (addEventFrom.value.length === 2) {
        addEventFrom.value += ":";
    }
    if (addEventFrom.value.length > 5) {
        addEventFrom.value = addEventFrom.value.slice(0, 5);
    }
});

addEventTo.addEventListener("input", (e) => {
    addEventTo.value = addEventTo.value.replace(/[^0-9:]/g, "");
    if (addEventTo.value.length === 2) {
        addEventTo.value += ":";
    }
    if (addEventTo.value.length > 5) {
        addEventTo.value = addEventTo.value.slice(0, 5);
    }
});

// addTaskDeadline.addEventListener("input", (e) => {
//     addTaskDeadline.value = addTaskDeadline.value.replace(/[^0-9-: ]/g, "");
// });

// addTaskDuration.addEventListener("input", (e) => {
//     addTaskDuration.value = addTaskDuration.value.replace(/[^0-9.]/g, "");
// });
function timeToMinutes(t) {
  const [hh, mm] = t.split(':').map(Number);
  return hh * 60 + mm;
}
addEventSubmit.addEventListener("click", () => {
    const selected = document.querySelector('input[name="flexibility"]:checked');
    console.log(selected);
    if (!selected) {
    alert('Please select an event flexibility.');
    return;
    }
    const eventType = selected.value;
    let eventData;
    if (eventType === "not-flexible") {
        const eventTitle = addEventTitle.value;
        const eventTimeFrom = addEventFrom.value;
        const eventTimeTo = addEventTo.value;
        if (eventTitle === "" || eventTimeFrom === "" || eventTimeTo === "") {
            alert("Please fill all fields for fixed-time event");
            return;
        }
        const timeFromArr = eventTimeFrom.split(":");
        const timeToArr = eventTimeTo.split(":");
        if (
            timeFromArr.length !== 2 ||
            timeToArr.length !== 2 ||
            timeFromArr[0] > 23 ||
            timeFromArr[1] > 59 ||
            timeToArr[0] > 23 ||
            timeToArr[1] > 59
        ) {
            alert("Invalid Time Format");
            return;
        }
        const timeFrom = convertTime(eventTimeFrom);
        const timeTo = convertTime(eventTimeTo);
        let eventExist = false;
        eventsArr.forEach((event) => {
            if (
                event.day === activeDay &&
                event.month === month + 1 &&
                event.year === year
            ) {
                event.events.forEach((event) => {
                    if (event.title === eventTitle) {
                        eventExist = true;
                    }
                });
            }
        });
        if (eventExist) {
            alert("Event already added");
            return;
        }
        //to change
        const newEvent = {
            title: eventTitle,
            time: timeFrom + " - " + timeTo,
            priority: null
        };
        let eventAdded = false;
        if (eventsArr.length > 0) {
            eventsArr.forEach((item) => {
                if (
                    item.day === activeDay &&
                    item.month === month + 1 &&
                    item.year === year
                ) {
                    item.events.push(newEvent);
                    eventAdded = true;
                }
            });
        }
        if (!eventAdded) {
            eventsArr.push({
                day: activeDay,
                month: month + 1,
                year: year,
                events: [newEvent]
            });
        }
        eventData = {
            type: "fixed",
            title: eventTitle,
            timeFrom: eventTimeFrom,
            timeTo: eventTimeTo,
            day: activeDay,
            month: month + 1,
            year: year,
            priority: null
        };
        addEventWrapper.classList.remove("active");
        addEventTitle.value = "";
        addEventFrom.value = "";
        addEventTo.value = "";
        updateEvents(activeDay);
        const activeDayEl = document.querySelector(".day.active");
        if (!activeDayEl.classList.contains("event")) {
            activeDayEl.classList.add("event");
        }
    } else {
        const addTaskTitle = document.querySelector(".event-name");
        const taskTitle = addTaskTitle.value;
        // const taskDeadline = addTaskDeadline.value;
        // const taskDuration = addTaskDuration.value;
        const taskDeadline=timeToMinutes(addEventTo.value);
        const taskDuration=Math.abs(timeToMinutes(addEventTo.value)-timeToMinutes(addEventFrom.value));
        if (isNaN(taskDuration) || taskDuration <= 0) {
            alert("Duration must be a positive number");
            return;
        }
        eventData = {
            type: "flexible",
            title: taskTitle,
            deadline: taskDeadline,
            duration: parseFloat(taskDuration)/60,
            day:activeDay,
            month:month,
            year:year
        };
        addEventWrapper.classList.remove("active");
        addTaskTitle.value = "";
        addEventTo.value="";
        addEventFrom.value="";
    }
    fetch("/add-event", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(eventData)
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                alert("success sending data to backend");
                // const list = Array.isArray(data) ? data :(Array.isArray(data.events) ? data.events : []);
                // // now safely append
                // list.forEach(ev => eventsArr.push(ev));
                // eventsArr.push(...JSON.parse(data));
                // console.log("DATA:",data);
                // console.log(eventsArr);
                // saveEvents();
                // initCalendar();
                // updateEvents(activeDay);
                updateFlexibleTasks();
            } else {
                alert("Failed to add event/task" ,(data.message));
                console.log(data.message);
            }
        })
        .catch(error => console.error("Error:", error));
        updateFlexibleTasks();
});

function updateFlexibleTasks() {
    fetch('/get-events')
    .then(response => {
        if (!response.ok) throw new Error(`Server returned ${response.status}`);
        return response.json();
    })
    .then(data => {
        const flexibleTasks = data.filter(evt => evt.type === "flexible"&&evt.day>=activeDay);
        const seen = new Set();
        const uniqueFlexibleTasks = flexibleTasks.filter(task => {
            if (seen.has(task.title)) {
                return false;
            }
            seen.add(task.title);
            return true;
        });
        
        let tasksHtml = '';
        flexibleTasks.forEach(task => {
            tasksHtml += `
            <div class="event">
            <div class="title">
            <i class="fas fa-circle"></i>
            <h3 class="event-title">${task.title}</h3>
            </div>
            <div class="event-time">
            <span>Deadline: ${task.deadline}</span>
            <span>Duration: ${task.duration.toFixed(2)}h</span>
            <span>Priority :${task.priority}</span>
            </div>
            <div class="event-date">
            ${task.day}/${task.month}/${task.year}
            </div>
            </div>`;
        });
        
        // 4. Deduplicate into your local array
        flexibleTasks.forEach(evt => {
            const exists = eventsArr.some(e =>
                e.day      === evt.day &&
                e.month    === evt.month &&
                e.year     === evt.year &&
                e.title    === evt.title &&
                e.type     === evt.type
            );
            if (!exists) {
                // eventsArr.push(evt);
                eventsContainer.innerHTML += tasksHtml;}
            });
            
            console.log("Flexible tasks loaded:", flexibleTasks);
            console.log("eventsArr after update:", eventsArr);
        })
        .catch(error => console.error("Error fetching tasks:", error));
        initCalendar();
    } 
    eventsContainer.addEventListener("click", (e) => {
        if (e.target.classList.contains("event")) {
            if (confirm("Are you sure you want to delete this event?")) {
                const eventTitle = e.target.children[0].children[1].innerHTML;
                eventsArr.forEach((event) => {
                    if (
                        event.day === activeDay &&
                        event.month === month + 1 &&
                        event.year === year
                    ) {
                        event.events.forEach((item, index) => {
                            if (item.title === eventTitle) {
                                event.events.splice(index, 1);
                            }
                        });
                        if (event.events.length === 0) {
                            eventsArr.splice(eventsArr.indexOf(event), 1);
                            const activeDayEl = document.querySelector(".day.active");
                            if (activeDayEl.classList.contains("event")) {
                                activeDayEl.classList.remove("event");
                            }
                        }
                    }
                });
                updateEvents(activeDay);
            }
        }
    });
    function saveEvents() {
    localStorage.setItem("fixedevents", JSON.stringify(eventsArr));
}

function getEvents() {
    if (localStorage.getItem("fixedevents") !== null) {
        eventsArr.push(...JSON.parse(localStorage.getItem("fixedevents")));
    }
    updateFlexibleTasks();
    initCalendar();
}

function convertTime(time) {
    let timeArr = time.split(":");
    let timeHour = parseInt(timeArr[0]);
    let timeMin = timeArr[1];
    let timeFormat = timeHour >= 12 ? "PM" : "AM";
    timeHour = timeHour % 12 || 12;
    return timeHour + ":" + timeMin + " " + timeFormat;
}

initCalendar();