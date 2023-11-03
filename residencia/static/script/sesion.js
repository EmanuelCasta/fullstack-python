document.querySelector('.btn-registrar').addEventListener('click', function(e) {
    e.preventDefault();
  

    let form = document.querySelector('.form-signup');


    let formData = new FormData(form);

 
    let object = {};
    formData.forEach(function(value, key) {
        object[key] = value;
    });


    fetch('http://localhost:8000/residencia/usuario/registrar/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(object)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.message);
            });
        }
        alert(response.json());  
        return response.json();
    })
    .then(data => {
        
        
        document.cookie = "token=" + data.access;
        document.cookie = "usuario_id=" + data.usuario;
    })
    .catch(error => {
        console.error('Error:', error.message);
        alert(error.message);  
    });

});




const switchers = [...document.querySelectorAll('.switcher')]

switchers.forEach(item => {
	item.addEventListener('click', function() {
		switchers.forEach(item => item.parentElement.classList.remove('is-active'))
		this.parentElement.classList.add('is-active')
	})
})
