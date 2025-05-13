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
});
