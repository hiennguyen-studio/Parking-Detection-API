// Dashboard JavaScript Functions

// API Base URL
const API_URL = '/api/v1';

/**
 * Load statistics from API
 */
async function loadStatistics() {
    try {
        const response = await fetch(`${API_URL}/statistics/summary`);
        const data = await response.json();
        
        document.getElementById('total-violations').textContent = data.total_violations || 0;
        document.getElementById('today-violations').textContent = data.violations_today || 0;
        document.getElementById('active-cameras').textContent = data.active_cameras || 0;
        document.getElementById('confirmed-violations').textContent = data.confirmed_violations || 0;
    } catch (error) {
        console.error('Error loading statistics:', error);
        showAlert('Lỗi khi tải thống kê', 'danger');
    }
}

/**
 * Load recent violations
 */
async function loadRecentViolations() {
    try {
        const response = await fetch(`${API_URL}/violations?limit=10`);
        const data = await response.json();
        
        const tbody = document.getElementById('violations-tbody');
        if (!tbody) return;
        
        tbody.innerHTML = '';
        
        data.forEach(violation => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${violation.id}</td>
                <td>${violation.plate_number}</td>
                <td>${violation.camera_id}</td>
                <td>${(violation.confidence * 100).toFixed(1)}%</td>
                <td>${new Date(violation.created_at).toLocaleString('vi-VN')}</td>
                <td>${violation.is_confirmed ? '<span class="badge confirmed">Đã xác nhận</span>' : '<span class="badge unconfirmed">Chưa xác nhận</span>'}</td>
                <td>
                    <button class="small" onclick="viewViolation(${violation.id})">Xem</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading violations:', error);
        showAlert('Lỗi khi tải danh sách vi phạm', 'danger');
    }
}

/**
 * Load violations with pagination
 */
let currentPage = 1;
const itemsPerPage = 20;

async function loadViolations() {
    try {
        const skip = (currentPage - 1) * itemsPerPage;
        const response = await fetch(`${API_URL}/violations?skip=${skip}&limit=${itemsPerPage}`);
        const data = await response.json();
        
        const tbody = document.getElementById('violations-tbody');
        tbody.innerHTML = '';
        
        data.forEach(violation => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${violation.id}</td>
                <td>${violation.plate_number}</td>
                <td>Camera ${violation.camera_id}</td>
                <td>Unknown</td>
                <td>${(violation.confidence * 100).toFixed(1)}%</td>
                <td>${violation.is_confirmed ? '<span class="badge confirmed">Đã xác nhận</span>' : '<span class="badge unconfirmed">Chưa xác nhận</span>'}</td>
                <td>${new Date(violation.created_at).toLocaleString('vi-VN')}</td>
                <td>
                    <button class="small" onclick="viewViolation(${violation.id})">Chi tiết</button>
                    ${!violation.is_confirmed ? `<button class="small success" onclick="confirmViolation(${violation.id})">Xác nhận</button>` : ''}
                </td>
            `;
            tbody.appendChild(row);
        });
        
        document.getElementById('page-info').textContent = `Trang ${currentPage}`;
    } catch (error) {
        console.error('Error loading violations:', error);
    }
}

function nextPage() {
    currentPage++;
    loadViolations();
}

function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        loadViolations();
    }
}

/**
 * View violation details
 */
function viewViolation(violationId) {
    alert(`Xem chi tiết vi phạm #${violationId}`);
    // TODO: Implement detailed view
}

/**
 * Confirm a violation
 */
async function confirmViolation(violationId) {
    if (!confirm('Xác nhận vi phạm này?')) return;
    
    try {
        const response = await fetch(`${API_URL}/violations/${violationId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ is_confirmed: true })
        });
        
        if (response.ok) {
            showAlert('Vi phạm đã được xác nhận', 'success');
            loadViolations();
        } else {
            showAlert('Lỗi khi xác nhận vi phạm', 'danger');
        }
    } catch (error) {
        console.error('Error confirming violation:', error);
        showAlert('Lỗi khi xác nhận vi phạm', 'danger');
    }
}

/**
 * Apply filters
 */
function applyFilters() {
    const plate = document.getElementById('filter-plate').value;
    const status = document.getElementById('filter-status').value;
    
    // TODO: Implement filtering logic
    console.log(`Filter plate: ${plate}, status: ${status}`);
    loadViolations();
}

/**
 * Update statistics
 */
function updateStatistics() {
    const dateFrom = document.getElementById('date-from').value;
    const dateTo = document.getElementById('date-to').value;
    const cameraId = document.getElementById('camera-select').value;
    
    // TODO: Implement statistics update with filters
    console.log(`Update statistics from ${dateFrom} to ${dateTo}, camera ${cameraId}`);
    loadStatistics();
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    document.body.insertBefore(alertDiv, document.body.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

/**
 * Format date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('vi-VN');
}

/**
 * Initialize dashboard on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('Dashboard initialized');
    loadStatistics();
});
