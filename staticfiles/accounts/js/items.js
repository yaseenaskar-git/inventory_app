// Item modal JS: Prevent duplicate submissions, handle success/error, reliable submit

document.addEventListener('DOMContentLoaded', function() {
    const inventoryId = window.INVENTORY_ID;
    const itemForm = document.getElementById('itemForm');
    const saveItemBtn = document.getElementById('saveItemBtn');
    const itemFormAlert = document.getElementById('itemFormAlert');
    const itemModalEl = document.getElementById('itemModal');
    let isSubmitting = false;

    async function fetchJSON(url, opts={}) {
        try {
            const res = await fetch(url, opts);
            const data = await res.json();
            return data;
        } catch (err) {
            return { success: false, error: 'Network or server error.' };
        }
    }

    itemForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        if (isSubmitting) return;
        isSubmitting = true;
        saveItemBtn.disabled = true;
        saveItemBtn.textContent = 'Saving...';
        itemFormAlert.classList.add('d-none');
        itemFormAlert.classList.remove('alert-danger');
        itemFormAlert.textContent = '';

        const id = document.getElementById('itemId').value;
        const url = id ? `/accounts/inventories/${inventoryId}/items/${id}/update/` : `/accounts/inventories/${inventoryId}/items/create/`;
        const fd = new FormData(itemForm);

        let data;
        try {
            const res = await fetch(url, {
                method: 'POST',
                headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value },
                body: fd
            });
            data = await res.json();
        } catch (err) {
            itemFormAlert.classList.remove('d-none');
            itemFormAlert.classList.add('alert-danger');
            itemFormAlert.textContent = 'Network/server error.';
            saveItemBtn.disabled = false;
            saveItemBtn.textContent = 'Save';
            isSubmitting = false;
            return;
        }

        if (data && data.success) {
            const modal = bootstrap.Modal.getInstance(itemModalEl);
            if (modal) modal.hide();
            window.location.reload();
        } else {
            itemFormAlert.classList.remove('d-none');
            itemFormAlert.classList.add('alert-danger');
            itemFormAlert.textContent = JSON.stringify(data.errors || data.error || 'Unknown error');
            saveItemBtn.disabled = false;
            saveItemBtn.textContent = 'Save';
            isSubmitting = false;
        }
    });

    itemModalEl.addEventListener('hidden.bs.modal', function() {
        isSubmitting = false;
        saveItemBtn.disabled = false;
        saveItemBtn.textContent = 'Save';
        itemFormAlert.classList.add('d-none');
        itemFormAlert.classList.remove('alert-danger');
        itemFormAlert.textContent = '';
    });
});
