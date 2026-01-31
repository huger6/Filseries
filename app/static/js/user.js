document.addEventListener('DOMContentLoaded', () => {
    // =========================
    // Avatar Upload
    // =========================
    const avatarWrapper = document.querySelector('.user-avatar-wrapper');
    const pfpInput = document.getElementById('pfpInput');
    const userAvatar = document.getElementById('userAvatar');

    avatarWrapper.addEventListener('click', () => pfpInput.click());

    pfpInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        if (!file.type.startsWith('image/')) {
            showToast('Please select an image file.', 'error');
            return;
        }

        if (file.size > 5 * 1024 * 1024) {
            showToast('Image size must be less than 5MB.', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('pfp', file);

        try {
            const response = await fetch('{{ url_for("auth.upload_profile_picture") }}', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                userAvatar.innerHTML = `<img src="{{ url_for('auth.get_profile_picture') }}?t=${Date.now()}" alt="Profile Picture" class="avatar-img">`;
                showToast('Profile picture updated!', 'success');
            } else {
                showToast(data.error || 'Failed to upload image.', 'error');
            }
        } catch (error) {
            console.error('Upload error:', error);
            showToast('An error occurred while uploading.', 'error');
        }
    });

    // =========================
    // Username Change with Debounce
    // =========================
    const usernameInput = document.getElementById('new-username');
    const usernameStatus = document.getElementById('username-status');
    const usernameFeedback = document.getElementById('username-feedback');
    const saveUsernameBtn = document.getElementById('save-username-btn');
    const usernameDisplay = document.getElementById('usernameDisplay');
    
    let usernameDebounceTimer;
    let isUsernameAvailable = false;

    function setUsernameStatus(status, message) {
        const loadingIcon = usernameStatus.querySelector('.loading-icon');
        const successIcon = usernameStatus.querySelector('.success-icon');
        const errorIcon = usernameStatus.querySelector('.error-icon');
        
        loadingIcon.classList.add('d-none');
        successIcon.classList.add('d-none');
        errorIcon.classList.add('d-none');
        
        usernameFeedback.textContent = message || '';
        usernameFeedback.className = 'input-feedback';
        
        switch(status) {
            case 'loading':
                loadingIcon.classList.remove('d-none');
                break;
            case 'success':
                successIcon.classList.remove('d-none');
                usernameFeedback.classList.add('feedback-success');
                isUsernameAvailable = true;
                break;
            case 'error':
                errorIcon.classList.remove('d-none');
                usernameFeedback.classList.add('feedback-error');
                isUsernameAvailable = false;
                break;
            default:
                isUsernameAvailable = false;
        }
        
        saveUsernameBtn.disabled = !isUsernameAvailable;
    }

    usernameInput.addEventListener('input', () => {
        const value = usernameInput.value.trim();
        
        clearTimeout(usernameDebounceTimer);
        
        if (value.length === 0) {
            setUsernameStatus('', '');
            return;
        }
        
        if (value.length < 3) {
            setUsernameStatus('error', 'Username must be at least 3 characters');
            return;
        }
        
        // Validate format locally first
        const usernamePattern = /^[a-zA-Z0-9_.]{3,12}$/;
        if (!usernamePattern.test(value)) {
            setUsernameStatus('error', 'Only letters, numbers, _ and . allowed');
            return;
        }
        
        setUsernameStatus('loading', 'Checking availability...');
        
        // Debounce the API call
        usernameDebounceTimer = setTimeout(async () => {
            try {
                const response = await fetch('{{ url_for("auth.check_username_availability") }}', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username: value })
                });
                
                const data = await response.json();
                
                if (data.available) {
                    setUsernameStatus('success', data.message);
                } else {
                    setUsernameStatus('error', data.message);
                }
            } catch (error) {
                setUsernameStatus('error', 'Error checking availability');
            }
        }, 500); // 500ms debounce
    });

    saveUsernameBtn.addEventListener('click', async () => {
        if (!isUsernameAvailable) return;
        
        const newUsername = usernameInput.value.trim();
        saveUsernameBtn.disabled = true;
        saveUsernameBtn.innerHTML = '<i class="bi bi-hourglass-split"></i> Saving...';
        
        try {
            const response = await fetch('{{ url_for("auth.update_username") }}', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: newUsername })
            });
            
            const data = await response.json();
            
            if (data.success) {
                usernameDisplay.textContent = '@' + data.new_username;
                usernameInput.value = '';
                setUsernameStatus('', '');
                showToast('Username updated successfully!', 'success');
            } else {
                showToast(data.error || 'Failed to update username', 'error');
            }
        } catch (error) {
            showToast('An error occurred', 'error');
        } finally {
            saveUsernameBtn.innerHTML = '<i class="bi bi-check-lg"></i> Save Username';
            saveUsernameBtn.disabled = true;
        }
    });

    // =========================
    // Password Change
    // =========================
    const currentPwInput = document.getElementById('current-password');
    const newPwInput = document.getElementById('new-password');
    const confirmPwInput = document.getElementById('confirm-password');
    const savePasswordBtn = document.getElementById('save-password-btn');
    const passwordMatchFeedback = document.getElementById('password-match-feedback');
    
    // Password requirements
    const reqLength = document.getElementById('req-length');
    const reqUpper = document.getElementById('req-upper');
    const reqLower = document.getElementById('req-lower');
    const reqNumber = document.getElementById('req-number');

    function updateReq(element, met) {
        const icon = element.querySelector('i');
        if (met) {
            element.classList.add('met');
            icon.className = 'bi bi-check-circle-fill';
        } else {
            element.classList.remove('met');
            icon.className = 'bi bi-circle';
        }
    }

    function validatePasswordForm() {
        const currentPw = currentPwInput.value;
        const newPw = newPwInput.value;
        const confirmPw = confirmPwInput.value;
        
        const lengthOk = newPw.length >= 4 && newPw.length <= 20;
        const upperOk = /[A-Z]/.test(newPw);
        const lowerOk = /[a-z]/.test(newPw);
        const numberOk = /\d/.test(newPw);
        const passwordsMatch = newPw === confirmPw && newPw.length > 0;
        
        updateReq(reqLength, lengthOk);
        updateReq(reqUpper, upperOk);
        updateReq(reqLower, lowerOk);
        updateReq(reqNumber, numberOk);
        
        // Password match feedback
        if (confirmPw.length > 0) {
            if (passwordsMatch) {
                passwordMatchFeedback.textContent = 'Passwords match';
                passwordMatchFeedback.className = 'input-feedback feedback-success';
                confirmPwInput.classList.remove('is-invalid');
                confirmPwInput.classList.add('is-valid');
            } else {
                passwordMatchFeedback.textContent = 'Passwords do not match';
                passwordMatchFeedback.className = 'input-feedback feedback-error';
                confirmPwInput.classList.remove('is-valid');
                confirmPwInput.classList.add('is-invalid');
            }
        } else {
            passwordMatchFeedback.textContent = '';
            passwordMatchFeedback.className = 'input-feedback';
            confirmPwInput.classList.remove('is-valid', 'is-invalid');
        }
        
        const allValid = currentPw.length > 0 && lengthOk && upperOk && lowerOk && numberOk && passwordsMatch;
        savePasswordBtn.disabled = !allValid;
    }

    currentPwInput.addEventListener('input', validatePasswordForm);
    newPwInput.addEventListener('input', validatePasswordForm);
    confirmPwInput.addEventListener('input', validatePasswordForm);

    savePasswordBtn.addEventListener('click', async () => {
        savePasswordBtn.disabled = true;
        savePasswordBtn.innerHTML = '<i class="bi bi-hourglass-split"></i> Updating...';
        
        const formData = new FormData();
        formData.append('current_password', currentPwInput.value);
        formData.append('new_password', newPwInput.value);
        formData.append('confirm_password', confirmPwInput.value);
        
        try {
            const response = await fetch('{{ url_for("auth.change_password") }}', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                currentPwInput.value = '';
                newPwInput.value = '';
                confirmPwInput.value = '';
                validatePasswordForm();
                showToast('Password updated successfully!', 'success');
            } else {
                showToast(data.error || 'Failed to update password', 'error');
            }
        } catch (error) {
            showToast('An error occurred', 'error');
        } finally {
            savePasswordBtn.innerHTML = '<i class="bi bi-shield-check"></i> Update Password';
            validatePasswordForm();
        }
    });

    // =========================
    // Toast Notification
    // =========================
    function showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        const toastIcon = toast.querySelector('.toast-icon');
        const toastMessage = toast.querySelector('.toast-message');
        
        toast.className = 'toast show toast-' + type;
        toastMessage.textContent = message;
        
        switch(type) {
            case 'success':
                toastIcon.className = 'toast-icon bi bi-check-circle-fill';
                break;
            case 'error':
                toastIcon.className = 'toast-icon bi bi-x-circle-fill';
                break;
            default:
                toastIcon.className = 'toast-icon bi bi-info-circle-fill';
        }
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
});

// Toggle password visibility
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const button = input.parentElement.querySelector('.password-toggle i');
    
    if (input.type === 'password') {
        input.type = 'text';
        button.classList.remove('bi-eye');
        button.classList.add('bi-eye-slash');
    } else {
        input.type = 'password';
        button.classList.remove('bi-eye-slash');
        button.classList.add('bi-eye');
    }
}