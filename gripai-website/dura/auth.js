/**
 * Dura Fulfilment — Gedeeld authenticatie script
 * Laad dit VOOR alle andere scripts op elke portal pagina.
 *
 * Functie:
 * 1. Checkt of er een sessie-token in sessionStorage zit
 * 2. Redirect naar login als dat niet zo is
 * 3. Zet window.DURA_API_BASE en window.DURA_API_HEADERS als globals
 * 4. Vult user-avatar en user-naam in de nav in
 * 5. Verifieert het token async — bij falen redirect naar login
 */
(function () {
    var API_BASE = 'https://dura-backend-production.up.railway.app';

    var token = sessionStorage.getItem('dura_token');
    var user = JSON.parse(sessionStorage.getItem('dura_user') || 'null');

    if (!token || !user) {
        window.location.href = '../demo-dura-login.html';
        return;
    }

    // Globals voor alle pagina-scripts
    window.DURA_API_BASE = API_BASE;
    window.DURA_API_HEADERS = {
        'Authorization': 'Bearer ' + token
    };

    // Nav user info invullen
    var avatar = document.getElementById('userAvatar');
    var uname = document.getElementById('userName');
    if (avatar) avatar.textContent = (user.name || 'D').charAt(0).toUpperCase();
    if (uname) uname.textContent = user.name || 'Gebruiker';

    // Async token verificatie — redirect bij ongeldig/verlopen token
    fetch(API_BASE + '/api/auth/verify', {
        headers: { 'Authorization': 'Bearer ' + token }
    }).then(function (res) {
        if (!res.ok) {
            sessionStorage.removeItem('dura_token');
            sessionStorage.removeItem('dura_user');
            window.location.href = '../demo-dura-login.html';
        }
    }).catch(function () {
        // Netwerk-fout: niet direct uitloggen, pagina werkt offline via cache
    });
})();
