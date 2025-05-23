document.addEventListener('DOMContentLoaded', function() {
    // Zvýraznění aktivního odkazu v navigaci
    const navLinks = document.querySelectorAll('nav ul li a');
    navLinks.forEach(link => {
        if (link.href === window.location.href) {
            link.style.fontWeight = 'bold';
            link.style.textDecoration = 'underline';
        }
    });

    // Potvrzení před smazáním
    const deleteButtons = document.querySelectorAll('.delete-button');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            if (!confirm('Opravdu chcete tuto položku smazat?')) {
                event.preventDefault();
            }
        });
    });

    // Přidání interaktivních prvků pro dashboard
    const toggleButtons = document.querySelectorAll('.toggle-details');

    toggleButtons.forEach(button => {
        button.addEventListener('click', function () {
            const details = this.nextElementSibling;
            if (details.style.display === 'none' || !details.style.display) {
                details.style.display = 'block';
                this.textContent = 'Skrýt detaily';
            } else {
                details.style.display = 'none';
                this.textContent = 'Zobrazit detaily';
            }
        });
    });

    // Přidání filtrování a třídění na dashboard

    const filterInput = document.getElementById('filter-input');
    const tableRows = document.querySelectorAll('.dashboard-table tbody tr');

    filterInput.addEventListener('input', function () {
        const filterValue = this.value.toLowerCase();
        tableRows.forEach(row => {
            const rowText = row.textContent.toLowerCase();
            row.style.display = rowText.includes(filterValue) ? '' : 'none';
        });
    });

    const sortButtons = document.querySelectorAll('.sort-button');
    sortButtons.forEach(button => {
        button.addEventListener('click', function () {
            const column = this.dataset.column;
            const order = this.dataset.order;
            const rowsArray = Array.from(tableRows);

            rowsArray.sort((a, b) => {
                const aText = a.querySelector(`td[data-column="${column}"]`).textContent;
                const bText = b.querySelector(`td[data-column="${column}"]`).textContent;
                return order === 'asc' ? aText.localeCompare(bText) : bText.localeCompare(aText);
            });

            const tbody = document.querySelector('.dashboard-table tbody');
            rowsArray.forEach(row => tbody.appendChild(row));

            this.dataset.order = order === 'asc' ? 'desc' : 'asc';
        });
    });

    // Přidání vizuálních indikátorů pro načítání dat

    const loadingIndicator = document.getElementById('loading-indicator');

    function showLoading() {
        loadingIndicator.style.display = 'block';
    }

    function hideLoading() {
        loadingIndicator.style.display = 'none';
    }

    // Příklad použití při načítání dat
    const loadDataButton = document.getElementById('load-data-button');
    if (loadDataButton) {
        loadDataButton.addEventListener('click', function () {
            showLoading();
            setTimeout(() => {
                hideLoading();
                alert('Data byla načtena!');
            }, 2000); // Simulace načítání dat
        });
    }

    // Přidání notifikací pro uživatele
    function showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    // Příklad použití notifikace
    const exportButton = document.getElementById('export-button');
    if (exportButton) {
        exportButton.addEventListener('click', function () {
            showNotification('Export dat byl úspěšný!');
        });
    }
});

// Stylování notifikací
const style = document.createElement('style');
style.textContent = `
.notification {
    position: fixed;
    top: 24px;
    right: 24px;
    background: linear-gradient(90deg, #bfa14a 0%, #fffbe6 100%);
    color: #181818;
    padding: 16px 32px;
    border-radius: 10px;
    font-size: 1.1em;
    box-shadow: 0 4px 16px rgba(191,161,74,0.18);
    z-index: 9999;
    font-family: 'Inter', 'Roboto', Arial, sans-serif;
    animation: fadeIn 0.5s;
}
.notification.error {
    background: linear-gradient(90deg, #181818 0%, #bfa14a 100%);
    color: #fff;
    border: 2px solid #bfa14a;
}
@keyframes fadeIn {
    from { opacity: 0; right: 0; }
    to { opacity: 1; right: 24px; }
}
`;
document.head.appendChild(style);
