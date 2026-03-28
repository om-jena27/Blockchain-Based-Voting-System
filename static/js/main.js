function castVote(candidateId) {
    const formData = new FormData();
    formData.append('candidate_id', candidateId);
    
    fetch('/vote', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if(data.error) {
            alert(data.error);
        } else {
            alert(data.success);
            window.location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
}

function updateTurnout() {
    fetch('/api/turnout')
        .then(res => res.json())
        .then(data => {
            const el = document.getElementById('total-turnout-count');
            if (el && data.total_votes !== undefined) {
                el.innerText = data.total_votes;
            }
        })
        .catch(console.error);
}

function updateCountdown() {
    if (!window.electionEndTime) return;
    
    const end = new Date(window.electionEndTime).getTime();
    const now = new Date().getTime();
    const distance = end - now;
    
    const adminTimer = document.getElementById('countdown-timer');
    const voterTimer = document.getElementById('countdown-timer-voter');
    
    if (distance < 0) {
        if(adminTimer) adminTimer.innerText = "ENDED";
        if(voterTimer) voterTimer.innerText = "ENDED";
        return;
    }
    
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
    const formatted = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    
    if(adminTimer) adminTimer.innerText = formatted;
    if(voterTimer) voterTimer.innerText = formatted;
}

document.addEventListener('DOMContentLoaded', () => {
    if(document.getElementById('total-turnout-count')) {
        setInterval(updateTurnout, 3000);
    }
    if(window.electionEndTime) {
        updateCountdown();
        setInterval(updateCountdown, 1000);
    }
});
