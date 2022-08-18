
// Initialise Materialize menu 
document.addEventListener('DOMContentLoaded', function() {
    //sidenav initialisation
    let sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav);
        
// Initialise Materialize Select

    let selects = document.querySelectorAll('select');
    M.FormSelect.init(selects);

// Initialise Materialize Parallax

    let paral = document.querySelectorAll('.parallax');
    vM.Parallax.init(paral);
  });
