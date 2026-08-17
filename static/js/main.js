// Client-Side Validation and Dynamic Form Handlers for Student Profile Form

document.addEventListener('DOMContentLoaded', function() {
    // 1. Dynamic Project Field Adding / Removing
    const addProjectBtn = document.getElementById('add-project-btn');
    const projectsContainer = document.getElementById('projects-container');

    if (addProjectBtn && projectsContainer) {
        addProjectBtn.addEventListener('click', function() {
            const projectCount = projectsContainer.querySelectorAll('.project-row').length + 1;
            const newRow = document.createElement('div');
            newRow.className = 'project-row card p-3 mb-3 border-light shadow-sm';
            newRow.innerHTML = `
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <h6 class="fw-bold mb-0 text-secondary">Project #${projectCount}</h6>
                    <button type="button" class="btn btn-sm btn-outline-danger remove-project-btn">
                        <i class="bi bi-trash"></i> Remove
                    </button>
                </div>
                <div class="mb-2">
                    <label class="form-label small fw-semibold">Project Title</label>
                    <input type="text" name="project_title" class="form-control form-control-sm" placeholder="e.g. E-Commerce REST API">
                </div>
                <div>
                    <label class="form-label small fw-semibold">Project Description</label>
                    <textarea name="project_desc" class="form-control form-control-sm" rows="2" placeholder="Technologies used, key features, and your role..."></textarea>
                </div>
            `;
            projectsContainer.appendChild(newRow);
            attachRemoveHandlers();
        });
    }

    function attachRemoveHandlers() {
        const removeBtns = document.querySelectorAll('.remove-project-btn');
        removeBtns.forEach(btn => {
            btn.onclick = function() {
                const projectRow = this.closest('.project-row');
                if (projectRow) {
                    projectRow.remove();
                }
            };
        });
    }

    attachRemoveHandlers();

    // 2. Profile Form Validation Handler
    const profileForm = document.getElementById('student-profile-form');
    if (profileForm) {
        profileForm.addEventListener('submit', function(e) {
            const nameInput = document.getElementById('name');
            const emailInput = document.getElementById('email');
            const cgpaInput = document.getElementById('cgpa');

            let isValid = true;
            let errorMessage = "";

            if (nameInput && !nameInput.value.trim()) {
                isValid = false;
                errorMessage = "Please enter your full name.";
                nameInput.focus();
            } else if (emailInput && !validateEmail(emailInput.value.trim())) {
                isValid = false;
                errorMessage = "Please enter a valid email address.";
                emailInput.focus();
            } else if (cgpaInput) {
                const cgpaVal = parseFloat(cgpaInput.value);
                if (isNaN(cgpaVal) || cgpaVal < 0.0 || cgpaVal > 10.0) {
                    isValid = false;
                    errorMessage = "CGPA must be a number between 0.0 and 10.0.";
                    cgpaInput.focus();
                }
            }

            if (!isValid) {
                e.preventDefault();
                alert(errorMessage);
            }
        });
    }

    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    }
});
