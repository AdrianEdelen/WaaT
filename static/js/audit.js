document.addEventListener('DOMContentLoaded', () => {
    const approveBtn = document.getElementById('approveBtn');
    const editBtn = document.getElementById('editBtn');
    const nextBtn = document.getElementById('nextBtn');
    const messageDisplay = document.getElementById('messageDisplay');

    function fetchNextMessage() {
        fetch('/audit/next')
            .then(response => response.json())
            .then(data => {
                // Display the message in messageDisplay
            });
    }

    approveBtn.addEventListener('click', () => handleAction('approve'));
    editBtn.addEventListener('click', () => handleAction('edit'));
    nextBtn.addEventListener('click', fetchNextMessage);

    function handleAction(action) {
        // Send action to server
        fetch('/audit/action', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: action })
        }).then(() => fetchNextMessage()); // Fetch next message after action
    }

    fetchNextMessage(); // Initial call to load the first message
});
