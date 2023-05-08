document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.editform').forEach(function(editform){
        editform.style.display='none'
    }) 
    document.querySelectorAll('.edit').forEach(button => {
        button.onclick = function() {
            hide(this.dataset.id);
        };
    });

    document.querySelectorAll('.save').forEach(button =>{
        button.onclick = function(){
            edit(this.dataset.id)
        }
    })

    document.querySelectorAll('.ffa').forEach(button =>{
        button.onclick = function(){
            like(this)
        }
    })


    
});

function hide(post) {
    document.querySelector(`#post-${post}`).style.display = 'none';
    document.querySelector(`#form-${post}`).style.display = 'block';
    document.querySelector(`#btn-${post}`).style.display = 'none'
}

function show(post) {
    document.querySelector(`#post-${post}`).style.display = 'block';
    document.querySelector(`#form-${post}`).style.display = 'none';
    document.querySelector(`#btn-${post}`).style.display = 'block'
}

function edit(id){
    const posttext = document.querySelector(`#text-${id}`).value
    fetch('/edit/'+`${id}`,{
        method : 'POST',
        body : JSON.stringify({
            POST : posttext
        })
    })
    document.querySelector(`#inpost-${id}`).textContent = posttext;
    show(id)
}


async function like(element){
    const likeid = element.dataset.id
    const user = document.querySelector(`#user-${likeid}`).innerHTML
    form = new FormData()
    form.append('user',user)
    await fetch('/like/'+`${likeid}`,{
        method : 'POST',
        body : form
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 0){
            document.querySelector(`#count-${likeid}`).innerHTML = data.count
            element.className = data.btn_class
        }
        else{
            console.log('failed')
        }
    })
    return false
}
