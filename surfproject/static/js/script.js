
// Initialise Materialize menu 
document.addEventListener('DOMContentLoaded', function() {
    //sidenav initialisation
    let sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav);
        
// Initialise Materialize Select

    var selects = document.querySelectorAll('select');
    M.FormSelect.init(selects);

// Initialise Materialize Parallax

    let paral = document.querySelectorAll('.parallax');
    vM.Parallax.init(paral);

// Initialise Materialize Modal

    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems, {});
    
  });
