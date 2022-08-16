
// Initialise Materialize menu 
document.addEventListener('DOMContentLoaded', function() {
    //sidenav initialisation
    let sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav);
  });

        
// Initialise Materialize Select
document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('select');
  var instances = M.FormSelect.init(elems, options);
});