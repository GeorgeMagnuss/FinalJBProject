// Main JavaScript file for Vacation Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Image preview for file inputs
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Create or update preview
                    let preview = input.parentNode.querySelector('.image-preview');
                    if (!preview) {
                        preview = document.createElement('img');
                        preview.className = 'image-preview img-thumbnail mt-2';
                        preview.style.maxWidth = '200px';
                        input.parentNode.appendChild(preview);
                    }
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add loading states to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton && this.checkValidity()) {
                submitButton.classList.add('loading');
                submitButton.disabled = true;
                const originalText = submitButton.innerHTML;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
                
                // Re-enable after 10 seconds as fallback
                setTimeout(() => {
                    submitButton.classList.remove('loading');
                    submitButton.disabled = false;
                    submitButton.innerHTML = originalText;
                }, 10000);
            }
        });
    });
});

// Utility functions
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const mainContainer = document.querySelector('main.container');
    if (mainContainer) {
        mainContainer.insertBefore(alertContainer, mainContainer.firstChild);
        
        // Auto-hide success and info alerts
        if (type === 'success' || type === 'info') {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alertContainer);
                bsAlert.close();
            }, 5000);
        }
    }
}

function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return confirm(message);
}

// CSRF token helper for AJAX requests
function getCSRFToken() {
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfInput ? csrfInput.value : '';
}

// Fetch wrapper with CSRF token
function csrfFetch(url, options = {}) {
    const defaultOptions = {
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json',
        },
    };
    
    return fetch(url, { ...defaultOptions, ...options });
}