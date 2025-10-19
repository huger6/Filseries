document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('contact-form');
    const submitButton = document.getElementById('submit-form-button');
    const fields = Array.from(form.querySelectorAll('input:not([type="submit"]), select'));

    // Updates form button
    const toggleSubmit = () => {
		if (form.checkValidity()) {
			submitButton.classList.remove('btn-disabled');
		}
		else {
			submitButton.classList.add('btn-disabled');
		}
    };

    const shouldValidate = field => field.hasAttribute('required') || field.value.trim() !== '';

    fields.forEach(field => {
		field.addEventListener('blur', () => {
			if (!shouldValidate(field)) {
				field.classList.remove('is-invalid', 'is-valid');
				return;
			}
			if (field.checkValidity()) {
				field.classList.add('is-valid');
				field.classList.remove('is-invalid');
			} 
			else {
				field.classList.add('is-invalid');
				field.classList.remove('is-valid');
			}
			toggleSubmit();
		})

		field.addEventListener('input', () => {
			field.classList.remove('is-invalid', 'is-valid');
			toggleSubmit();
		});

		field.addEventListener('change', () => {
			if (shouldValidate(field)) {
				if (field.checkValidity()) {
					field.classList.add('is-valid');
					field.classList.remove('is-invalid');
				}
				else {
					field.classList.add('is-invalid');
					field.classList.remove('is-valid');
				}
			}
			else {
				field.classList.remove('is-invalid', 'is-valid');
			}
			toggleSubmit();
		});
    });

    // Submiting form
    form.addEventListener('submit', (e) => {
		if (!form.checkValidity()) {
			e.preventDefault();
			e.stopPropagation();

			// Marks all invalid fields
			fields.forEach(field => {
				if (shouldValidate(field) && !field.checkValidity()) {
					field.classList.add('is-invalid');
				}
        	});
      	}
    });

    submitButton.addEventListener('click', e => {
      fields.forEach(field => {
        if (shouldValidate(field)) {
			if (field.checkValidity()) {
				field.classList.remove('is-invalid');
				field.classList.add('is-valid');
			}
			else {
				field.classList.remove('is-valid');
				field.classList.add('is-invalid');
			}
        }
        else {
          field.classList.remove('is-invalid', 'is-valid');
        }
      });
    });

	// Confirm if passwords match if in register page
	if (page === "register") { // page is passed via a script in html (using jinja)
		let timeout;
		document.getElementById("confirm-password").addEventListener("change", function() {
			clearTimeout(timeout);
			const pw = document.getElementById("password").value;
			const confirm_pw = this;
			
			timeout = setTimeout(() => {
				if (pw !== confirm_pw.value) {
					confirm_pw.classList.remove('is-valid');
					confirm_pw.classList.add('is-invalid');
				} 
				else {
					confirm_pw.classList.remove('is-invalid');
					confirm_pw.classList.add('is-valid');
					console.log("Marked valid");
				}
				toggleSubmit();
			}, 600);
		});
	}

    toggleSubmit();
});
