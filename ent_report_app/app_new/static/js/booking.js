// Booking functionality
function loadSlots() {
    const doctorSelect = document.getElementById('doctor-select');
    const dateSelect = document.getElementById('date-select');
    const slotsContainer = document.getElementById('slots-container');
    
    if (!doctorSelect.value || !dateSelect.value) {
        slotsContainer.innerHTML = '<p class="text-muted">Select a doctor and date to view available slots</p>';
        return;
    }
    
    const doctorId = doctorSelect.value;
    const date = dateSelect.value;
    
    fetch(`/booking/api/slots/${doctorId}/${date}`)
        .then(response => response.json())
        .then(data => {
            if (data.slots && data.slots.length > 0) {
                slotsContainer.innerHTML = data.slots.map(slot => `
                    <button class="slot-btn ${slot.available ? 'available' : 'disabled'}" 
                            onclick="selectSlot(this, ${slot.id})"
                            ${!slot.available ? 'disabled' : ''}>
                        ${slot.start_time} - ${slot.end_time}
                    </button>
                `).join('');
            } else {
                slotsContainer.innerHTML = '<p class="text-muted">No available slots for selected date</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            slotsContainer.innerHTML = '<p class="text-muted">Error loading slots</p>';
        });
}

function selectSlot(element, slotId) {
    // Remove previous selection
    document.querySelectorAll('.slot-btn').forEach(btn => btn.classList.remove('selected'));
    
    // Mark this slot as selected
    element.classList.add('selected');
    
    // Store selected slot
    document.getElementById('selected-slot-id').value = slotId;
}

// Initialize date picker with minimum date
document.addEventListener('DOMContentLoaded', () => {
    const dateSelect = document.getElementById('date-select');
    if (dateSelect) {
        const today = new Date();
        const minDate = today.toISOString().split('T')[0];
        const maxDate = new Date(today.getTime() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
        
        dateSelect.min = minDate;
        dateSelect.max = maxDate;
    }
    
    // Create hidden input for selected slot if it doesn't exist
    if (!document.getElementById('selected-slot-id')) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.id = 'selected-slot-id';
        input.name = 'slot_id';
        document.querySelector('form').appendChild(input);
    }
});

// Phone number validation
document.addEventListener('DOMContentLoaded', () => {
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '').slice(0, 10);
        });
    }
});
