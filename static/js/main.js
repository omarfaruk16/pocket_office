document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('[onclick*="confirm"]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });
    
    // Calculate attendance percentage
    function calculateAttendancePercentage() {
        const rows = document.querySelectorAll('#attendance-table tbody tr');
        rows.forEach(function(row) {
            const attendanceCells = row.querySelectorAll('.attendance-cell');
            let presentCount = 0;
            let totalCount = 0;
            
            attendanceCells.forEach(function(cell) {
                if (cell.textContent.trim() === 'P') {
                    presentCount++;
                }
                if (cell.textContent.trim() !== 'N/A') {
                    totalCount++;
                }
            });
            
            const percentageCell = row.querySelector('.percentage-cell');
            if (percentageCell && totalCount > 0) {
                const percentage = (presentCount / totalCount * 100).toFixed(1);
                percentageCell.textContent = percentage + '%';
            }
        });
    }
    
    // Initialize attendance calculation if table exists
    if (document.getElementById('attendance-table')) {
        calculateAttendancePercentage();
    }
});