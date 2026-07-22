const browserStatus = document.getElementById("browserStatus");
const focusCount = document.getElementById("focusCount");
const lastFocusTime = document.getElementById("lastFocusTime");

let count = 0;

function logBrowserEvent(eventType, remarks) {

    fetch("/browser_event", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            event_type: eventType,
            remarks: remarks
        })
    });

}

document.addEventListener("visibilitychange", function () {

    if (document.hidden) {

        browserStatus.innerHTML = "Browser Inactive";
        browserStatus.style.color = "red";

        count++;
        focusCount.innerHTML = count;

        const now = new Date().toLocaleString();
        lastFocusTime.innerHTML = now;

        logBrowserEvent(
            "Browser Focus Lost",
            "Candidate switched away from exam window"
        );

    }
    else {

        browserStatus.innerHTML = "Browser Active";
        browserStatus.style.color = "green";

        logBrowserEvent(
            "Browser Focus Regained",
            "Candidate returned to exam window"
        );

    }

});