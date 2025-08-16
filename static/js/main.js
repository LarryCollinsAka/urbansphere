function getAirQuality() {
    fetch('/air_quality')
        .then(res => res.json())
        .then(data => {
            document.getElementById('output').innerText =
                `Air Quality: ${data.level} (PM2.5: ${data.pm25})\nAdvice: ${data.advice}`;
        });
}

function getHousingUpgrades() {
    fetch('/housing')
        .then(res => res.json())
        .then(data => {
            let upgrades = data.map(item =>
                `${item.type}: ${item.desc}`).join('\n');
            document.getElementById('output').innerText = upgrades;
        });
}

function getCivicFeedback() {
    fetch('/civic')
        .then(res => res.json())
        .then(data => {
            let feedback = data.map(item =>
                `${item.user}: ${item.message}`).join('\n');
            document.getElementById('output').innerText = feedback;
        });
}